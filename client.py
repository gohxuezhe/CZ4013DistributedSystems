import os
from dotenv import load_dotenv
import sys
import socket
import time
import marshalling

load_dotenv()
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

# CONSTANTS
CLIENT_SERVICE_MESSAGE = """Client Services Available:
1. Read
2. Write
3. Monitor
4. Idempotent Operation
5. Non-Idempotent Operation
6. Quit
Enter the service number you want to call: """
FILE_PATHNAME_MESSAGE = "Enter the file pathname: "
OFFSET_MESSAGE = "Enter the offset: "
LENGTH_OF_BYTES_MESSAGE = "Enter length of bytes to read: "
CONTENT_MESSAGE = "Enter content to write: "

# Cache dictionary to hold file contents and timestamps
cache = {}

# Freshness interval (in seconds)
t = 60 

# Create a UDP socket
def create_UDP_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Client function
def service(service_called, file_pathname, offset, length_of_bytes, content, length_of_monitoring_interval):
    global cache
    
    # Check cache before requesting data from the server
    if service_called == "read":
        if file_pathname in cache:
            cache_entry = cache[file_pathname]
            Tc = cache_entry.get('Tc', 0)
            print("Tc: ", Tc)
            Tmclient = cache_entry.get('Tmclient', 0)
            print("Tmclient: ", Tmclient)
            current_time = time.time()
            print("current_time: ", current_time)
            # Evaluate whether T - Tc < t
            if current_time - Tc < t:
                print("current_time - Tc < t")
                response_data = ""
                for i in range(offset, offset + length_of_bytes):
                    if i in cache_entry['data']:
                        response_data+=cache_entry['data'][i]
                        print("cache_entry['data'][",i,"]",(cache_entry['data'][i]))                    
                    else:
                        response_data+=fill_cache(file_pathname, i) # If the byte is missing, call read service to fill it
                        print("NEWLY FILLED cache_entry['data'][",i,"]",(cache_entry['data'][i])) 
                        
                print("Response from cache:", response_data)
                print("Cache content:", cache)
                return
            else:
                print("current_time - Tc >= t")
                # Call tmserver service to obtain tmserver value
                Tmserver = service("tmserver", file_pathname, None, None, None, None)
                if Tmclient == Tmserver:
                    print("Cache entry is valid.")
                    # Update Tc
                    cache_entry['Tc'] = current_time
                else:
                    print("Cache entry is invalidated. Requesting updated data from server.")
                    # Update Tc
                    cache_entry['Tc'] = current_time
                    # Call read service to fill cache with updated data
                    service("read", file_pathname, offset, length_of_bytes, None, None)
                print("Cache content:", cache)
                return

    # 'read' request message
    if service_called == "read":
        message_data = (1, file_pathname, offset, length_of_bytes) # service_code (term used in marshalling.py) = 0: refers to read
        marshalled_message_data = marshalling.ReadServiceClientMessage(*message_data).marshal()
        # Send the marshalled data to the server
        client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshal the received data
        response_message = marshalling.ReadServiceServerMessage.unmarshal(response)
        # Update cache
        cache_entry = {
            'data': {offset + i: response_message.file_data[i] for i in range(len(response_message.file_data))},
            'Tc': time.time(),  # Update Tc
            'Tmclient': service("tmserver", file_pathname, None, None, None, None)
        }
        print("Cache content BEFORE:", cache)
        cache[file_pathname] = cache_entry
        print("Cache content AFTER:", cache)
        print("Response:", response_message.file_data)

    # 'write' request message
    elif service_called == 'write':
        message_data = (2, file_pathname, offset, content)  # service_code (term used in marshalling.py) = 1: refers to write
        marshalled_message_data = marshalling.WriteServiceClientMessage(*message_data).marshal()
        # Send the marshalled data to the server
        client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshal the received data
        response_message = marshalling.WriteServiceServerMessage.unmarshal(response)
        # Check if file_pathname exists in the cache, if exists update cache too, else dont care
        if file_pathname in cache:
            print(file_pathname, "in cache, going in to update")
            print("Cache content BEFORE:", cache)
            cache_entry = cache.get(file_pathname, {})  # Retrieve existing cache entry or create a new one if it doesn't exist
            written_content_length = len(content)

            # Update existing keys to shift up or down depending on where the new data is written
            temp_data = {}
            for key, value in cache_entry['data'].items():
                if key >= offset:
                    temp_data[key + written_content_length] = value  # Shift keys up
                else:
                    temp_data[key] = value  # Keep existing keys as they are

            # Insert new data into temporary dictionary
            for i in range(written_content_length):
                temp_data[offset + i] = content[i]

            # Update cache entry with temporary data
            cache_entry['data'] = temp_data

            # Update Tc and Tmclient to current time
            cache_entry['Tc'] = time.time()
            cache_entry['Tmclient'] = time.time()
            cache[file_pathname] = cache_entry
        print("Cache content AFTER:", cache)
        print("Response:", response_message.file_data)

    # 'monitor' request message
    elif service_called=='monitor':
        message_data = (3, file_pathname, length_of_monitoring_interval) # service_code (term used in marshalling.py) = 2: refers to monitor
        marshalled_message_data = marshalling.MonitorServiceClientMessage(*message_data).marshal()
        # Send the marshalled data to the server
        client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024) #todo: implement while loop here
        # Unmarshal the received data
        response_message = marshalling.MonitorServiceServerMessage.unmarshal(response)
        print("Response:", response_message.file_data)

    # 'tmrserver' request message
    elif service_called == 'tmserver':
        message_data = (3, file_pathname)  # service_code (term used in marshalling.py) = 3: refers to tmserver
        marshalled_message_data = marshalling.tmserver_service_client_message(*message_data).marshal()
        # Send the marshalled data to the server
        client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshal the received data
        response_message = marshalling.tmserver_service_server_message.unmarshal(response)
        return response_message.Tmserver

