import os
from dotenv import load_dotenv
import sys
import socket
import time
import marshalling

load_dotenv()
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
print(SERVER_IP, SERVER_PORT)

# CONSTANTS
CLIENT_SERVICE_MESSAGE = """Client Services Available:
1. Read
2. Write
3. Monitor
4. Like File
5. File Liked By
6. Quit
Enter the service number you want to call: """
FILE_PATHNAME_MESSAGE = "Enter the file pathname: "
OFFSET_MESSAGE = "Enter the offset: "
LENGTH_OF_BYTES_MESSAGE = "Enter length of bytes to read: "
CONTENT_MESSAGE = "Enter content to write: "
MONITORING_INTERVAL_MESSAGE = "Enter the length of monitoring interval (in min): "
# Freshness interval (in seconds)
t = 60
# Cache dictionary to hold file contents and timestamps
cache = {}


# Client function
def service(service_called, file_pathname, offset, length_of_bytes, content, length_of_monitoring_interval):
    global cache

    # 'read' request message
    if service_called == "read":
        # IF CACHE HAS THAT FILE
        if file_pathname in cache:
            cache_entry = cache[file_pathname]
            response_data = ""
            for i in range(offset, offset + length_of_bytes):
                if i in cache_entry["data"]:
                    cache_byte_entry = cache_entry["data"][i]
                    Tc = cache_byte_entry.get("Tc", 0)
                    print(f"Tc: {Tc}")
                    Tmclient = cache_byte_entry.get("Tmclient", 0)
                    print(f"Tmclient: {Tmclient}")
                    current_time = time.time()
                    print(f"current_time: {current_time}")
                    if current_time - Tc < t:
                        print("current_time - Tc < t")
                        # Cache hit, byte is still fresh
                        response_data += cache_entry["data"][i]["data"]
                        print(f"cache_entry[\"data\"][\"{i}\"][\"data\"]: {cache_entry['data'][i]['data']}")
                    else:
                        print("current_time - Tc >= t")
                        # Call tmserver service to obtain tmserver value
                        Tmserver = service("tmserver", file_pathname, i, None, None, None)
                        if Tmclient == Tmserver:
                            # Cache entry is valid, byte is still fresh
                            print("Cache entry is valid.")
                            # Update Tc
                            cache_byte_entry["Tc"] = current_time
                            cache_entry["data"][i] = cache_byte_entry
                            cache[file_pathname] = cache_entry
                            response_data += cache_entry["data"][i]["data"]
                            print(f"cache_entry[\"data\"][\"{i}\"][\"data\"]: {cache_entry['data'][i]['data']}")
                        else:
                            # Cache entry is invalid, need request byte from server
                            print("Cache entry is invalidated. Requesting updated data from server.")
                            response_data += fill_cache(file_pathname, i)  # Read and update the byte
                            print(f"UPDATED cache_entry[\"data\"][\"{i}\"][\"data\"]: {cache_entry['data'][i]['data']}")
                else:
                    # Byte not found in cache, fetch it from server
                    response_data += fill_cache(file_pathname, i)  # If the byte is missing, call read service to fill it
                    print(f"NEWLY FILLED cache_entry[\"data\"][\"{i}\"][\"data\"]: {cache_entry['data'][i]['data']}")
            print(f"Cache content: {cache}")
            print(f"data that is read in: {response_data}")
            return

        # IF CACHE DOES NOT HAVE THAT FILE
        else:
            message_data = (1, file_pathname, offset, length_of_bytes) # service_code (term used in marshalling.py) = 1: refers to read
            marshallled_message_data = marshalling.ReadServiceClientMessage(*message_data).marshal()
            # Send the marshallled data to the server
            client_socket.sendto(marshallled_message_data, (SERVER_IP, SERVER_PORT))
            # Receive response from the server
            response, _ = client_socket.recvfrom(1024)
            # Unmarshall the received data
            response_message = marshalling.ReadServiceServerMessage.unmarshal(response)
            print(f"Cache content BEFORE: {cache}")
            # Update cache for each byte
            cache_entry = cache.get(file_pathname, {})
            for i in range(offset, offset + length_of_bytes):
                byte_cache = cache_entry.get("data", {})
                byte_cache_entry = {"data": response_message.file_data[i - offset], "Tc": time.time(), "Tmclient": service("tmserver", file_pathname, i, None, None, None)}
                byte_cache[i] = byte_cache_entry
                cache_entry["data"] = byte_cache
            cache[file_pathname] = cache_entry
            print(f"Cache content AFTER: {cache}")
            print(f"Response: {response_message.file_data}")

    # 'write' request message
    elif service_called == "write":
        message_data = (2, file_pathname, offset, content)  # service_code (term used in marshalling.py) = 2: refers to write
        marshallled_message_data = marshalling.WriteServiceClientMessage(*message_data).marshal()
        # Send the marshalled data to the server
        client_socket.sendto(marshallled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshall the received data
        response_message = marshalling.WriteServiceServerMessage.unmarshal(response)

        # If file_pathname in cache, update cache entry for each byte being written
        if file_pathname in cache:
            print(f"{file_pathname} in cache, going in to update")
            print(f"Cache content BEFORE: {cache}")
            cache_entry = cache.get(file_pathname, {})  # Retrieve existing cache entry or create a new one if it doesn't exist
            written_content_length = len(content)

            # Update existing keys to shift up or down depending on where the new data is written
            temp_data = {}
            for key, value in cache_entry["data"].items():
                if key >= offset:
                    temp_data[key + written_content_length] = value  # Shift keys up
                else:
                    temp_data[key] = value  # Keep existing keys as they are

            # Insert new data into temporary dictionary
            for i in range(written_content_length):
                temp_data[offset + i] = {"data": content[i], "Tc": time.time(), "Tmclient": time.time()}
            # Update cache entry with temporary data
            cache_entry["data"] = temp_data
            cache[file_pathname] = cache_entry

        # If file_pathname not in cache, create a new cache entry
        else: 
            print(file_pathname, "not in cache, creating new entry")
            new_cache_entry = {'data': {}, 'Tc': time.time(), 'Tmclient': time.time()}
            written_content_length = len(content)
            # Insert new data into temporary dictionary
            for i in range(written_content_length):
                new_cache_entry['data'][offset + i] = {'data': content[i], 'Tc': time.time(), 'Tmclient': time.time()}
            # Update cache with new entry
            cache[file_pathname] = new_cache_entry
        print(f"Cache content AFTER: {cache}")
        print(f"Response: {response_message.file_data}")

    # 'monitor' request message
    elif service_called == "monitor":
        message_data = (3, file_pathname, length_of_monitoring_interval) # service_code (term used in marshalling.py) = 3: refers to monitor
        marshallled_message_data = marshalling.MonitorServiceClientMessage(*message_data).marshal()
        # Send the marshallled data to the server
        client_socket.sendto(marshallled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshall the received data
        response_message = marshalling.MonitorServiceServerMessage.unmarshal(response)
        print(f"Response: {response_message.file_data}")
        # Set timeout for monitoring
        client_socket.settimeout(length_of_monitoring_interval * 60)

        while True:
            try:
                # Receive response from the server
                response, _ = client_socket.recvfrom(1024)
                # Unmarshall the received data
                response_message = marshalling.MonitorCallbackServiceServerMessage.unmarshal(response)
                print(f'New update for {file_pathname}: {response_message.file_data}')
                print(f"Cache content BEFORE: {cache}")
                # Update the cache
                cache_entry = {}
                for i in range(len(response_message.file_data)):
                    byte_cache = cache_entry.get("data", {})
                    byte_cache_entry = {"data": response_message.file_data[i], "Tc": time.time(), "Tmclient": service( "tmserver", file_pathname, i, None, None, None)}
                    byte_cache[i] = byte_cache_entry
                    cache_entry["data"] = byte_cache
                cache[file_pathname] = cache_entry
                print(f"Cache content AFTER: {cache}")
            except socket.timeout:
                print("Monitoring completed.")
                return
            except Exception as e:
                print("Error:", e)

    # 'like' request message
    elif service_called == "like":
        message_data = (4, file_pathname)  # service_code (term used in marshalling.py) = 4: refers to like
        marshallled_message_data = marshalling.LikeServiceClientMessage(*message_data).marshal()
        # Send the marshallled data to the server
        client_socket.sendto(marshallled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshall the received data
        response_message = marshalling.LikeServiceServerMessage.unmarshal(response)
        print(f"Response: {response_message.like_status}")

    # 'liked_by' request message
    elif service_called == "liked_by":
        message_data = (5, file_pathname)
        marshallled_message_data = marshalling.LikedByServiceClientMessage(*message_data).marshal()
        # Send the marshallled data to the server
        client_socket.sendto(marshallled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshall the received data
        response_message = marshalling.LikedByServiceServerMessage.unmarshal(response)
        print(f"Response: {response_message.liked_by}")

    # 'tmserver' request message
    elif service_called == "tmserver":
        message_data = (69, file_pathname, offset)  # service_code (term used in marshalling.py) = 69: refers to tmserver
        marshallled_message_data = marshalling.TmserverServiceClientMessage(*message_data).marshal()
        # Send the marshallled data to the server
        client_socket.sendto(marshallled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshall the received data
        response_message = marshalling.TmserverServiceServerMessage.unmarshal(response)
        return response_message.modification_time


# Helper function to fill in missing bytes into cache from server
def fill_cache(file_pathname, offset):
    # Call read service to fill the missing byte in cache
    message_data = (1, file_pathname, offset, 1)  # service_code (term used in marshalling.py) = 1: refers to read
    marshallled_message_data = marshalling.ReadServiceClientMessage(*message_data).marshal()
    # Send the marshalled data to the server
    client_socket.sendto(marshallled_message_data, (SERVER_IP, SERVER_PORT))
    # Receive response from the server
    response, _ = client_socket.recvfrom(1024)
    # Unmarshall the received data
    response_message = marshalling.ReadServiceServerMessage.unmarshal(response)

    # Update cache entry with new byte key and value along with timestamps
    cache_entry = cache.get(file_pathname, {})
    byte_cache = cache_entry.get("data", {})
    byte_cache_entry = {"data": response_message.file_data, "Tc": time.time(), "Tmclient": service("tmserver", file_pathname, offset, None, None, None)}
    byte_cache[offset] = byte_cache_entry
    cache_entry["data"] = byte_cache
    cache[file_pathname] = cache_entry

    return response_message.file_data


if __name__ == "__main__":
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
                length_of_monitoring_interval = int(input(MONITORING_INTERVAL_MESSAGE))
                service("monitor", file_pathname, None, None, None, length_of_monitoring_interval)
            elif option == 4:
                file_pathname = input(FILE_PATHNAME_MESSAGE)
                service("like", file_pathname, None, None, None, None)
            elif option == 5:
                file_pathname = input(FILE_PATHNAME_MESSAGE)
                service("liked_by", file_pathname, None, None, None, None)
            else:
                sys.exit()
        except Exception as e:
            print("Error:", e)
        print("\n")
