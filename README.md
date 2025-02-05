# CP373 - Computer Networks, Winter 2025
# Socket Programming Assignment 
This assignment implements a simple client-server communication application. 

Clients are able to:
1. Connect to server
2. Send messages to the server as input. These messages include:
   - “exit”, which will terminate the connection with the server and close the client
   - “status”, which will ask the server for the contents of the cache
   - “list”, which will ask the server for a list of files stored in the server repository
   - “get <filename>”, which will ask the server to stream the contents of a file
   - any string using the Command Line Interface.

The server is able to:
1. Handle a limited number of clients. Currently, the limit is hard coded as 3.
2. Connect with a client and assign them a specific name in the form of [“Client” + an incrementing number starting with 01], along with the dates and times when the connection was established and ended.
3. Respond to messages sent from the clients. These messages include:
   - “exit”, which will save the date and time when this client disconnects
   - “status”, which will send the contents of the cache to the client
   - “list”, which will send the contents of the repository to the client
   - “get <filename>”, which will attempt to stream the contents of a repository file to the client, or return an error message if the file cannot be found
   - any string using the Command Line Interface, which will “echo” the string back to the client, along with the word “ACK” appended to the message.