# Helper function to fill in missing bytes into cache from server
def fill_cache(file_pathname, offset):
        # Call read service to fill the missing byte in cache
        message_data = (0, file_pathname, offset, 1)  # service_code (term used in marshalling.py) = 0: refers to read
        marshalled_message_data = marshalling.read_service_client_message(*message_data).marshal()
        # Send the marshalled data to the server
        client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshal the received data
        response_message = marshalling.read_service_server_message.unmarshal(response)
        
        # Update cache entry with new byte key and value
        cache_entry = cache.get(file_pathname, {})
        cache_entry['data'] = {**cache_entry.get('data', {}), **{offset: response_message.file_data}}
        cache[file_pathname] = cache_entry

        return response_message.file_data

if __name__ == "__main__":
    client_socket = create_UDP_socket()
    while True:
        try:
            option = int(input(CLIENT_SERVICE_MESSAGE))
            if option == 1:
                file_pathname = input(FILE_PATHNAME_MESSAGE)
                offset = int(input(OFFSET_MESSAGE))
                length_of_bytes = int(input(LENGTH_OF_BYTES_MESSAGE))
                service("read", file_pathname, offset, length_of_bytes, None, None)
            elif option == 2:
                file_pathname = input(FILE_PATHNAME_MESSAGE)
                offset = int(input(OFFSET_MESSAGE))
                content = input(CONTENT_MESSAGE)
                service("write", file_pathname, offset, None, content, None)
            elif option == 3:
                file_pathname = input(FILE_PATHNAME_MESSAGE)
                length_of_monitoring_interval = int(input("Enter the length of monitoring interval (in min): "))
                service("monitor", file_pathname, None, None, None, length_of_monitoring_interval)
            elif option == 4:
                print("Not implemented yet.")
            elif option == 5:
                print("Not implemented yet.")
            else:
                sys.exit()
        except Exception as e:
            print("Error:", e)
        print('\n')
