def calculate_liberation_player_efficiency(health, liberation, players):
    
    # Calculate liberation progression
    liberation_progression = liberation / 100
    
    if players == 0:
        return 0  # Avoid division by zero
    
    # Calculate liberation/player efficiency
    liberation_player_efficiency = (liberation_progression / players)
    return liberation_player_efficiency

def format_efficiency(efficiency):
    # Format efficiency to make it more human-readable
    return "{:.10f}".format(efficiency)


# Calculate liberation/player efficiency
#efficiency = calculate_liberation_player_efficiency(health, liberation, players)
#print("Liberation/Player Efficiency:", efficiency)