# marshalling.py
 
# (read service) marshalling and unmarshalling for client msg
class ReadServiceClientMessage:
    def __init__(self, service_code, file_path, offset, length_of_bytes):
        self.service_code = service_code
        self.file_path = file_path
        self.offset = offset
        self.length_of_bytes = length_of_bytes

    def marshall(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        offset_bytes = self.offset.to_bytes(8, byteorder='big')
        length_of_bytes_bytes = self.length_of_bytes.to_bytes(8, byteorder='big')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes + offset_bytes + length_of_bytes_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1],byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')
        offset = int.from_bytes(data[2 + file_path_length:10 + file_path_length], byteorder='big')
        length_of_bytes = int.from_bytes(data[10 + file_path_length:], byteorder='big')

        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path, offset, length_of_bytes)

# (read service) marshalling and unmarshalling for server msg
class ReadServiceServerMessage:
    def __init__(self, file_data):
        self.file_data = file_data

    def marshall(self):
        # Encode object attributes into a byte stream
        file_data_bytes = self.file_data.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return len(file_data_bytes).to_bytes(1, byteorder='big') + file_data_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        file_data_length = int.from_bytes(data[0:1], byteorder='big')
        file_data = data[1:1 + file_data_length].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(file_data)
    
# (write service) marshalling and unmarshalling for client msg
class WriteServiceClientMessage:
    def __init__(self, service_code, file_path, offset, content):
        self.service_code = service_code
        self.file_path = file_path
        self.offset = offset
        self.content = content

    def marshall(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        offset_bytes = self.offset.to_bytes(8, byteorder='big')
        content_bytes = self.content.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes + offset_bytes + content_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')
        offset = int.from_bytes(data[2 + file_path_length:10 + file_path_length], byteorder='big')
        content = data[10 + file_path_length:].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path, offset, content)

# (write service) marshalling and unmarshalling for server msg
class WriteServiceServerMessage:
    def __init__(self, file_data):
        self.file_data = file_data

    def marshall(self):
        # Encode object attributes into a byte stream
        file_data_bytes = self.file_data.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return len(file_data_bytes).to_bytes(1, byteorder='big') + file_data_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        file_data_length = int.from_bytes(data[0:1], byteorder='big')
        file_data = data[1:1 + file_data_length].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(file_data)

# (monitor service) marshalling and unmarshalling for client msg
class MonitorServiceClientMessage:
    def __init__(self, service_code, file_path, length_of_monitoring_interval):
        self.service_code = service_code
        self.file_path = file_path
        self.length_of_monitoring_interval = length_of_monitoring_interval

    def marshall(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        length_of_monitoring_interval_bytes = self.length_of_monitoring_interval.to_bytes(8, byteorder='big')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes + length_of_monitoring_interval_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1],byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')
        length_of_monitoring_interval = int.from_bytes(data[2 + file_path_length:], byteorder='big')

        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path, length_of_monitoring_interval)

# (monitor service) marshalling and unmarshalling for server msg
class MonitorServiceServerMessage:
    def __init__(self, file_data):
        self.file_data = file_data

    def marshall(self):
        # Encode object attributes into a byte stream
        file_data_bytes = self.file_data.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return len(file_data_bytes).to_bytes(1, byteorder='big') + file_data_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        file_data_length = int.from_bytes(data[0:1], byteorder='big')
        file_data = data[1:1 + file_data_length].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(file_data)

# (monitor callback service) marshalling and unmarshalling for server msg
class MonitorCallbackServiceServerMessage:
    def __init__(self, file_data):
        self.file_data = file_data

    def marshall(self):
        # Encode object attributes into a byte stream
        file_data_bytes = self.file_data.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return len(file_data_bytes).to_bytes(1, byteorder='big') + file_data_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        file_data_length = int.from_bytes(data[0:1], byteorder='big')
        file_data = data[1:1 + file_data_length].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(file_data)
    
# (like service) marshalling and unmarshalling for client msg
class LikeServiceClientMessage:
    def __init__(self, service_code, file_path):
        self.service_code = service_code
        self.file_path = file_path
    
    def marshall(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes
    
    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')
        
        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path)
    
# (like service) marshalling and unmarshalling for server msg
class LikeServiceServerMessage:
    def __init__(self, like_status):
        self.like_status = like_status
    
    def marshall(self):
        # Encode object attributes into a byte stream
        like_status_bytes = self.like_status.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return like_status_bytes
    
    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        like_status = data.decode('utf-8')
        # Create a new message instance with reconstructed attributes
        return cls(like_status)
    
# (liked by service) marshalling and unmarshalling for client msg
class LikedByServiceClientMessage:
    def __init__(self, service_code, file_path):
        self.service_code = service_code
        self.file_path = file_path
    
    def marshall(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes
    
    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')
        
        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path)
    
# (liked by service) marshalling and unmarshalling for server msg
class LikedByServiceServerMessage:
    def __init__(self, liked_by):
        self.liked_by = liked_by
    
    def marshall(self):
        # Encode object attributes into a byte stream
        liked_by_bytes = self.liked_by.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return len(liked_by_bytes).to_bytes(1, byteorder='big') + liked_by_bytes
    
    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        liked_by_length = int.from_bytes(data[0:1], byteorder='big')
        liked_by = data[1:1 + liked_by_length].decode('utf-8')
        
        # Create a new message instance with reconstructed attributes
        return cls(liked_by)
    
# (tmserver service) marshalling and unmarshalling for client msg
class TmserverServiceClientMessage:
    def __init__(self, service_code, file_path, offset):
        self.service_code = service_code
        self.file_path = file_path
        self.offset = offset

    def marshall(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        offset_bytes = self.offset.to_bytes(8, byteorder='big')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes + offset_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')
        offset = int.from_bytes(data[2+file_path_length:], byteorder='big')

        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path, offset)

# (tmserver service) marshalling and unmarshalling for server msg
class TmserverServiceServerMessage:
    def __init__(self, modification_time):
        self.modification_time = modification_time

    def marshall(self):
        # Convert modification_time to integer
        modification_time_int = int(self.modification_time)
        # Encode modification_time into a byte stream
        modification_time_bytes = modification_time_int.to_bytes(8, byteorder='big')
        # Combine encoded attributes into a byte stream
        return modification_time_bytes

    @classmethod
    def unmarshall(cls, data):
        # Decode byte stream to reconstruct modification_time
        modification_time = int.from_bytes(data, byteorder='big')

        # Create a new message instance with reconstructed attributes
        return cls(modification_time)