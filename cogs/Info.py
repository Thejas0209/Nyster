import nextcord
from nextcord.ext import commands

class Info(commands.Cog):
    """
    A cog for displaying user and server information.
    """
    def __init__(self, bot):
        """
        Initializes the Info Cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
        
    @nextcord.slash_command(name='user_info', description="Display user info")
    async def user_info(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        """
        Command to display information about a user.

        Args:
            interaction (nextcord.Interaction): The interaction object.
            member (nextcord.Member, optional): The member whose information to display. Defaults to the user who invoked the command.
        """
        if member is None:
            member = interaction.user
        embed = nextcord.Embed(
            title="User Info",
            description="Display user info",
            color=nextcord.Color.teal(),
            timestamp=interaction.created_at
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Username", value=member)
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="Nick name", value=member.display_name)
        embed.add_field(name="Created at", value=member.created_at.strftime("%d %b %Y"))
        embed.add_field(name="Joined at", value=member.joined_at.strftime("%d %b %Y"))
        embed.add_field(name="Status", value=member.status)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name='server_info', description="Display server info")
    async def server_info(self, interaction: nextcord.Interaction):
        """
        Command to display information about the server.

        Args:
            interaction (nextcord.Interaction): The interaction object.
        """
        embed = nextcord.Embed(
            title="Server Info",
            description="Display server info",
            color=nextcord.Color.teal(),
            timestamp=interaction.created_at
        )
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name="Name", value=interaction.guild.name)
        embed.add_field(name="Created at", value=interaction.guild.created_at.strftime("%d %b %Y"))
        embed.add_field(name="Server owner", value=interaction.guild.owner)
        embed.add_field(name="Description", value=interaction.guild.description)
        embed.add_field(name="Members", value=interaction.guild.member_count)
        embed.add_field(name="Roles", value=len([role.name for role in interaction.guild.roles]))
        embed.add_field(name="Text channels", value=len([text.name for text in interaction.guild.text_channels]))
        embed.add_field(name="Voice channels", value=len([voice.name for voice in interaction.guild.voice_channels]))
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))