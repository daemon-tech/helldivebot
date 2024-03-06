import os
import requests
import discord
import json


from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

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
channel_id = config['server_channel_id']
server_id = config['server_id']

# Event handler for bot startup
@bot.event
async def on_ready():
    print('Console: Bot is ready!')

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
        
# Slash command to retrieve status from the API
@bot.tree.command(name="warstatus", description="Fetch War Status")
async def warstatus(interaction: discord.Interaction):
    data = fetch_data_from_api("/api/801/status")
    if data:
        embed = discord.Embed(title=":ringed_planet: Planet Status :ringed_planet:", color=discord.Color.blue())
        
        # Add fields for different parts of the data
        for i in range(len(data['planet_status'])):
            
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
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Failed to fetch data from the API. Please wait a bit")

#load .env file / run bot
load_dotenv()
bot.run(os.getenv("TOKEN"))