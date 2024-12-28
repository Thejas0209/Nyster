import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import asyncio

load_dotenv()

bot = commands.Bot(
    command_prefix='!',
    intents=nextcord.Intents.all()
)

db_github = None
db_gitlab = None

@bot.event
async def on_ready():
    """
    Sets the bot's status and activity when it is ready.
    """
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.listening,
            name="Excessive Phonk"
        ),
        status=nextcord.Status.do_not_disturb
    )
    print(f'{bot.user.name} connected to Discord')

def Getdb(DB_Name):
    """
    Establishes a connection to the MongoDB database and returns the database object.
    """
    uri =os.getenv("Mongo_DB_Url")

    try:

        client = MongoClient(uri, server_api=ServerApi('1'))

        client.admin.command('ping')
        print(f"Successfully connected to {DB_Name}!")

        db = client[DB_Name]
        return db

    except Exception as e:
        print("An error occurred while connecting to MongoDB:", e)
        raise

async def setup_db():
    """
    Initialize the database connection using the Getdb function.
    """
    global db_github, db_gitlab 
    db_github = Getdb(os.getenv("Github_Db"))
    db_gitlab = Getdb(os.getenv("Gitlab_Db"))


def load_cogs():
    """
    Dynamically loads all Python files from the 'cogs' folder as bot extensions (Cogs).
    Passes the bot instance and database connection to each cog.
    """
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # Import the cog module dynamically
            cog_name = filename[:-3]
            module = __import__(f'cogs.{cog_name}', fromlist=[cog_name])

            # Dynamically retrieve the cog class from the module
            cog_class = getattr(module, cog_name, None)

            # Ensure cog_class is valid and not None
            if cog_class is None:
                print(f"Skipping {filename} because no valid cog class was found.")
                continue  # Skip to the next file if cog_class is not found

            # Create the cog instance
            if "Github" in cog_name:
                cog = cog_class(bot, db_github)
            elif "Gitlab" in cog_name:
                cog = cog_class(bot, db_gitlab)
            else:
                cog = cog_class(bot)

            # Ensure that cog is a valid instance before attempting to add it
            if cog is not None:
                bot.add_cog(cog)
            else:
                print(f"Failed to create a valid cog instance for {filename}. Skipping...")

async def main():
    """
    Main function to initialize the bot, load extensions, and start the bot instance.
    """
    await setup_db()
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
