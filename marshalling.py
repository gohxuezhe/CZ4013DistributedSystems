# marshalling.py
 
# (read service) marshalling and unmarshalling for client msg
class read_service_client_message:
    def __init__(self, service_code, file_path, offset, length_of_bytes):
        self.service_code = service_code
        self.file_path = file_path
        self.offset = offset
        self.length_of_bytes = length_of_bytes

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        offset_bytes = self.offset.to_bytes(8, byteorder='big')
        length_of_bytes_bytes = self.length_of_bytes.to_bytes(8, byteorder='big')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes + offset_bytes + length_of_bytes_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1],byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')
        offset = int.from_bytes(data[2 + file_path_length:10 + file_path_length], byteorder='big')
        length_of_bytes = int.from_bytes(data[10 + file_path_length:], byteorder='big')

        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path, offset, length_of_bytes)

# (read service) marshalling and unmarshalling for server msg
class read_service_server_message:
    def __init__(self, file_data):
        self.file_data = file_data

    def marshal(self):
        # Encode object attributes into a byte stream
        file_data_bytes = self.file_data.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return len(file_data_bytes).to_bytes(1, byteorder='big') + file_data_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        file_data_length = int.from_bytes(data[0:1], byteorder='big')
        file_data = data[1:1 + file_data_length].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(file_data)
    
# (write service) marshalling and unmarshalling for client msg
class write_service_client_message:
    def __init__(self, service_code, file_path, offset, content):
        self.service_code = service_code
        self.file_path = file_path
        self.offset = offset
        self.content = content

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        offset_bytes = self.offset.to_bytes(8, byteorder='big')
        content_bytes = self.content.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes + offset_bytes + content_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')
        offset = int.from_bytes(data[2 + file_path_length:10 + file_path_length], byteorder='big')
        content = data[10 + file_path_length:].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path, offset, content)

# (write service) marshalling and unmarshalling for server msg
class write_service_server_message:
    def __init__(self, file_data):
        self.file_data = file_data

    def marshal(self):
        # Encode object attributes into a byte stream
        file_data_bytes = self.file_data.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return len(file_data_bytes).to_bytes(1, byteorder='big') + file_data_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        file_data_length = int.from_bytes(data[0:1], byteorder='big')
        file_data = data[1:1 + file_data_length].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(file_data)
    
# (tmserver service) marshalling and unmarshalling for client msg
class tmserver_service_client_message:
    def __init__(self, service_code, file_path):
        self.service_code = service_code
        self.file_path = file_path

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder='big')
        file_path_bytes = self.file_path.encode('utf-8')
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder='big') + file_path_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder='big')
        file_path_length = int.from_bytes(data[1:2], byteorder='big')
        file_path = data[2:2 + file_path_length].decode('utf-8')

        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path)

# (tmserver service) marshalling and unmarshalling for server msg
class tmserver_service_server_message:
    def __init__(self, Tmserver):
        self.Tmserver = Tmserver

    def marshal(self):
        # Encode object attributes into a byte stream
        Tmserver_bytes = self.Tmserver.to_bytes(8, byteorder='big')
        # Combine encoded attributes into a byte stream
        return Tmserver_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        Tmserver = int.from_bytes(data, byteorder='big')

        # Create a new message instance with reconstructed attributes
        return cls(Tmserver)