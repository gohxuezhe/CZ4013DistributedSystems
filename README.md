Instructions on running:

1) if you are using 2 or more remote computers, connect to the same WiFi/hotspot

2) open 2 terminals

3) on first terminal: run server.py `python server.py`, copy the IP address printed on the terminal as that will be your server's IP address

4) on second terminal: run client.py with the necessary command-line arguments behind it `python client.py <service_called> <filename> <offset> <length_of_bytes> <content (if applicable)>`

    -service called: 'write' or 'read'

   -content: in string

    -to read: `python client.py <service_called> <filename> <offset> <length_of_bytes>`
  
    -to write: `python client.py <service_called> <filename> <offset> <length_of_bytes> <content>`

    -example: `python client.py write abc.txt 1 100 hihi`
