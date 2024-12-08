import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import asyncio


load_dotenv()

# Initialize the bot with the desired command prefix and intents
bot = commands.Bot(
    command_prefix='!',  
    intents=nextcord.Intents.all()  
)

@bot.event
async def on_ready():
    """
    Sets the bot's status and activity when it is ready.
    This method is triggered automatically after the bot successfully connects to Discord.
    """
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.listening,  
            name="Excessive Phonk"  
        ),
        status=nextcord.Status.do_not_disturb  
    )
    print(f'{bot.user.name} connected to Discord')  


def load_cogs():
    """
    Dynamically loads all Python files from the 'cogs' folder as bot extensions (Cogs).
    Each file in the folder must define a valid Cog class.
    """
    for filename in os.listdir('./cogs'):  
        if filename.endswith('.py'):  
            bot.load_extension(f'cogs.{filename[:-3]}')  


async def main():
    """
    Main function to initialize the bot, load extensions, and start the bot instance.
    The bot token is retrieved from environment variables.
    """
    load_cogs()  
    await bot.start(os.getenv('Discord_Token')) 


if __name__ == "__main__":
    """
    Run the bot using asyncio. Handles cleanup and shutdown on manual interruption.
    """
    try:
        asyncio.run(main()) 
    except KeyboardInterrupt:  
        print("Bot has been stopped manually.")
