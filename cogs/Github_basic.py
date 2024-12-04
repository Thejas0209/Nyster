import nextcord
from nextcord.ext import commands
from github import Github
from DBConnect import Getdb

class GithubBasic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = Getdb("GithubDB")
        self.github_token = None
        self.github_client = None
        
    # Display Repository Information
    @nextcord.slash_command(name="github-repo-info", description="Display repository information")
    async def github_repo_info(self, interaction: nextcord.Interaction, repo: str):
        """Display information about a specific GitHub repository."""
        try:
            # Fetch the GitHub token from the database
            user_record = self.DB["UserInfo"].find_one({"user": interaction.user.name})
            if not user_record or "Token" not in user_record:
                await interaction.response.send_message("GitHub token not found. Please set up your token using /github-setup.")
                return
            
            self.github_token = user_record["Token"]
            self.github_client = Github(self.github_token)
            
            # Fetch repository details
            repository = self.github_client.get_repo(repo)
            
            # Create an embed for repository details
            embed = nextcord.Embed(
                title=f"{repository.name} - GitHub Repository Info",
                description=repository.description or "No description provided.",
                color=nextcord.Color.gold(),
                timestamp=interaction.created_at
            )
            embed.set_thumbnail(url=repository.owner.avatar_url)
            embed.add_field(name="Owner", value=repository.owner.login, inline=True)
            embed.add_field(name="Stars", value=repository.stargazers_count, inline=True)
            embed.add_field(name="Forks", value=repository.forks_count, inline=True)
            
            languages = repository.get_languages()
            embed.add_field(
                name="Languages", 
                value=", ".join(languages.keys()) if languages else "No languages detected.", 
                inline=False
            )
            embed.add_field(name="Clone URL", value=repository.clone_url, inline=False)
            embed.add_field(name="Created On", value=repository.created_at.strftime("%Y-%m-%d"), inline=True)

            # Send the embed as a response
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Command failed with error: {str(e)}")

# Async setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(GithubBasic(bot))
