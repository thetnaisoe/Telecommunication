# Question / Answer Application

This is a simple Question / Answer application where clients attempt to guess a number chosen by the server. The server can serve multiple clients simultaneously and uses a TCP connection for communication. The client uses a logarithmic search algorithm to guess the number.

## Requirements

- Python 3.x
- `struct` module (part of Python's standard library)
- The client and server scripts communicate via TCP.

## Game Flow

1. **Server:**
   - The server listens for incoming connections and chooses a random integer between 1 and 100.
   - For each client, the server will guide them through the guessing process by responding to their guesses.
   - The server uses the `SELECT` function to serve multiple clients concurrently.

2. **Client:**
   - The client guesses the number using logarithmic search.
   - The client will continue the guessing process based on the server's responses:
     - `>` indicates the guessed number is too low.
     - `<` indicates the guessed number is too high.
     - `=` indicates the guess is correct.
   - The client will disconnect upon receiving one of the following messages:
     - `Y` (Win): The client has correctly guessed the number.
     - `K` (Quit): The client opts to quit.
     - `V` (End): The game has ended.

3. **Message Format:**
   - **Client Message:** `(char, integer)` where the `char` represents the comparison operator (`<`, `>`, `=`) and the `integer` is the guessed number.
     - Example: `('>', 10)` meaning the guessed number is greater than 10.
   - **Server Message:** Same format as client message, but the integer is irrelevant.
     - `I` means "Yes", `N` means "No", `K` means "Quit", `Y` means "Win", `V` means "End".
     - Example: `('V', 0)` means the game has ended.

## Script Usage

To start the server and client, use the following commands:

1. **Start the server**:
   ```bash
   python3 server.py <hostname> <port number>
