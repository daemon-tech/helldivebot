import system
import discord


from dotenv import load_dotenv
from discord.ext import commands


# check config exist
config_file_path = os.path.join(os.path.dirname(__file__), "config.json")f

if os.path.isfile(config_file_path):
    with open(config_file_path) as file:
        config = json.load(file)
else:
    sys.exit('"config.json" not found!')
    
    
#load .env file
load_dotenv()


#run bot _> bot nbot yet specified
bot.run(os.getenv("TOKEN"))



"""
to-do:

listen to commands only with "x" role // start with implementing commands framework

implement api

call api data with commands:
	start with /api/{war_id}/info
"""
