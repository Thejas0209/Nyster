import nextcord
from nextcord.ext import commands, tasks
from github import Github
from DBConnect import Getdb

class Github_releases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = Getdb()  # Assuming Getdb() connects to your MongoDB database
        self.release_trackers_collection = self.DB["ReleaseTrackers"]  # Collection for tracking information
        self.check_new_releases.start()  # Start the periodic task

    async def get_github_token(self, user_name):
        """Fetch the GitHub token from the database for the given user."""
        user_info = self.DB["UserInfo"].find_one({"user": user_name})
        if user_info and "Token" in user_info:
            return user_info["Token"]
        else:
            raise ValueError("GitHub token not found for the user.")
    
    # Track New Releases
    @nextcord.slash_command(name="git-track-releases", description="Set up notifications for new releases on a repository")
    async def track_releases(self, interaction: nextcord.Interaction, repo: str, channel: nextcord.TextChannel):
        """Track new releases from a specified GitHub repository."""
        try:
            # Get the GitHub token from the database
            self.github_token = await self.get_github_token(interaction.user.name)
            self.github_client = Github(self.github_token)  # Initialize GitHub client here
            
            # Check if the repository is already in the collection
            existing_entry = self.release_trackers_collection.find_one({"repo": repo})
            if existing_entry:
                await interaction.response.send_message(f"Already tracking `{repo}`.")
                return

            # Store tracking info in the ReleaseTrackers collection
            self.release_trackers_collection.insert_one({
                "repo": repo,
                "channel_id": channel.id,
                "user":interaction.user.name,
                "last_release_id": None
            })
            
            await interaction.response.send_message(f"Now tracking new releases for `{repo}` in {channel.mention}.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to set up release tracking: {str(e)}")

    # Periodic Task: Check New Releases
    @tasks.loop(minutes=1)
    async def check_new_releases(self):
        # Iterate through documents in the ReleaseTrackers collection
        for entry in self.release_trackers_collection.find():
            try:
                repo = entry["repo"]
                channel_id = entry["channel_id"]
                last_release_id = entry.get("last_release_id")
                user=entry.get("user")
                
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
        await self.bot.wait_until_ready()

    # Untrack Releases
    @nextcord.slash_command(name="git-untrack-releases", description="Stop tracking new releases for a repository")
    async def untrack_releases(self, interaction: nextcord.Interaction, repo: str):
        result = self.release_trackers_collection.delete_one({"repo": repo})
        if result.deleted_count > 0:
            await interaction.response.send_message(f"Stopped tracking new releases for `{repo}`.")
        else:
            await interaction.response.send_message(f"`{repo}` is not currently being tracked.")
            
# Async setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(Github_releases(bot))
