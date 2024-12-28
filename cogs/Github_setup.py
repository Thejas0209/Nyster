import nextcord
from nextcord.ext import commands
import os 
from dotenv import load_dotenv
load_dotenv()

class Github_setup(commands.Cog):
    """
    A Cog for managing GitHub token setup for bot commands.
    Provides commands to set up, check, and remove GitHub tokens for users.
    """

    def __init__(self, bot, db):
        """
        Initializes the Github_setup Cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
        self.db= db  
        self.github_token = None
        self.github_client = None
        self.collection = self.db[os.getenv("Table_users")] 

    @nextcord.slash_command(name="github-setup", description="Collects your GitHub token for usage.")
    async def github_setup(self, interaction: nextcord.Interaction, git_token: str):
        """
        Collects and stores the user's GitHub token for bot commands.

        Args:
            interaction (nextcord.Interaction): The interaction context.
            git_token (str): The GitHub token provided by the user.
        """
        try:
            self.collection.insert_one({"user": interaction.user.name, "Token": git_token})
            await interaction.response.send_message("Setup successful.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Error during setup.", ephemeral=True)
            print(e)

    @nextcord.slash_command(name="github-status", description="Display setup status.")
    async def github_setup_status(self, interaction: nextcord.Interaction):
        """
        Displays the setup status of the user's GitHub token.

        Args:
            interaction (nextcord.Interaction): The interaction context.
        """
        try:
            result = self.collection.find_one({"user": interaction.user.name})
            if result and "Token" in result:
                await interaction.response.send_message(
                    "Your setup is complete. You are eligible to use the Git commands."
                )
            else:
                await interaction.response.send_message(
                    "You haven't set up your GitHub token. Please use /github-setup to set it up."
                )
        except Exception as e:
            await interaction.response.send_message("Error fetching setup details.", ephemeral=True)
            print(e)

    @nextcord.slash_command(name="github-setup-remove", description="Remove your GitHub setup information.")
    async def github_setup_remove(self, interaction: nextcord.Interaction):
        """
        Removes the user's GitHub token information from the database.

        Args:
            interaction (nextcord.Interaction): The interaction context.
        """
        try:
            result = self.collection.delete_one({"user": interaction.user.name})
            if result.deleted_count == 1:
                await interaction.response.send_message(
                    "Your GitHub token information has been removed.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Your GitHub token information does not exist in the database.", ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message("Error during removal.", ephemeral=True)
            print(e)


def setup(bot,db):
    bot.add_cog(Github_setup(bot,db))