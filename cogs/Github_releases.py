import nextcord
from nextcord.ext import commands, tasks
from github import Github
import os 
from dotenv import load_dotenv
load_dotenv()

class Github_releases(commands.Cog):
    """
    A Cog to track and notify about new releases on GitHub repositories.
    Provides commands to set up tracking, stop tracking, and a periodic task
    to check for new releases.
    """

    def __init__(self, bot, db):
        """
        Initializes the Github_releases Cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
        self.db= db
        self.github_token = None
        self.github_client = None
        self.release_trackers_collection = self.db[os.getenv("Table_releases_trackers")] 
        self.check_new_releases.start()  

    async def get_github_token(self, user_name):
        """
        Fetches the GitHub token for the given user from the database.

        Args:
            user_name (str): The username of the GitHub token owner.

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
    
    @nextcord.slash_command(name="github-track-releases", description="Set up notifications for new releases on a repository")
    async def github_track_releases(self, interaction: nextcord.Interaction, repo: str, channel: nextcord.TextChannel):
        """
        Sets up tracking for new releases from a GitHub repository.

        Args:
            interaction (nextcord.Interaction): The interaction context.
            repo (str): The full repository name (e.g., "owner/repo").
            channel (nextcord.TextChannel): The channel to send notifications to.
        """
        try:
            self.github_token = await self.get_github_token(interaction.user.name)
            self.github_client = Github(self.github_token)

            # Check if the repository is already being tracked
            existing_entry = self.release_trackers_collection.find_one({"repo": repo})
            if existing_entry:
                await interaction.response.send_message(f"Already tracking `{repo}`.")
                return

            # Insert tracking information into the database
            self.release_trackers_collection.insert_one({
                "repo": repo,
                "channel_id": channel.id,
                "user": interaction.user.name,
                "last_release_id": None
            })

            await interaction.response.send_message(f"Now tracking new releases for `{repo}` in {channel.mention}.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to set up release tracking: {str(e)}")

    @tasks.loop(minutes=1)
    async def check_new_releases(self):
        """
        Periodically checks for new releases in tracked repositories and sends notifications.
        """
        for entry in self.release_trackers_collection.find():
            try:
                repo = entry["repo"]
                channel_id = entry["channel_id"]
                last_release_id = entry.get("last_release_id")
                user = entry.get("user")

                self.github_token = await self.get_github_token(user)
                self.github_client = Github(self.github_token)
                repository = self.github_client.get_repo(repo)

                releases = repository.get_releases()
                if releases.totalCount == 0:
                    continue

                latest_release = releases[0]
                if last_release_id != latest_release.id:
                    # Update the last release ID in the database
                    self.release_trackers_collection.update_one(
                        {"repo": repo},
                        {"$set": {"last_release_id": latest_release.id}}
                    )
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        await channel.send(
                            f"🎉 New release in `{repo}`: **{latest_release.title}**\n"
                            f"{latest_release.html_url}\n\n"
                            f"{latest_release.body or 'No description provided.'}"
                        )
            except Exception as e:
                print(f"Error checking releases for {repo}: {e}")

    @check_new_releases.before_loop
    async def before_check_new_releases(self):
        """
        Ensures the bot is ready before starting the periodic release check.
        """
        await self.bot.wait_until_ready()

    @nextcord.slash_command(name="github-untrack-releases", description="Stop tracking new releases for a repository")
    async def github_untrack_releases(self, interaction: nextcord.Interaction, repo: str):
        """
        Stops tracking new releases for a specified repository.

        Args:
            interaction (nextcord.Interaction): The interaction context.
            repo (str): The full repository name (e.g., "owner/repo").
        """
        result = self.release_trackers_collection.delete_one({"repo": repo})
        if result.deleted_count > 0:
            await interaction.response.send_message(f"Stopped tracking new releases for `{repo}`.")
        else:
            await interaction.response.send_message(f"`{repo}` is not currently being tracked.")
            
def setup(bot,db):
    bot.add_cog(Github_releases(bot,db))