import nextcord
from nextcord.ext import commands
from gitlab import Gitlab
import os 
from dotenv import load_dotenv
load_dotenv()

class Gitlab_basic(commands.Cog):
    """
    A Cog for interacting with GitLab repositories.
    Provides commands to fetch and display repository information.
    """

    def __init__(self, bot, db):
        """
        Initializes the GitlabBasic Cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
        self.db= db
        self.gitlab_token = None
        self.gitlab_client = None

    @nextcord.slash_command(name="gitlab-repo-info", description="Display repository information")
    async def gitlab_repo_info(self, interaction: nextcord.Interaction, repo: str):
        """
        Fetches and displays information about a specific GitLab repository.

        Args:
            interaction (nextcord.Interaction): The interaction context.
            repo (str): The repository path (e.g., "owner/repo").
        """
        try:
            user_record = self.db[os.getenv("Table_users")].find_one({"user": interaction.user.name})
            if not user_record or "Token" not in user_record:
                await interaction.response.send_message("GitLab token not found. Please set up your token using the setup command.")
                return

            self.gitlab_token = user_record["Token"]
            self.gitlab_client = Gitlab(private_token=self.gitlab_token)
            repository = self.gitlab_client.projects.get(repo)

            embed = nextcord.Embed(
                title=f"{repository.name} - GitLab Repository Info",
                description=repository.description or "No description provided.",
                color=nextcord.Color.gold(),
                timestamp=interaction.created_at
            )
            embed.set_thumbnail(
                url=repository.avatar_url or "https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png"
            )
            embed.add_field(name="Owner", value=repository.owner["username"], inline=True)
            embed.add_field(name="Stars", value=repository.star_count, inline=True)
            embed.add_field(name="Forks", value=repository.forks_count, inline=True)
            embed.add_field(name="Clone URL", value=repository.http_url_to_repo, inline=False)
            embed.add_field(name="Created On", value=repository.created_at[:10], inline=True)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"Command failed with error: {str(e)}")


def setup(bot,db):
    bot.add_cog(Gitlab_basic(bot,db))