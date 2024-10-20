import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        
    #User info
    @discord.app_commands.command(name='user_info',description="Display user info")
    async def user_info(self,interaction:discord.Interaction,member:discord.Member=None):
        if member==None:
            member=interaction.user
        embed=discord.Embed(
            title="User info",
            description="Display user info",
            color=discord.Color.gold(),
            timestamp=interaction.created_at)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Username",value=member)
        embed.add_field(name="Name",value=member.name)
        embed.add_field(name="Nick name",value=member.display_name)
        embed.add_field(name="Created at",value=member.created_at.strftime("%d %b %Y"))
        embed.add_field(name="Joined at",value=member.joined_at.strftime("%d %b %Y"))
        embed.add_field(name="Status",value=member.status)
        await interaction.response.send_message(embed=embed)

    #Server info 
    @discord.app_commands.command(name='server_info',description="Display Server info")
    async def server_info(self,interaction:discord.Interaction):
        embed=discord.Embed(
            title="Server info",
            description="Display server info",
            color=discord.Color.pink(),
            timestamp=interaction.created_at)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name="Name",value=interaction.guild.name)
        embed.add_field(name="Created at",value=interaction.guild.created_at.strftime("%d %b %Y"))
        embed.add_field(name="Server owner",value=interaction.guild.owner)
        embed.add_field(name="Description",value=interaction.guild.description)
        embed.add_field(name="Members",value=interaction.guild.member_count)
        embed.add_field(name="Roles",value=len([roles.name for roles in interaction.guild.roles]))
        embed.add_field(name="Text channels",value=len([text.name for text in interaction.guild.text_channels]))
        embed.add_field(name="Voice channels",value=len([voice.name for voice in interaction.guild.voice_channels]))
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
