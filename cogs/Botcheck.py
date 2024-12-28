import nextcord
from nextcord.ext import commands
import nextcord.ext
import nextcord.ext.tasks

class Botcheck(commands.Cog):
    """
    A Cog that provides a slash command to check the bot's current latency (ping).
    """

    def __init__(self, bot):
        """
        Initializes the Botcheck Cog.

        Args:
            bot (commands.Bot): The bot instance to which this Cog belongs.
        """
        self.bot = bot

    @nextcord.slash_command(name='ping', description="It will show ping")
    async def ping(self, interaction: nextcord.Interaction):
        """
        A slash command to display the bot's current latency in milliseconds.

        Args:
            interaction (nextcord.Interaction): The interaction context from the user.
        """
        bot_ping = abs(self.bot.latency * 100)
        await interaction.response.send_message(f"Current ping is: {bot_ping}")

def setup(bot):
    bot.add_cog(Botcheck(bot))