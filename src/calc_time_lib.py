def calculate_time_to_liberate(liberation, regen_per_second):
    
    liberation = float(liberation)
    regen_per_second = float(regen_per_second)
    
    print(liberation, regen_per_second)
    
    remaining_liberation = 100 - liberation
    liberation_per_second = regen_per_second
    
    #print(f"liberation in seconds: " + {liberation_per_second})
    
    if liberation_per_second == 0:
        return "Liberation not progressing"
    
    print(f"{remaining_liberation} / {liberation_per_second} = {remaining_liberation / liberation_per_second}")
    
    time_to_liberate_seconds = remaining_liberation / liberation_per_second  # Calculate time to liberate in seconds
    time_to_liberate_hours = time_to_liberate_seconds / 3600  # Convert to hours#
    
    print("Remaining liberation:", remaining_liberation)
    print("{} {} hours".format("Time: ",time_to_liberate_hours))
    print("-----------------")
    
    return "{:.2f} hours".format(time_to_liberate_hours)

'''# Example usage:
planet_status = {
    "health": 924222,
    "liberation": 7.577799999999996,
    "owner": "Terminids",
    "planet": {
        "disabled": False,
        "hash": 2875368439,
        "index": 125,
        "initial_owner": "Terminids",
        "max_health": 1000000,
        "name": "Fenrir III",
        "position": {"x": 46.994886, "y": 27.418607},
        "sector": "20",
        "waypoints": [64, 168]
    },
    "players": 36780,
    "regen_per_second": 4.1666665
}'''

#time_to_liberate = calculate_time_to_liberate(planet_status)
#print("Time to fully liberate the planet:", time_to_liberate)



