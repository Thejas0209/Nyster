import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()

# Create a bot instance with the command prefix "!"
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

# Event to indicate when the bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Excessive Phonk"),status=discord.Status.do_not_disturb)
    print(f'{bot.user.name} connected to discord')
    await bot.tree.sync()

# Function to load Cogs from the "cogs" folder
async def load_commands():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

# Main function to run the bot
async def main():
    async with bot:
        await load_commands()
        await bot.start(os.getenv('Discord_Token'))

# Run the main function
asyncio.run(main())