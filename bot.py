import os
import requests
import discord
import json
import asyncio
import datetime


from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands, tasks

#clear terminal
os.system("clear")

# check config exist
config_file_path = os.path.join(os.path.dirname(__file__), "config.json")

if os.path.isfile(config_file_path):
	with open(config_file_path) as file:
		config = json.load(file)
else:
	os.system.exit('"config.json" not found!')


# Initialize the bot
bot = commands.Bot(command_prefix=";", intents=discord.Intents.all())


# Function to generate the embed with current time
def generate_time_embed():
    # Get current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create an embed
    #embed = discord.Embed(title="Current Time", description=f"The current time is: {current_time}", color=discord.Color.blue())
    
    return current_time

# Define a function to fetch data from the API
def fetch_data_from_api(endpoint):
	try:
		response = requests.get(f'https://helldivers-2.fly.dev{endpoint}')
		response.raise_for_status()  # Raise an error for bad responses (status code >= 400)
		return response.json()
	except requests.RequestException as e:
		print(f"Error fetching data from API: {e}")
		return None

#test server connection
def api_server_test():
	try:
		response = requests.get("https://helldivers-2.fly.dev")
		response.raise_for_status()
		ok = "ok"
		return ok, print(f"Console: raise_for_status: {ok}")

	except requests.RequestException as e:
		print(f"Error fetching data from API: {e}")
		error_api = "error"
		return error_api, print(f"Console: raise_for_status: {error_api}")

#format players decimals
def format_players(players):
    if players >= 1000000:  # Greater than or equal to 1 million
        return f"{players // 1000000}.{players % 1000000 // 100000}M"
    elif players >= 1000:   # Greater than or equal to 1 thousand
        return f"{players // 1000}.{players % 1000 // 100}k"
    else:
        return str(players)

#validate emoji for attack/defend/ etc from the config
def validate_war(i):
    data = fetch_data_from_api("/api/801/status")
    if data['planet_status'][i]['planet']['initial_owner'] == 'Terminids':
        if data['planet_status'][i]['owner'] == 'Terminids':
            return f"{config['emojis']['terminid']} {config['emojis']['attack']}"
        else:
            return f"{config['emojis']['terminid']} {config['emojis']['defend']}"
    
    elif data['planet_status'][i]['planet']['initial_owner'] == 'Automaton':
        if data['planet_status'][i]['owner'] == 'Automaton':
            return f"{config['emojis']['automaton']} {config['emojis']['attack']}"
        else:
            return f"{config['emojis']['automaton']} {config['emojis']['defend']}"
    
    else:
        if data['planet_status'][i]['owner'] == 'Humans':
            return f"{config['emojis']['humans']} {config['emojis']['defend']}"
        else:
            return f"{config['emojis']['humans']} {config['emojis']['attack']}"

#fetch id's from config
channelid = config['server_channel_id']
serverid = config['server_id']


#command sync
@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == int(config['daemon']):
        try:
            s = await bot.tree.sync()
            print(f'Synced {len(s)} commands')
            await ctx.send('BOT: Synced!')
        except Exception as e:
            print(f'Error syncing commands: {e}')
    else:
        await ctx.send('You must be the owner to use this command!')

previous_message = None

#define embed content
def generate_content():
    
    data = fetch_data_from_api("/api/801/status")
    data_event = fetch_data_from_api("/api/801/events")
        
    if data:
        embed = discord.Embed(title=":ringed_planet: Current War Intel :ringed_planet:", color=discord.Color.blue())
        
        #superearth messages 
        for i in range(0, len(data_event)):
            embed.add_field(name=f"Superearth Message {i+1}:", value=f"{data_event[i]['message']['en']}", inline=False)
            embed.add_field(name=" ", value=" ", inline=False)
            
        
        # Add fields for different parts of the data
        for i in range(0, len(data['planet_status'])):
            
            
            #var init for post if
            liberation_as_int = int(float(data['planet_status'][i]['liberation']))
            liberation_formated = "{:.2f}".format(liberation_as_int)
            players_formatted = format_players(data['planet_status'][i]['players'])
            
            
            #check if war between 100 < target > 0
            if data['planet_status'][i]['liberation'] < 100 and data['planet_status'][i]['liberation'] > 0:
                embed.add_field(name="Planet:", value=f"{validate_war(i)} {data['planet_status'][i]['planet']['name']}", inline=True)
                embed.add_field(name="Liberation:", value=f"{liberation_formated}% ", inline=True)
                embed.add_field(name="Players:", value=f"{players_formatted}", inline=True)
                embed.add_field(name="", value=" ", inline=False)

        
        embed.add_field(name="Updated:", value=generate_time_embed(), inline=True)
        print(f"Updated: {generate_time_embed()}")
        #embed.add_field(name="War ID of the first Galactic War:", value=fetch_data_from_api("/api/801/info")['war_id'], inline=True)
        
        return embed

