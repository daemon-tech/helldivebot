import requests

url = "https://helldivers-2.fly.dev/api/801/status"
response = requests.get(url)
json_data = response.json()

def alert_for_conquered_planet():
    conquered_events = []

    # Check planet attacks
    for attack in json_data['planet_attacks']:
        if attack['source']['initial_owner'] != 'Humans':
            conquered_events.append({
                'planet': attack['target']['name'],
                'conquering_entity': attack['source']['initial_owner'],
                'timestamp': attack.get('timestamp', 'Unknown timestamp')
            })

    # Check global events
    for event in json_data['global_events']:
        if event['race'] != 'Humans':
            conquered_events.append({
                'planet': event.get('title', 'Unknown planet'),
                'conquering_entity': event['race'],
                'timestamp': event.get('timestamp', 'Unknown timestamp')
            })

    # Check community targets
    for target in json_data['community_targets']:
        if target['race'] != 'Humans':
            conquered_events.append({
                'planet': target['planet'],
                'conquering_entity': target['race'],
                'timestamp': target.get('timestamp', 'Unknown timestamp')
            })

    # If no conquered events found, return appropriate message
    if not conquered_events:
        return "No conquered planet found."

    # Sort conquered events by timestamp (excluding "Unknown timestamp")
    conquered_events.sort(key=lambda x: (x['timestamp'] == 'Unknown timestamp', x['timestamp']))

    # Return details of the earliest conquered planet
    earliest_event = conquered_events[0]
    print(f"Planet {earliest_event['planet']} got conquered by {earliest_event['conquering_entity']} at {earliest_event['timestamp']}!")
    return f"Planet {earliest_event['planet']} got conquered by {earliest_event['conquering_entity']} at {earliest_event['timestamp']}!"
