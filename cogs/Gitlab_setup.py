import nextcord
from nextcord.ext import commands
import os 
from dotenv import load_dotenv
load_dotenv()

class Gitlab_setup(commands.Cog):
    """
    A Cog for managing GitLab token setup.
    Provides commands to set up, check, and remove GitLab tokens for a user.
    """

    def __init__(self, bot, db):
        """
        Initializes the Gitlab_setup Cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
        self.db= db
        self.gitlab_token = None
        self.gitlab_client = None
        self.collection = self.db[os.getenv("Table_users")]

    @nextcord.slash_command(name="gitlab-setup", description="Collects your GitLab token for usage")
    async def gitlab_setup(self, interaction: nextcord.Interaction, git_token: str):
        """
        Stores the user's GitLab token in the database.

        Args:
            interaction (nextcord.Interaction): The interaction context.
            git_token (str): The user's GitLab token.
        """
        try:
            self.collection.insert_one({"user": interaction.user.name, "Token": git_token})
            await interaction.response.send_message("Your setup is successful.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Error with setup.", ephemeral=True)
            print(e)

    @nextcord.slash_command(name="gitlab-status", description="Display Setup status")
    async def gitlab_setup_status(self, interaction: nextcord.Interaction):
        """
        Displays the setup status for the user's GitLab token.

        Args:
            interaction (nextcord.Interaction): The interaction context.
        """
        try:
            result = self.collection.find_one({"user": interaction.user.name})
            if result and result.get('Token'):
                await interaction.response.send_message("Your setup is complete, and you are eligible to use GitLab commands.")
            else:
                await interaction.response.send_message("You haven't set up your GitLab token. Please use /gitlab-setup to set it up.")
        except Exception as e:
            await interaction.response.send_message("Error trying to fetch details.", ephemeral=True)

    @nextcord.slash_command(name="gitlab-setup-remove", description="Remove your information if you no longer plan to use GitLab commands")
    async def gitlab_setup_remove(self, interaction: nextcord.Interaction):
        """
        Removes the user's GitLab token information from the database.

        Args:
            interaction (nextcord.Interaction): The interaction context.
        """
        try:
            result = self.collection.delete_one({"user": interaction.user.name})
            if result.deleted_count == 1:
                await interaction.response.send_message("Your GitLab token information has been removed.", ephemeral=True)
            else:
                await interaction.response.send_message("Your GitLab token information does not exist in our records.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Error with setup.", ephemeral=True)
            print(e)
def setup(bot,db):
    bot.add_cog(Gitlab_setup(bot,db))