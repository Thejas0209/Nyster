import nextcord
from nextcord.ext import commands, tasks
from github import Github
import os
from dotenv import load_dotenv
from DBConnect import Getdb

load_dotenv()

class Github_commits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = Getdb()  # Connect to the MongoDB database
        self.commits_trackers_collection = self.DB["CommitTracker"]  # Collection for tracking commit information
        self.github_token = None
        self.github_client = None
        self.check_new_commits.start()  # Start the periodic task

    async def get_github_token(self, user_name):
        """Fetch the GitHub token from the database for the given user."""
        user_info = self.DB["UserInfo"].find_one({"user": user_name})
        if user_info and "Token" in user_info:
            return user_info["Token"]
        else:
            raise ValueError("GitHub token not found for the user.")

    async def set_github_client(self, user_name):
        """Set the GitHub client using the token from the database."""
        self.github_token = await self.get_github_token(user_name)
        self.github_client = Github(self.github_token)

    # Fetch Latest Commits
    @nextcord.slash_command(name="git-commits", description="Fetches last 5 commits on the repository")
    async def commits(self, interaction: nextcord.Interaction, repo: str):
        """Fetch the latest commits from a GitHub repository."""
        try:
            await self.set_github_client(interaction.user.name)  # Ensure the client is set
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

    @nextcord.slash_command(name="git-track-commits", description="Sends last 5 commits of a repo every 5 mins")
    async def git_track_commits(self, interaction: nextcord.Interaction, repo: str, channel: nextcord.TextChannel):
        try:
            await self.set_github_client(interaction.user.name)  # Ensure the client is set
            # Check if the repo is already being tracked
            existing_entry = self.commits_trackers_collection.find_one({"repo": repo})
            if existing_entry:
                await interaction.response.send_message(f"Already tracking `{repo}`.")
                return

            # Add the repo to the commit trackers collection
            self.commits_trackers_collection.insert_one({
                "repo": repo,
                "channel_id": channel.id
            })
            await interaction.response.send_message(f"Now tracking commits for `{repo}` in {channel.mention}.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to set up commit tracking: {str(e)}")

    @tasks.loop(minutes=5)
    async def check_new_commits(self):
        try:
            # Iterate through the commit trackers collection
            for entry in self.commits_trackers_collection.find():
                repo = entry["repo"]
                channel_id = entry["channel_id"]
                await self.set_github_client("some_default_user")  # Replace with appropriate user if needed
                
                # Fetch the repository and its commits
                repository = self.github_client.get_repo(repo)
                commits = repository.get_commits()
                
                if commits.totalCount == 0:
                    continue  # Skip if no commits are found

                commit_messages = [
                    f"🔹 {commit.commit.message} by {commit.commit.author.name}" 
                    for commit in commits[:5]
                ]

                # Send the latest commit messages to the specified channel
                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(
                        f"Here are the latest updates on `{repo}`:\n" + "\n".join(commit_messages)
                    )
        except Exception as e:
            print(f"Error posting commits: {e}")

    @check_new_commits.before_loop
    async def before_check_new_commits(self):
        await self.bot.wait_until_ready()

# Async setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(Github_commits(bot))
