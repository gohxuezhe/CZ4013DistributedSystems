import os
from dotenv import load_dotenv
import socket
import marshalling
import datetime
from collections import defaultdict

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
udp_socket.bind((ip_address, 12345))
print(f"Server listening on IP: {ip_address} and Port: {12345}")

load_dotenv()
INVOCATION_SEMANTICS = os.getenv("INVOCATION_SEMANTICS")
print(f"Invocation Semantic: {INVOCATION_SEMANTICS}")

monitor_dict = defaultdict(list)
like_dict = defaultdict(list)
request_history = {}


# Read content from file function
def read_file(file_name, offset, length):
    try:
        with open(file_name, "r") as file:
            # Move to the specified offset
            file.seek(offset)
            # Read the specified length of bytes
            data = file.read(length)
            # Check if end of file is reached
            if not data:
                return 0, "End of File"
            return 0, data
    except FileNotFoundError:
        return 1, "File not found."
    except IOError:
        return 1, "Unable to read the file."
    except ValueError:
        return 1, "Invalid offset or length."
    except Exception as e:
        return 1, f"{e}"

# Write content to file function
def write_file(file_name, offset, content):
    try:
        with open(file_name, 'rb+') as file:
            # Navigate to the specified offset
            file.seek(offset)
            # Read the content after the offset
            existing_content = file.read()
            # Move back to the offset
            file.seek(offset)
            # Write the new content (convert string to bytes)
            file.write(content.encode('utf-8'))
            # Write back the existing content
            file.write(existing_content)

        return 0, f"Successful write to {file_name} at offset {offset}"
    except Exception as e:
        return 1, f"{e}"

# Monitor file (add to monitor_dict)
def monitor_file(file_name, length_of_monitoring_interval, address):
    try:
        with open(file_name, "r"):
            pass

        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(minutes=length_of_monitoring_interval)
        
        current_time_fmt = current_time.strftime("%H:%M:%S")
        end_time_fmt = end_time.strftime("%H:%M:%S")

        monitor_dict[file_name].append((address, end_time))

        return 0, f"Client ({address}) is monitoring {file_name} for {length_of_monitoring_interval} min from {current_time_fmt} to {end_time_fmt}"
    except FileNotFoundError:
        return 1, "File not found."
    except Exception as e:
        return 1, f"{e}"

# Update monitoring clients about file updates, and update monitor_dict to remove clients who are no longer monitoring
def monitor_callback(file_name):
    for address, end_time in monitor_dict[file_name]:
        current_time = datetime.datetime.now()
        new_monitor_list = []

        if current_time <= end_time:
            # Read the whole file
            status, data_to_send = read_file(file_name, 0, -1)
            # Send the whole file to the monitoring client
            marshalled_data = marshalling.ServerMessage(status, data_to_send).marshal()
            udp_socket.sendto(marshalled_data, address)
            new_monitor_list.append((address, end_time))

        monitor_dict[file_name] = new_monitor_list

def like(file_name, address):
    try:
        with open(file_name, "r"):
            pass
        if file_name not in like_dict or address not in like_dict[file_name]:
            like_dict[file_name].append(address)
            return 0, "Liked"
        else:
            like_dict[file_name].remove(address)
            return 0, "Unliked"
    except FileNotFoundError:
        return 1, "File not found."
    except Exception as e:
        return 1, f"{e}"

def like_by(file_name):
    try:
        with open(file_name, "r"):
            pass
        list_of_likes = like_dict[file_name]
        if (len(list_of_likes) > 0):
            return 0, ''.join([f"IP: {ip}, Port: {port}\n" for ip, port in list_of_likes])
        else:
            return 0, "No likes yet."
    except FileNotFoundError:
        return 1, "File not found."
    except Exception as e:
        return 1, f"{e}"

# Get modification time of byte in file
def get_modification_time(file_name, byte_index):
    try:
        if byte_index is not None:
            with open(file_name, 'rb') as file:
                file.seek(byte_index)
                file.read(1)  # Read a single byte to ensure we reach the desired position
                byte_modification_time = os.fstat(file.fileno()).st_mtime
            return 0, datetime.datetime.fromtimestamp(byte_modification_time).strftime("%Y-%m-%d %H:%M:%S")
        else:
            modification_time = os.path.getmtime(file_name)
            return 0, datetime.datetime.fromtimestamp(modification_time).strftime("%Y-%m-%d %H:%M:%S")

    except FileNotFoundError:
        return 1, "File not found."
    except Exception as e:
        return 1, f"{e}"

