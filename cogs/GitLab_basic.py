import nextcord
from nextcord.ext import commands
from gitlab import Gitlab
from DBConnect import Getdb

class GitlabBasic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = Getdb("GitlabDB")
        self.gitlab_client = None

    # Display Repository Information
    @nextcord.slash_command(name="gitlab-repo-info", description="Display repository information")
    async def gitlab_repo_info(self, interaction: nextcord.Interaction, repo: str):
        """Display information about a specific GitLab repository."""
        try:
            # Fetch the GitLab token from the database
            user_record = self.DB["UserInfo"].find_one({"user": interaction.user.name})
            if not user_record or "Token" not in user_record:
                await interaction.response.send_message("GitLab token not found. Please set up your token.")
                return

            self.gitlab_token = user_record["Token"]
            self.gitlab_client = Gitlab(private_token=self.gitlab_token)

            # Fetch repository details
            project = self.gitlab_client.projects.get(repo)

            # Create an embed for repository details
            embed = nextcord.Embed(
                title=f"{project.name} - GitLab Repository Info",
                description=project.description or "No description provided.",
                color=nextcord.Color.gold(),
                timestamp=interaction.created_at
            )
            embed.set_thumbnail(url=project.avatar_url or "https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png")
            embed.add_field(name="Owner", value=project.owner["username"], inline=True)
            embed.add_field(name="Stars", value=project.star_count, inline=True)
            embed.add_field(name="Forks", value=project.forks_count, inline=True)
            embed.add_field(name="Clone URL", value=project.http_url_to_repo, inline=False)
            embed.add_field(name="Created On", value=project.created_at[:10], inline=True)

            # Send the embed as a response
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"Command failed with error: {str(e)}")

# Async setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(GitlabBasic(bot))
