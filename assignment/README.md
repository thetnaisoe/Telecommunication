# Circuit Simulation

## Project Overview
This project simulates the allocation and release of resources based on the topology, capacities, and demands specified in a JSON file.

## Features
- Simulates resource allocation and release.
- Supports custom topologies and demands defined in JSON format.
- Provides detailed logs of simulation events with timestamps and statuses.

## Requirements
The following Python libraries are required to run the project:
```
python 3.x
json
```
Install dependencies using:
```
pip install -r requirements.txt
```

## File Structure
- **client.py** - Main script for running the simulation.
- **cs1.json** - Example JSON file defining topology, capacities, and demands.
- **README.md** - Documentation for the project.

## Usage
1. Run the program with a JSON input file:
```
python3 client.py cs1.json
```
2. The output logs events in the following format:
```
event number. < event name >: < node1 > <-> < node2 > st:< simulation time > [- < successful/failed >]
```
Example Output:
```
1. demand reservation: A<->C st:1 - successful
2. demand reservation: B<->C st:2 - successful
3. demand release: A<->C st:5
4. demand reservation: D<->C st:6 - successful
5. demand reservation: A<->C st:7 - unsuccessful
```

## Submission
Submit the program via the TMS system in .zip format, including **client.py** and any required resources.

## Authors
- [Your Name]

## License
This project is licensed under the MIT License - see the LICENSE file for details.

