import sys
import socket
import time
import marshalling

# CONSTANTS
SERVER_IP = '10.238.203.108' # CHANGE IP ADDRESS ACCORDINGLY TO THE IP ADDRESS OF SERVER
SERVER_PORT = 12345
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

# Create a UDP socket
def create_UDP_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Client function
def service(service_called, file_pathname, offset, length_of_bytes, content, length_of_monitoring_interval):
    
    # 'read' request message
    if service_called == "read":
        message_data = (0, file_pathname, offset, length_of_bytes) # service_code (term used in marshalling.py) = 0: refers to read
        marshalled_message_data = marshalling.read_service_client_message(*message_data).marshal()
        # Send the marshalled data to the server
        client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshal the received data
        response_message = marshalling.read_service_server_message.unmarshal(response)
        print("Response:", response_message.file_data)
    
    # 'write' request message
    elif service_called=='write':
        message_data = (1, file_pathname, offset, content) # service_code (term used in marshalling.py) = 1: refers to write
        marshalled_message_data = marshalling.write_service_client_message(*message_data).marshal()
        # Send the marshalled data to the server
        client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
        # Receive response from the server
        response, _ = client_socket.recvfrom(1024)
        # Unmarshal the received data
        response_message = marshalling.write_service_server_message.unmarshal(response)
        print("Response:", response_message.file_data)

    # 'monitor' request message
    elif service_called=='monitor':
        message_data = (2, file_pathname, length_of_monitoring_interval) # service_code (term used in marshalling.py) = 2: refers to monitor
        marshalled_message_data = marshalling.monitor_service_client_message(*message_data).marshal()

        # Send the marshalled data to the server
        

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
                length_of_monitoring_interval = int(input("Enter the length of monitoring interval: "))
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
