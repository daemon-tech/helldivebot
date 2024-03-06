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


#fetch id's from config
channel_id = config['server_channel_id']
server_id = config['server_id']

guild = discord.Object(id=server_id) if server_id else None

# Event handler for bot startup
@bot.event
async def on_ready():
    print('Console: Bot is ready!')

#command sync
@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 250648489220898817:
        try:
            s = await bot.tree.sync()
            print(f'Synced {len(s)} commands')
            await ctx.send('BOT: Synced!')
        except Exception as e:
            print(f'Error syncing commands: {e}')
    else:
        await ctx.send('You must be the owner to use this command!')
        
# Slash command to retrieve data from the API
@bot.tree.command(name="warstatus", description="Fetch War Status")
async def warstatus(interaction: discord.Interaction):
    data = fetch_data_from_api("/api/801/status")
    if data:
        embed = discord.Embed(title="War Status", color=discord.Color.green())
        for key, value in data.items():
            embed.add_field(name=key, value=value, inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Failed to fetch data from the API.")

#load .env file / run bot
load_dotenv()
bot.run(os.getenv("TOKEN"))