import socket
import os
import time
import marshalling
import datetime
from collections import defaultdict

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

monitor_dict = defaultdict(list)

udp_socket.bind((ip_address, 12345))
print("Server listening on", ip_address, "port 12345")

# Read content from file function
def read_file(file_name, offset, length):
    try:
        with open(file_name, "r") as file:
            # Move to the specified offset
            file.seek(offset)
            # Read the specified length of bytes
            data = file.read(length)
            return data
    except FileNotFoundError:
        return "(Error) File not found."
    except IOError:
        return "(Error) Unable to read the file."
    except ValueError:
        return "(Error) Invalid offset or length."
    except Exception as e:
        return f"(Error) {e}"

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

        return f"Successful write to {file_name} at offset {offset}"
    except Exception as e:
        return f"(Error) {e}"

# Monitor file (add to monitor_dict)
def monitor_file(file_name, length_of_monitoring_interval, address):
    try:
        with open(file_name, "r") as file:
            pass

        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(minutes=length_of_monitoring_interval)
        
        current_time_fmt = current_time.strftime("%H:%M:%S")
        end_time_fmt = end_time.strftime("%H:%M:%S")

        monitor_dict[file_name].append((address, end_time))

        return f"Client ({address}) is monitoring {file_name} for {length_of_monitoring_interval}min from {current_time_fmt} to {end_time_fmt}"
    except FileNotFoundError:
        return "(Error) File not found."
    except Exception as e:
        return f"(Error) {e}"

# Update monitoring clients about file updates, and update monitor_dict to remove clients who are no longer monitoring
def monitor_callback(file_name):
    for address, end_time in monitor_dict[file_name]:
        current_time = datetime.datetime.now()
        new_monitor_list = []

        if current_time <= end_time:
            # Read the whole file
            data_to_send = read_file(file_name, 0, -1)
            # Send the whole file to the monitoring client
            marshalled_data = marshalling.MonitorCallbackServiceServerMessage(data_to_send).marshal()
            udp_socket.sendto(marshalled_data, address)
            new_monitor_list.append((address, end_time))

        monitor_dict[file_name] = new_monitor_list

# Get modification time of file
def get_modification_time(file_name):
    try:
        modification_time = os.path.getmtime(file_name)
        return modification_time
    except FileNotFoundError:
        return "(Error) File not found."
    except Exception as e:
        return f"(Error) {str(e)}"
    
while True:
    try:
        data, address = udp_socket.recvfrom(1024)
        print("Received message:", data, "from", address)

        service_code_in_msg = int.from_bytes(data[0:1], byteorder='big')

        # if client request for read
        if service_code_in_msg == 1:
            # Unmarshal the received data
            message = marshalling.ReadServiceClientMessage.unmarshal(data)
            print("Unmarshalled message:", message.service_code, message.file_path, message.offset, message.length_of_bytes)
            # Read data from file, extract requested portion of data
            data_to_send = read_file(message.file_path, message.offset, message.length_of_bytes)
            # Marshal the data and send it back to the client
            marshalled_data = marshalling.ReadServiceServerMessage(data_to_send).marshal()
            udp_socket.sendto(marshalled_data, address)
        
        # if client request for write
        elif service_code_in_msg == 2:
            # Unmarshal the received data
            message = marshalling.WriteServiceClientMessage.unmarshal(data)
            print("Unmarshalled message:", message.service_code, message.file_path, message.offset, message.content)
            # write data from file, return if successful or not+error
            data_to_send = write_file(message.file_path, message.offset, message.content)
            # Marshal the data and send it back to the client
            marshalled_data = marshalling.WriteServiceServerMessage(data_to_send).marshal()
            udp_socket.sendto(marshalled_data, address)
            # Update the clients monitoring the file updates
            monitor_callback(message.file_path)

        # if client request for monitor
        elif service_code_in_msg == 3:
            # Unmarshal the received data
            message = marshalling.MonitorServiceClientMessage.unmarshal(data)
            print("Unmarshalled message:", message.service_code, message.file_path, message.length_of_monitoring_interval)
            # monitor data from file, return if successful or not+error
            data_to_send = monitor_file(message.file_path, message.length_of_monitoring_interval, address)
            # Marshal the data and send it back to the client
            marshalled_data = marshalling.MonitorServiceServerMessage(data_to_send).marshal()
            udp_socket.sendto(marshalled_data, address)

        # if client requests for modification time of file
        elif service_code_in_msg == 69:
            # Unmarshal the received data
            message = marshalling.TmserverServiceClientMessage.unmarshal(data)
            print("Unmarshalled message:", message.service_code, message.file_path)
            # get modification time of file
            modification_time = get_modification_time(message.file_path)
            # Marshal the modification time and send it back to the client
            marshalled_data = marshalling.TmserverServiceServerMessage(modification_time).marshal()
            udp_socket.sendto(marshalled_data, address)

    except Exception as e:
        print("Error:", e)

udp_socket.close()
