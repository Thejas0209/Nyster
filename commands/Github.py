import discord
from discord.ext import commands
import requests
import os 
from dotenv import load_dotenv
load_dotenv()

class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_token = os.getenv("Git_Token")
        self.github_api_url = 'https://api.github.com'
        self.headers = {'Authorization': f'token {self.github_token}'}
        
    #Commits information
    @discord.app_commands.command(name="git-commits",description="Fetches last 5 commits on the repository")
    async def commits(self, interaction:discord.Interaction, repo: str):
        """Fetch the latest commits from a GitHub repository."""
        url = f"{self.github_api_url}/repos/{repo}/commits"
        
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            commits = response.json()
            commit_messages = [
                f"{commit['commit']['message']} by {commit['commit']['author']['name']}" 
                for commit in commits[:5]
            ]
            await interaction.response.send_message(f"Here are the latest updates on **{repo}**:\n"+'\n'.join(commit_messages))
        else:
            await interaction.response.send_message(f"Error fetching commits: {response.status_code}")
            
    #Repository Information       
    @discord.app_commands.command(name="git-repo_info", description="Display repository information")
    async def Repoinfo(self, interaction: discord.Interaction, repo: str):
        url = f"{self.github_api_url}/repos/{repo}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            repo_info = response.json()
            embed = discord.Embed(
                title='GitHub Repository Info',
                description="Displays basic information about the specified GitHub repository.",
                color=discord.Color.gold(),
                timestamp=interaction.created_at
            )
            
            # Basic repo information
            embed.set_thumbnail(url="https://github-production-user-asset-6210df.s3.amazonaws.com/19292210/290303037-0612e088-0394-421d-9266-2f6e1d12498e.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20241014%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241014T224831Z&X-Amz-Expires=300&X-Amz-Signature=a68a34c2d828b9911bd4ec6cfe6dc819d26169dc119857bd7d493680f3c8126b&X-Amz-SignedHeaders=host")
            embed.add_field(name="Repo Name", value=repo_info['name'], inline=False)
            embed.add_field(name="Repo Owner", value=repo_info['owner']['login'], inline=False)
            embed.add_field(name="Repo Description", value=repo_info.get("description", "No description"), inline=False)
            embed.add_field(name="Repo Created On", value=repo_info['created_at'], inline=False)
            embed.add_field(name="Stars Received", value=repo_info['stargazers_count'], inline=False)
            response_collab = requests.get(url + "/collaborators", headers=self.headers)
            response_lang = requests.get(url + "/languages", headers=self.headers)
            if response_collab.status_code == 200:
                collaborators = [collab['login'] for collab in response_collab.json()]
                embed.add_field(name="Collaborators", value="\n".join(collaborators) if collaborators else "None", inline=False)
            if response_lang.status_code == 200:
                languages = response_lang.json().keys()
                embed.add_field(name="Languages Used", value=", ".join(languages) if languages else "None", inline=False)
            embed.add_field(name="Clone Repo Link", value=repo_info["clone_url"], inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"Command failed with error {response.status_code}: {response.json().get('message', 'Unknown error')}")
          

# Async setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(GitHub(bot))
