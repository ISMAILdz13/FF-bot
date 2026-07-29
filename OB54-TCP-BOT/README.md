# OB54-TCP-BOT

TCP bot module for Free Fire — handles direct socket communication with Garena game servers.

## Features
- TCP connection to whisper + online servers
- AES-256 encrypted packet communication
- Protobuf message construction and parsing
- Room join/leave operations
- Emote sending
- Player info queries

## Files
| File | Purpose |
|------|---------|
| `main.py` | Main bot logic and command handler |
| `server.js` | Express.js server for running the Python bot |
| `byte.py` | Byte-level packet utilities |
| `xC4.py` | Encryption module (AES) |
| `xHeaders.py` | HTTP header construction |
| `xKEys.py` | Key generation utilities |
| `xPARA.py` | Parameter construction |
| `room_join_pb2.py` | Room join protobuf |
| `AccountPersonalShow_pb2.py` | Player info protobuf |
| `Pb2/` | Compiled protobuf definitions |

## Usage
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for server.js)
npm install

# Run via Node.js server
node server.js

# Or run Python directly
python main.py
```

## Author
ISMAILdz13

## License
MIT
