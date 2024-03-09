import os
import requests
import discord
import json
import datetime

from dotenv import load_dotenv
from discord.ext import commands, tasks
#from src.event_handler_log import *

# Load configuration from config.json
config_file_path = "config.json"
if os.path.isfile(config_file_path):
    with open(config_file_path) as file:
        config = json.load(file)
else:
    exit('"config.json" not found!')

# Initialize Discord bot
bot = commands.Bot(command_prefix=";", intents=discord.Intents.all())

# Function to fetch data from the API
def fetch_data_from_api(endpoint):
    try:
        response = requests.get(f'https://helldivers-2.fly.dev{endpoint}')
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

# Function to format player counts
def format_players(players):
    if players >= 1000000:  
        return f"{players // 1000000}.{players % 1000000 // 100000}M"
    elif players >= 1000:   
        return f"{players // 1000}.{players % 1000 // 100}k"
    else:
        return str(players)

# Function to validate emoji for attack/defend based on config
def validate_war(i):
    data = fetch_data_from_api("/api/801/status")
    planet_status = data.get('planet_status', [])
    if planet_status:
        planet = planet_status[i]['planet']
        initial_owner = planet.get('initial_owner')
        owner = planet_status[i]['owner']
        emojis = config.get('emojis', {})
        if initial_owner == 'Terminids':
            return f"{emojis.get('terminid', '')} {emojis.get('attack', '')}" if owner == 'Terminids' else f"{emojis.get('terminid', '')} {emojis.get('defend', '')}"
        elif initial_owner == 'Automaton':
            return f"{emojis.get('automaton', '')} {emojis.get('attack', '')}" if owner == 'Automaton' else f"{emojis.get('automaton', '')} {emojis.get('defend', '')}"
        else:
            return f"{emojis.get('humans', '')} {emojis.get('defend', '')}" if owner == 'Humans' else f"{emojis.get('humans', '')} {emojis.get('attack', '')}"
    else:
        return ""

# Function to generate the embed with current time
def generate_time_embed():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time

# Initializing for check_for_updates
previous_message = None

# Task to check for updates and send to a channel
@tasks.loop(minutes=6)
async def check_for_updates(channel_id):
    try:
        global previous_message
        channel = bot.get_channel(channel_id)
        if channel is None:
            print(f"Error: Channel with ID {channel_id} not found.")
            return

        current_embed_content = generate_content()
        if previous_message:
            try:
                await previous_message.edit(embed=current_embed_content)
                print("Console: Updated [Current War Intel]")
            except (discord.NotFound, discord.Forbidden) as e:
                print(f"Error: {e}")
        else:
            try:
                previous_message = await channel.send(embed=current_embed_content)
            except discord.Forbidden:
                print("Error: Bot does not have permission to send messages in this channel.")
    except Exception as e:
        print(f"DEBUG: ERROR in check_for_updates - {e}")

# Function to generate the embed content
def generate_content():
    data = fetch_data_from_api("/api/801/status")
    data_event = fetch_data_from_api("/api/801/events")
    if data:
        embed = discord.Embed(title=":ringed_planet: Current War Intel :ringed_planet:", color=discord.Color.blue())
        for i in range(0, len(data_event)):
            embed.add_field(name=f"Superearth Message {i+1}:", value=f"{data_event[i]['message']['en']}", inline=False)
            embed.add_field(name=" ", value=" ", inline=False)

        for i in range(0, len(data.get('planet_status', []))):
            if 100 > data['planet_status'][i]['liberation'] > 0:
                embed.add_field(name="Planet:", value=f"{validate_war(i)} {data['planet_status'][i]['planet']['name']}", inline=True)
                embed.add_field(name="Liberation:", value=f"{data['planet_status'][i]['liberation']:.2f}%", inline=True)
                embed.add_field(name="Players:", value=f"{format_players(data['planet_status'][i]['players'])}", inline=True)
                embed.add_field(name="", value=" ", inline=False)

        embed.add_field(name="Updated:", value=generate_time_embed(), inline=True)
        return embed
    else:
        return None

# Slash command to retrieve status from the API
@bot.command(name="warstatus", description="Fetch War Status")
async def warstatus(ctx):
    if ctx.channel.id == config['server_channel_id']:
        embed_content = generate_content()
        if embed_content:
            await ctx.send(embed=embed_content)
            print(f"Console: Sent embed message for /warstatus")
        else:
            await ctx.send("Failed to fetch data from the API. Please wait a bit")
    else:
        print(f"Console: /warstatus is not allowed in this channel: {ctx.channel.id}")

# Event handler for bot startup
@bot.event
async def on_ready():
    print('Console: Bot is ready!')
    print("----------------------------------------------------")
    game = discord.Game("Superearth Office")
    check_for_updates.start(config['server_channel_id'])
    await bot.change_presence(status=discord.Status.idle, activity=game)

# Load .env file and run the bot
load_dotenv()
bot.run(os.getenv("TOKEN"))
