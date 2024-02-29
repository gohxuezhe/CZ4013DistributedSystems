Instructions on running:

-if you are using 2 or more remote computers, connect to the same WiFi/hotspot
-open 2 terminals
-on first terminal: run server.py `python server.py`, copy the IP address printed on the terminal as that will be your server's IP address
-on second terminal: run python.py with the necessary command-line arguments behind it `python client.py <service_called> <filename> <offset> <length_of_bytes> <content (if applicable)>`
  -to read: `python client.py <service_called> <filename> <offset> <length_of_bytes>`
  -to write: `python client.py <service_called> <filename> <offset> <length_of_bytes> <content>`
