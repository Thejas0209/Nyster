import nextcord
from nextcord.ext import commands, tasks

from DBConnect import Getdb

class Github_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB=Getdb("GithubDB")
        self.collection=self.DB["UserInfo"]

    @nextcord.slash_command(name="github-setup", description="Collects your github token for usage")
    async def github_setup(self, interaction: nextcord.Interaction, git_token: str):
        """Display information about a specific GitHub repository."""
        try:
            result=self.collection.insert_one({"user":interaction.user.name,"Token":git_token})
            await interaction.response.send_message("Setup Sucessfull ",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Error with setup",ephemeral=True)
            print(e)
        
    @nextcord.slash_command(name="github-status", description="Display Setup status")
    async def github_setup_status(self, interaction: nextcord.Interaction):
        """Display information about a specific GitHub repository."""
        try:
            result=self.collection.find_one({"user":interaction.user.name})
            if result['Token']:
                await interaction.response.send_message("Your setup is complete and you are eligible to use the git commands")
            else:
                await interaction.response.send_message("You haven't setup your github-token for accessing ur github please use /git-setup and set it")
        except Exception as e:
            await interaction.response.send_message("Error trying to fetch details",ephemeral=True)
    
    @nextcord.slash_command(name="github-setup-remove", description="Remove your Information if u do not plan to use this commands anymore")
    async def github_setup_remove(self, interaction: nextcord.Interaction):
        """Display information about a specific GitHub repository."""
        try:
            result=self.collection.delete_one({"user":interaction.user.name})
            if result.deleted_count==1:
                await interaction.response.send_message("Your github token information has been removed",ephemeral=True)
            else:
                await interaction.response.send_message("Your github token information does not exist with us",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Error with setup",ephemeral=True)
            print(e)
# Async setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(Github_setup(bot))
