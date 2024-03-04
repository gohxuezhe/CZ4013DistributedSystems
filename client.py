import sys
import socket
import marshalling

# Define server IP address and port
SERVER_IP = '172.20.10.10' # CHANGE IP ADDRESS ACCORDINGLY TO THE IP ADDRESS OF SERVER
SERVER_PORT = 12345

# Client function
def main(service_called, filename, offset, length_of_bytes, content):
    
    # Create a message object
    # 'read' request message
    if service_called=='read':
        message_data = (0, filename, offset, length_of_bytes) # service_code (term used in marshalling.py) = 0: refers to read
        marshalled_message_data = marshalling.read_service_client_message(*message_data).marshal()
        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            # Send the marshalled data to the server
            client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
            
            # Receive response from the server
            response, server_address = client_socket.recvfrom(1024)
            print("Received data from server:", response.decode())

            # Unmarshal the received data
            response_message = marshalling.read_service_server_message.unmarshal(response)
            print("Unmarshalled data:", response_message.file_data)
    
    # 'write' request message
    elif service_called=='write':
        message_data = (1, filename, offset, content) # service_code (term used in marshalling.py) = 1: refers to write
        marshalled_message_data = marshalling.write_service_client_message(*message_data).marshal()
        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            # Send the marshalled data to the server
            client_socket.sendto(marshalled_message_data, (SERVER_IP, SERVER_PORT))
            
            # Receive response from the server
            response, server_address = client_socket.recvfrom(1024)
            print("Received data from server:", response.decode())

            # Unmarshal the received data
            response_message = marshalling.write_service_server_message.unmarshal(response)
            print("Unmarshalled data:", response_message.file_data)

if __name__ == "__main__":
    # Check if command-line arguments are provided correctly
    if (len(sys.argv) < 5):
        print("Usage: python client.py <service_called> <filename> <offset> <length_of_bytes (if applicable)> <content (if applicable)>")
        sys.exit(1)
    
    # Utilisation of command-line arguments
    service_called = sys.argv[1]
    filename = sys.argv[2]
    offset = int(sys.argv[3])
    if service_called == 'read':
        length_of_bytes = int(sys.argv[4])
    else:
        length_of_bytes = None
    content = ' '.join(sys.argv[5:]) if len(sys.argv) > 5 else None
    
    # Calling main
    main(service_called, filename, offset, length_of_bytes, content)
