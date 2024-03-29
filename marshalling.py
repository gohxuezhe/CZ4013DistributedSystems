# marshalling.py is used to marshal and unmarshal the data to be sent and received between the client and server.

# (read service) marshalling and unmarshalling for client msg
class ReadServiceClientMessage:
    def __init__(self, service_code, request_ID, file_path, offset, length_of_bytes):
        self.service_code = service_code
        self.request_ID = request_ID
        self.file_path = file_path
        self.offset = offset
        self.length_of_bytes = length_of_bytes

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder="big")
        request_ID_bytes = self.request_ID.to_bytes(1, byteorder="big")
        file_path_length_bytes = len(self.file_path).to_bytes(1, byteorder="big")
        file_path_bytes = self.file_path.encode("utf-8")
        offset_bytes = self.offset.to_bytes(8, byteorder="big")
        length_of_bytes_bytes = self.length_of_bytes.to_bytes(8, byteorder="big")
        # Combine encoded attributes into a byte stream
        return service_code_bytes + request_ID_bytes + file_path_length_bytes + file_path_bytes + offset_bytes + length_of_bytes_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder="big")
        request_ID = int.from_bytes(data[1:2], byteorder="big")
        file_path_length = int.from_bytes(data[2:3], byteorder="big")
        file_path = data[3:3 + file_path_length].decode("utf-8")
        offset = int.from_bytes(data[3 + file_path_length:11 + file_path_length], byteorder="big")
        length_of_bytes = int.from_bytes(data[11 + file_path_length:], byteorder="big")

        # Create a new message instance with reconstructed attributes
        return cls(service_code, request_ID, file_path, offset, length_of_bytes)


# (write service) marshalling and unmarshalling for client msg
class WriteServiceClientMessage:
    def __init__(self, service_code, request_ID, file_path, offset, content):
        self.service_code = service_code
        self.request_ID = request_ID
        self.file_path = file_path
        self.offset = offset
        self.content = content

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder="big")
        request_ID_bytes = self.request_ID.to_bytes(1, byteorder="big")
        file_path_length_bytes = len(self.file_path).to_bytes(1, byteorder="big")
        file_path_bytes = self.file_path.encode("utf-8")
        offset_bytes = self.offset.to_bytes(8, byteorder="big")
        content_bytes = self.content.encode("utf-8")
        # Combine encoded attributes into a byte stream
        return service_code_bytes + request_ID_bytes + file_path_length_bytes + file_path_bytes + offset_bytes + content_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder="big")
        request_ID = int.from_bytes(data[1:2], byteorder="big")
        file_path_length = int.from_bytes(data[2:3], byteorder="big")
        file_path = data[3:3 + file_path_length].decode("utf-8")
        offset = int.from_bytes(data[3 + file_path_length : 11 + file_path_length], byteorder="big")
        content = data[11 + file_path_length :].decode("utf-8")

        # Create a new message instance with reconstructed attributes
        return cls(service_code, request_ID, file_path, offset, content)


# (monitor service) marshalling and unmarshalling for client msg
class MonitorServiceClientMessage:
    def __init__(self, service_code, file_path, length_of_monitoring_interval):
        self.service_code = service_code
        self.file_path = file_path
        self.length_of_monitoring_interval = length_of_monitoring_interval

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder="big")
        file_path_bytes = self.file_path.encode("utf-8")
        length_of_monitoring_interval_bytes = self.length_of_monitoring_interval.to_bytes(8, byteorder="big")
        # Combine encoded attributes into a byte stream
        return service_code_bytes + len(file_path_bytes).to_bytes(1, byteorder="big") + file_path_bytes + length_of_monitoring_interval_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder="big")
        file_path_length = int.from_bytes(data[1:2], byteorder="big")
        file_path = data[2:2 + file_path_length].decode("utf-8")
        length_of_monitoring_interval = int.from_bytes(data[2 + file_path_length :], byteorder="big")

        # Create a new message instance with reconstructed attributes
        return cls(service_code, file_path, length_of_monitoring_interval)


