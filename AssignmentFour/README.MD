# NetCopy Client/Server Application

This project implements a client/server application that enables transferring files and verifying the transferred data using CRC or MD5 checksums. The system is composed of three main components:

1. **Checksum Server**
2. **NetCopy Client**
3. **NetCopy Server**

Each component is detailed below with instructions on usage and operation.

---

## 1. Checksum Server

### Description
The Checksum Server handles storing and querying checksum data for file transfers. It operates using a simple text-based protocol to store and retrieve quadruplets of the form:

`(file identifier, checksum length, checksum, expiration (in seconds))`

### Protocol Details

#### Insert Message
**Format:**
```
ON|<file_id>|<validity_in_seconds>|<checksum_length>|<checksum_bytes>
```

**Example:**
```
ON|1237671|60|12|abcdefabcdef
```
- File ID: `1237671`
- Validity: `60` seconds
- Checksum Length: `12` bytes
- Checksum: `abcdefabcdef`

**Response:**
```
OK
```

#### Take Out Message
**Format:**
```
OFF|<file_id>
```

**Example:**
```
OFF|1237671
```
- Requesting checksum for file ID `1237671`

**Response:**
```
<checksum_length>|<checksum_bytes>
```
**Example Response:**
```
12|abcdefabcdef
```
If no checksum exists:
```
0|
```

### Running the Checksum Server
To start the server:
```
python3 checksum_srv.py <ip> <port>
```
- `<ip>`: Server address (e.g., `localhost`)
- `<port>`: Port to bind the server

The server runs in an infinite loop, supports multiple clients, and communicates over TCP. Expired checksums are removed upon the next request.

---

## 2. NetCopy Client

### Description
The NetCopy Client transfers files to the NetCopy Server. During or after the transfer, it calculates an MD5 checksum of the file and uploads it to the Checksum Server.

### Workflow
1. Connects to the NetCopy Server at the specified address and port.
2. Transfers the file byte by byte.
3. Computes an MD5 checksum for the file.
4. Uploads the checksum along with the file identifier to the Checksum Server.
5. Disconnects and exits.

### Running the NetCopy Client
To run the client:
```
python3 netcopy_cli.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <file_id> <file_path>
```
- `<srv_ip>`: NetCopy Server IP address
- `<srv_port>`: NetCopy Server port
- `<chsum_srv_ip>`: Checksum Server IP address
- `<chsum_srv_port>`: Checksum Server port
- `<file_id>`: Integer identifier for the file
- `<file_path>`: Path to the file to transfer

---

## 3. NetCopy Server

### Description
The NetCopy Server receives files from the NetCopy Client, saves them to disk, and verifies their integrity using the Checksum Server.

### Workflow
1. Waits for a client to connect.
2. Receives the transferred file bytes and saves them to the specified location.
3. Requests the MD5 checksum for the file identifier from the Checksum Server.
4. Verifies the correctness of the transferred file by comparing the computed checksum with the received checksum.
5. Prints the result of the verification to the standard output.

### Running the NetCopy Server
To start the server:
```
python3 netcopy_srv.py <ip> <port> <file_id> <output_file>
```
- `<ip>`: Server address (e.g., `localhost`)
- `<port>`: Port to bind the server
- `<file_id>`: Integer identifier for the file
- `<output_file>`: Path to save the received file

---

## Example Workflow
1. Start the Checksum Server:
   ```
   python3 checksum_srv.py localhost 5000
   ```

2. Start the NetCopy Server:
   ```
   python3 netcopy_srv.py localhost 6000 1237671 received_file.txt
   ```

3. Run the NetCopy Client to transfer a file:
   ```
   python3 netcopy_cli.py localhost 6000 localhost 5000 1237671 input_file.txt
   ```

4. Verify the result in the NetCopy Server's standard output.

---

## Notes
- Ensure all components can communicate over the specified IP addresses and ports.
- Use unique file identifiers for each file transfer.
- Checksum expiration is set to 60 seconds by default.

---

## License
This project is released under the MIT License.
