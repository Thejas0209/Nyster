import nextcord
from nextcord.ext import commands

import nextcord.ext
import nextcord.ext.tasks

class Botcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='ping',description="It will show ping")
    async def ping(self,interaction:nextcord.Interaction):
        bot_ping=abs(self.bot.latency*100)
        await interaction.response.send_message(f"Current ping is: {bot_ping}")
    
    
# Function to setup the cog
def setup(bot):
    bot.add_cog(Botcheck(bot))