# (like service) marshalling and unmarshalling for client msg
class LikeServiceClientMessage:
    def __init__(self, service_code, request_ID, file_path):
        self.service_code = service_code
        self.request_ID = request_ID
        self.file_path = file_path

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder="big")
        request_ID_bytes = self.request_ID.to_bytes(1, byteorder="big")
        file_path_length_bytes = len(self.file_path).to_bytes(1, byteorder="big")
        file_path_bytes = self.file_path.encode("utf-8")
        # Combine encoded attributes into a byte stream
        return service_code_bytes + request_ID_bytes + file_path_length_bytes + file_path_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder="big")
        request_ID = int.from_bytes(data[1:2], byteorder="big")
        file_path_length = int.from_bytes(data[2:3], byteorder="big")
        file_path = data[3:3 + file_path_length].decode("utf-8")

        # Create a new message instance with reconstructed attributes
        return cls(service_code, request_ID, file_path)


# (liked by service) marshalling and unmarshalling for client msg
class LikedByServiceClientMessage:
    def __init__(self, service_code, request_ID, file_path):
        self.service_code = service_code
        self.request_ID = request_ID
        self.file_path = file_path

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder="big")
        request_ID_bytes = self.request_ID.to_bytes(1, byteorder="big")
        file_path_length_bytes = len(self.file_path).to_bytes(1, byteorder="big")
        file_path_bytes = self.file_path.encode("utf-8")
        # Combine encoded attributes into a byte stream
        return service_code_bytes + request_ID_bytes + file_path_length_bytes + file_path_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder="big")
        request_ID = int.from_bytes(data[1:2], byteorder="big")
        file_path_length = int.from_bytes(data[2:3], byteorder="big")
        file_path = data[3:3 + file_path_length].decode("utf-8")

        # Create a new message instance with reconstructed attributes
        return cls(service_code, request_ID, file_path)


# (tmserver service) marshalling and unmarshalling for client msg
class TmserverServiceClientMessage:
    def __init__(self, service_code, request_ID, file_path, offset):
        self.service_code = service_code
        self.request_ID = request_ID
        self.file_path = file_path
        self.offset = offset

    def marshal(self):
        # Encode object attributes into a byte stream
        service_code_bytes = self.service_code.to_bytes(1, byteorder="big")
        request_ID_bytes = self.request_ID.to_bytes(1, byteorder="big")
        file_path_length_bytes = len(self.file_path).to_bytes(1, byteorder="big")
        file_path_bytes = self.file_path.encode("utf-8")
        offset_bytes = self.offset.to_bytes(8, byteorder="big")
        # Combine encoded attributes into a byte stream
        return service_code_bytes + request_ID_bytes + file_path_length_bytes + file_path_bytes + offset_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        service_code = int.from_bytes(data[0:1], byteorder="big")
        request_ID = int.from_bytes(data[1:2], byteorder="big")
        file_path_length = int.from_bytes(data[2:3], byteorder="big")
        file_path = data[3 : 3 + file_path_length].decode("utf-8")
        offset = int.from_bytes(data[3 + file_path_length:], byteorder="big")

        # Create a new message instance with reconstructed attributes
        return cls(service_code, request_ID, file_path, offset)

# marshalling and unmarshalling for server msgs
class ServerMessage:
    def __init__(self, status, data):
        self.status = status
        self.data = data

    def marshal(self):
        # Encode object attributes into a byte stream
        status_bytes = self.status.to_bytes(1, byteorder="big")
        data_bytes = self.data.encode("utf-8")
        # Combine encoded attributes into a byte stream
        return status_bytes + data_bytes

    @classmethod
    def unmarshal(cls, data):
        # Decode byte stream to reconstruct object attributes
        status = int.from_bytes(data[0:1], byteorder="big")
        data = data[1:].decode("utf-8")

        # Create a new message instance with reconstructed attributes
        return cls(status, data)