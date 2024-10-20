import discord
from discord.ext import commands
import random

class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @discord.app_commands.command(name='ping',description="It will show ping")
    async def ping(self,interaction:discord.Interaction):
        bot_ping=abs(self.bot.latency*100)
        await interaction.response.send_message(f"Current ping is: {bot_ping}")

    @discord.app_commands.command(name='roll',description='Rolls a random number')
    async def roll(self,interaction:discord.Interaction,max:int=6):
        rand=random.randint(1,max)
        embed=discord.Embed(title=f'You rolled {rand}',color=discord.Color.dark_gold())    
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Utility(bot))