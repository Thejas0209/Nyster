import nextcord
from nextcord.ext import commands, tasks
from github import Github
import os
from dotenv import load_dotenv

load_dotenv()
from DBConnect import Getdb

class Gitlab_basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB=Getdb()
        self.gitlab_token = os.getenv("Gitlab_token")
        self.gitlab_client = None
        
    # Display Repository Information
    @nextcord.slash_command(name="gitlab-repo-info", description="Display repository information")
    async def gitlab_repo_info(self, interaction: nextcord.Interaction, repo: str):
        """Display information about a specific Gitlab repository."""
        self.github_token=self.DB["UserInfo"].find_one({"user":interaction.user.name})["Token"]
        self.github_client=Github(self.github_token)
        try:
            repository = self.github_client.get_repo(repo)
            embed = nextcord.Embed(
                title=f"{repository.name} - GitLab Repository Info",
                description=repository.description or "No description provided.",
                color=nextcord.Color.gold(),
                timestamp=interaction.created_at
            )
            embed.set_thumbnail(url=repository.owner.avatar_url)
            embed.add_field(name="Owner", value=repository.owner.login, inline=True)
            embed.add_field(name="Stars", value=repository.stargazers_count, inline=True)
            embed.add_field(name="Forks", value=repository.forks_count, inline=True)
            embed.add_field(name="Languages", value=", ".join(repository.get_languages().keys()), inline=False)
            embed.add_field(name="Clone URL", value=repository.clone_url, inline=False)
            embed.add_field(name="Created On", value=repository.created_at.strftime("%Y-%m-%d"), inline=True)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Command failed with error: {str(e)}")
            
# Async setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(Gitlab_basic(bot))