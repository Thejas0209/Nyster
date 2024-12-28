import nextcord
from nextcord.ext import commands
from github import Github
import os 
from dotenv import load_dotenv
load_dotenv()


class Github_basic(commands.Cog):
    """
    A Cog that provides GitHub integration commands for fetching and displaying repository information.
    """

    def __init__(self, bot, db):
        """
        Initializes the GithubBasic Cog.

        Args:
            bot (commands.Bot): The bot instance to which this Cog belongs.
        """
        self.bot = bot
        self.db = db
        self.github_token = None
        self.github_client = None

    @nextcord.slash_command(name="github-repo-info", description="Display repository information")
    async def github_repo_info(self, interaction: nextcord.Interaction, repo: str):
        """
        Slash command to display information about a specific GitHub repository.

        Args:
            interaction (nextcord.Interaction): The interaction context from the user.
            repo (str): The full name of the repository (e.g., "owner/repo").
        """
        try:
            user_record = self.db[os.getenv("Table_users")].find_one({"user": interaction.user.name})
            if not user_record or "Token" not in user_record:
                await interaction.response.send_message("GitHub token not found. Please set up your token using /github-setup.")
                return

            self.github_token = user_record["Token"]
            self.github_client = Github(self.github_token)
            repository = self.github_client.get_repo(repo)

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

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Command failed with error: {str(e)}")

# Setup function should be outside the class
def setup(bot, db):
    bot.add_cog(Github_basic(bot, db))