print("DEBUG: loop task")
@tasks.loop(minutes=6)
async def check_for_updates(channel_id):
    try:
        global previous_message
    
        # Get the channel object
        channel = bot.get_channel(channel_id)
        if channel is None:
            print(f"Error: Channel with ID {channel_id} not found.")
            return
    
        # Generate the current embed content
        current_embed_content = generate_content()
    
        # Check if there's a previous message to edit
        if previous_message:
            # Edit the previous message with the updated embed
            try:
                await previous_message.edit(embed=current_embed_content)
                print("Console: Updated [Current War Intel]")
            except discord.NotFound:
                print("Error: Previous message not found.")
            except discord.Forbidden:
                print("Error: Bot does not have permission to edit the message.")
        else:
            # Send a new message with the embed and store it as the previous message
            try:
                previous_message = await channel.send(embed=current_embed_content)
            except discord.Forbidden:
                print("Error: Bot does not have permission to send messages in this channel.")
    except:
        print("DEBUG: ERROR in checkforupdates")
        pass

# Slash command to retrieve status from the API
@bot.tree.command(name="warstatus", description="Fetch War Status")
async def warstatus(interaction: discord.Interaction):
    if interaction.channel_id == channelid:
        
        data = fetch_data_from_api("/api/801/status")
        data_event = fetch_data_from_api("/api/801/events")
        
        if data:
            embed = discord.Embed(title=":ringed_planet: Current War Intel :ringed_planet:", color=discord.Color.blue())
        
            #superearth messages 
            for i in range(0, len(data_event)):
                embed.add_field(name=f"Superearth Message {i+1}:", value=f"{data_event[i]['message']['en']}", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
            
        
            # Add fields for different parts of the data
            for i in range(0, len(data['planet_status'])):
            
            
                #var init for post if
                liberation_as_int = int(float(data['planet_status'][i]['liberation']))
                liberation_formated = "{:.2f}".format(liberation_as_int)
                players_formatted = format_players(data['planet_status'][i]['players'])
            
            
                #check if war between 100 < target > 0
                if data['planet_status'][i]['liberation'] < 100 and data['planet_status'][i]['liberation'] > 0:
                        embed.add_field(name="Planet:", value=f"{validate_war(i)} {data['planet_status'][i]['planet']['name']}", inline=True)
                        embed.add_field(name="Liberation:", value=f"{liberation_formated}% ", inline=True)
                        embed.add_field(name="Players:", value=f"{players_formatted}", inline=True)
                        embed.add_field(name="", value=" ", inline=False)

        
            embed.add_field(name="Updated:", value=generate_time_embed(), inline=True)
            print(f"Updated: {generate_time_embed()}")
            #embed.add_field(name="D-0 of the first Galactic War:", value=fetch_data_from_api("/api/801/info")['start_date'], inline=True)
            #embed.add_field(name="War ID of the first Galactic War:", value=fetch_data_from_api("/api/801/info")['war_id'], inline=True)
            
            await interaction.response.send_message(embed=embed)
            print(f"Console: interaction.response.send_message(embed=embed) -> warstatus")
        else:
            await interaction.response.send_message("Failed to fetch data from the API. Please wait a bit")
    else:
        print(f"Console: /warstatus is not allowed to be read and pasted in current channel id: {interaction.channel_id}")


# Event handler for bot startup
@bot.event
async def on_ready():
    print('Console: Bot is ready!')
    print("----------------------------------------------------")
    game = discord.Game("Superearth Office")
    check_for_updates.start(channelid)
    await bot.change_presence(status=discord.Status.idle, activity=game)

#load .env file / run bot
load_dotenv()
bot.run(os.getenv("TOKEN"))