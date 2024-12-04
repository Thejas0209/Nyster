import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Create a bot instance with the command prefix "!"
bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all())

# Event to indicate when the bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="Excessive Phonk"),
        status=nextcord.Status.do_not_disturb
    )
    print(f'{bot.user.name} connected to Discord')

# Function to load Cogs from the "cogs" folder
def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

# Main function to run the bot
async def main():
    load_cogs()  
    await bot.start(os.getenv('Discord_Token'))

# Run the main function
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot has been stopped manually.")