# Helper function to print the request/response messages
def format_print(type, request_id, service_code, file_pathname, offset, length_of_bytes, content, status, data_to_send):
    if type == 0:
        print(f"""Request Message
    Request ID: {request_id}
    Service: {service_code}
    File Pathname: {file_pathname}
    Offset: {offset}
    Length of Bytes: {length_of_bytes}
    Content: {content}""")
    else:
        print(f"""Reply
    Status: {"OK" if status == 0 else "ERROR"}
    Data: {data_to_send}""")
    
while True:
    try:
        data, address = udp_socket.recvfrom(1024)
        # print("Received message:", data, "from", address)

        request_id_in_msg = int.from_bytes(data[1:2], byteorder='big')
        service_code_in_msg = int.from_bytes(data[0:1], byteorder='big')

        status = 1
        data_to_send = "Request not serviced yet"

        # if client request has been serviced before
        if (INVOCATION_SEMANTICS == "at-most-once" and (address, request_id_in_msg) in request_history):
            print("Request has been serviced before")
            status, data_to_send = request_history[(address, request_id_in_msg)]

        # if client request for read
        elif service_code_in_msg == 1:
            # Unmarshall the received data
            message = marshalling.ReadServiceClientMessage.unmarshal(data)
            format_print(0, request_id_in_msg, message.service_code, message.file_path, message.offset, message.length_of_bytes, None, None, None)
            # Read data from file, extract requested portion of data
            status, data_to_send = read_file(message.file_path, message.offset, message.length_of_bytes)
        
        # if client request for write
        elif service_code_in_msg == 2:
            # Unmarshall the received data
            message = marshalling.WriteServiceClientMessage.unmarshal(data)
            format_print(0, request_id_in_msg, message.service_code, message.file_path, message.offset, None, message.content, None, None)
            # write data from file, return if successful or not+error
            status, data_to_send = write_file(message.file_path, message.offset, message.content)
            # Update the clients monitoring the file updates
            monitor_callback(message.file_path)

        # if client request for monitor
        elif service_code_in_msg == 3:
            # Unmarshall the received data
            message = marshalling.MonitorServiceClientMessage.unmarshal(data)
            format_print(0, request_id_in_msg, message.service_code, message.file_path, message.length_of_monitoring_interval, None, None, None, None)
            # monitor data from file, return if successful or not+error
            status, data_to_send = monitor_file(message.file_path, message.length_of_monitoring_interval, address)

        # if client request for like
        elif service_code_in_msg == 4:
            # Unmarshall the received data
            message = marshalling.LikeServiceClientMessage.unmarshal(data)
            format_print(0, request_id_in_msg, message.service_code, message.file_path, None, None, None, None, None)
            # like data from file, return if successful or not+error
            status, data_to_send = like(message.file_path, address)

        # if client request for like by
        elif service_code_in_msg == 5:
            # Unmarshall the received data
            message = marshalling.LikedByServiceClientMessage.unmarshal(data)
            format_print(0, request_id_in_msg, message.service_code, message.file_path, None, None, None, None, None)
            # like by data from file, return if successful or not+error
            status, data_to_send = like_by(message.file_path)

        # if client requests for modification time of file
        elif service_code_in_msg == 69:
            # Unmarshall the received data
            message = marshalling.TmserverServiceClientMessage.unmarshal(data)
            # print("Unmarshalled message:", message.service_code, message.file_path)
            # get modification time of file
            status, data_to_send = get_modification_time(message.file_path, message.offset)

        # Save reply history
        if INVOCATION_SEMANTICS == "at-most-once":
            request_history[(address, request_id_in_msg)] = (status,data_to_send)
        # marshall the data and send it back to the client
        format_print(1, request_id_in_msg, None, None, None, None, None, status, data_to_send)
        marshalled_data = marshalling.ServerMessage(status, data_to_send).marshal()
        udp_socket.sendto(marshalled_data, address)

    except Exception as e:
        print("Error:", e)
