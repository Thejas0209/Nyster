import nextcord
from nextcord.ext import commands, tasks
from github import Github
import os
from dotenv import load_dotenv
load_dotenv()

class Github_commits(commands.Cog):
    """
    A Cog that provides GitHub commit tracking and fetching functionality.
    Allows users to fetch the latest commits, track commit updates periodically, 
    and stop tracking repositories.
    """

    def __init__(self, bot, db):
        """
        Initializes the Github_commits Cog.

        Args:
            bot (commands.Bot): The bot instance to which this Cog belongs.
        """
        self.bot = bot
        self.db = db 
        self.commits_trackers_collection = self.db[os.getenv("Table_commits_trackers")]  
        self.github_token = None
        self.github_client = None
        self.check_new_commits.start()  

    async def get_github_token(self, user_name):
        """
        Fetches the GitHub token for the specified user from the database.

        Args:
            user_name (str): The username to fetch the token for.

        Returns:
            str: The GitHub token.

        Raises:
            ValueError: If no token is found for the user.
        """
        user_info = self.db[os.getenv("Table_users")].find_one({"user": user_name})
        if user_info and "Token" in user_info:
            return user_info["Token"]
        else:
            raise ValueError("GitHub token not found for the user.")

    async def set_github_client(self, user_name):
        """
        Sets the GitHub client using the token fetched for the specified user.

        Args:
            user_name (str): The username for which to set the client.
        """
        self.github_token = await self.get_github_token(user_name)
        self.github_client = Github(self.github_token)

    @nextcord.slash_command(name="github-commits", description="Fetches last 5 commits on the repository")
    async def github_commits(self, interaction: nextcord.Interaction, repo: str):
        """
        Fetches the latest 5 commits from a specified GitHub repository.

        Args:
            interaction (nextcord.Interaction): The interaction context from the user.
            repo (str): The full name of the repository (e.g., "owner/repo").
        """
        try:
            await self.set_github_client(interaction.user.name)
            repository = self.github_client.get_repo(repo)
            commits = repository.get_commits()
            commit_messages = [
                f"🔹 {commit.commit.message} by {commit.commit.author.name}" 
                for commit in commits[:5]
            ]
            await interaction.response.send_message(
                f"Here are the latest updates on `{repo}`:\n" + "\n".join(commit_messages)
            )
        except Exception as e:
            await interaction.response.send_message(f"Failed to fetch commits: {str(e)}")

    @nextcord.slash_command(name="github-track-commits", description="Sends last 5 commits of a repo every 5 mins")
    async def github_track_commits(self, interaction: nextcord.Interaction, repo: str, channel: nextcord.TextChannel):
        """
        Sets up tracking for a repository's latest commits and sends updates periodically.

        Args:
            interaction (nextcord.Interaction): The interaction context from the user.
            repo (str): The full name of the repository.
            channel (nextcord.TextChannel): The Discord channel to send updates to.
        """
        try:
            await self.set_github_client(interaction.user.name)
            existing_entry = self.commits_trackers_collection.find_one({"repo": repo})
            if existing_entry:
                await interaction.response.send_message(f"Already tracking `{repo}`.")
                return

            self.commits_trackers_collection.insert_one({
                "repo": repo,
                "channel_id": channel.id,
                "user": interaction.user.name
            })
            await interaction.response.send_message(f"Now tracking commits for `{repo}` in {channel.mention}.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to set up commit tracking: {str(e)}")

    @tasks.loop(hours=1)
    async def check_new_commits(self):
        """
        Periodically checks for new commits in tracked repositories and sends updates to the respective channels.
        """
        try:
            for entry in self.commits_trackers_collection.find():
                repo = entry["repo"]
                channel_id = entry["channel_id"]
                user = entry["user"]
                await self.set_github_client(user)

                repository = self.github_client.get_repo(repo)
                commits = repository.get_commits()

                if commits.totalCount == 0:
                    continue

                commit_messages = [
                    f"🔹 {commit.commit.message} by {commit.commit.author.name}" 
                    for commit in commits[:5]
                ]

                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(
                        f"Here are the latest updates on `{repo}`:\n" + "\n".join(commit_messages)
                    )
        except Exception as e:
            print(f"Error posting commits: {e}")

    @nextcord.slash_command(name="github-untrack-commits", description="Stop tracking new commits for a repository")
    async def github_untrack_commits(self, interaction: nextcord.Interaction, repo: str):
        """
        Stops tracking commit updates for a specified repository.

        Args:
            interaction (nextcord.Interaction): The interaction context from the user.
            repo (str): The full name of the repository.
        """
        result = self.commits_trackers_collection.delete_one({"repo": repo})
        if result.deleted_count > 0:
            await interaction.response.send_message(f"Stopped tracking new commits for `{repo}`.")
        else:
            await interaction.response.send_message(f"`{repo}` is not currently being tracked.")

    @check_new_commits.before_loop
    async def before_check_new_commits(self):
        """
        Ensures the bot is ready before starting the periodic task.
        """
        await self.bot.wait_until_ready()

def setup(bot,db):
    bot.add_cog(Github_commits(bot,db))