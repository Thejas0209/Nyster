import nextcord
from nextcord.ext import commands, tasks
from github import Github

from DBConnect import Getdb

class Github_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB=Getdb()
        self.collection=self.DB["UserInfo"]

    @nextcord.slash_command(name="git-setup", description="Collects your github token for usage")
    async def git_setup(self, interaction: nextcord.Interaction, git_token: str):
        """Display information about a specific GitHub repository."""
        try:
            result=self.collection.insert_one({"user":interaction.user.name,"Token":git_token})
            await interaction.response.send_message("ho ho setup complete",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Error with setup",ephemeral=True)
            print(e)
        
    @nextcord.slash_command(name="git-status", description="Display Setup status")
    async def git_setup_status(self, interaction: nextcord.Interaction):
        """Display information about a specific GitHub repository."""
        try:
            result=self.collection.find_one({"user":interaction.user.name})
            if result['Token']:
                await interaction.response.send_message("Ur setup is complete and you are eligible to use the git commands")
            else:
                await interaction.response.send_message("You haven't setup your git-token for accessing ur github please use /git-setup and set it")
        except Exception as e:
            await interaction.response.send_message("Error trying to fetch details",ephemeral=True)
    
    @nextcord.slash_command(name="git-setup-remove", description="Remove your Information if u do not plan to use this commands anymore")
    async def git_setup_remove(self, interaction: nextcord.Interaction):
        """Display information about a specific GitHub repository."""
        try:
            result=self.collection.delete_one({"user":interaction.user.name})
            if result.deleted_count==1:
                await interaction.response.send_message("Your git token information has been removed",ephemeral=True)
            else:
                await interaction.response.send_message("Your git token information does not exist with us",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Error with setup",ephemeral=True)
            print(e)
# Async setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(Github_setup(bot))
