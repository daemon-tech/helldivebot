import discord
import asyncio
import aiohttp

'''
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
'''

#bot = discord.Bot(intents=intents)

API_ENDPOINT = "https://helldivers-2.fly.dev/api/801/planets/{}/status"
PLANET_IDS = [1, 2, 3]  # Replace with the actual planet IDs you want to monitor

# This event is triggered when the bot is ready and connected to Discord
'''
@bot.event
async def on_ready():
    print('Bot is ready.')
    # Start polling the API for updates
    await poll_api_for_updates()
'''

async def poll_api_for_updates():
    while True:
        await asyncio.sleep(600)  # Polling interval (e.g., every 10 minutes)
        for planet_id in PLANET_IDS:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_ENDPOINT.format(planet_id)) as response:
                    if response.status == 200:
                        data = await response.json()
                        owner = data.get('owner', None)
                        if owner is not None and owner != previous_owners[planet_id]:
                            handle_planet_status_update(planet_id, owner)
                            previous_owners[planet_id] = owner

async def handle_planet_status_update(planet_id, new_owner):
    # Your logic to handle planet status updates goes here
    # Update your war log, trigger events, etc.
    print(f"Planet {planet_id} has been conquered by {new_owner}!")