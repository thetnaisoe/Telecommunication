import json
import sys

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    
#print(load_json(sys.argv[1]))

def initialize_network(data):
    links = {}
    for link in data['links']:
        points = tuple(link['points'])
        capacity = link['capacity']
        links[points] = {'capacity': capacity, 'usage': 0}
    return links

#print(initialize_network(load_json(sys.argv[1])))

def find_path(possible_circuits, start, end):
    for path in possible_circuits:
        if path[0] == start and path[-1] == end:
            return path
    return None

def can_allocate_demand(links, path, demand):
    for i in range(len(path)-1):
        link = (path[i], path[i+1])
        if links[link]['usage'] +  demand > links[link]['capacity']:
            return False
    return True

def allocate_demand(links, path, demand):
    for i in range(len(path)-1):
        link = (path[i], path[i+1])
        links[link]['usage'] += demand

def deallocate_demand(links, path, demand):
    for i in range(len(path) - 1):
        link = (path[i], path[i + 1])
        links[link]['usage'] -= demand

def simulate(data):
    links = initialize_network(data)
    possible_circuits = data['possible-circuits']
    events = []
    current_demands = {}

    for time in range(1, data['simulation']['duration']+1):
        for demand in data['simulation']['demands']:
            start,end = demand['end-points']
            if time == demand['start-time']:
                path = find_path(possible_circuits, start, end)
                if path and can_allocate_demand(links, path, demand['demand']):
                    allocate_demand(links, path, demand['demand'])
                    current_demands[(start, end)] = path
                    events.append(f"{len(events) + 1}. demand allocation: {start}<->{end} st:{time} – successful")
                else:
                    events.append(f"{len(events) + 1}. demand allocation: {start}<->{end} st:{time} – unsuccessful")
            if time == demand['end-time'] and (start, end) in current_demands:
                path = current_demands.pop((start, end))
                deallocate_demand(links, path, demand['demand'])
                events.append(f"{len(events) + 1}. demand deallocation: {start}<->{end} st:{time}")
    return events

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 client.py cs1.json")
        return

    filename = sys.argv[1]
    data = load_json(filename)
    events = simulate(data)

    for event in events:
        print(event)

if __name__ == "__main__":
    main()





