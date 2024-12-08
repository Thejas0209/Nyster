from nextcord.ext import commands

class Greetings(commands.Cog):
    """
    A simple cog to greet users.
    Contains commands for saying hello and goodbye.
    """
    def __init__(self, bot):
        """
        Initializes the Greetings Cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @commands.command(name='hello')
    async def say_hello(self, ctx):
        """
        Sends a hello message to the user.

        Args:
            ctx (commands.Context): The context of the command.
        """
        await ctx.send(f'Hello, {ctx.author.name}!')

    @commands.command(name='goodbye')
    async def say_goodbye(self, ctx):
        """
        Sends a goodbye message to the user.

        Args:
            ctx (commands.Context): The context of the command.
        """
        await ctx.send(f'Goodbye, {ctx.author.name}!')

# Function to setup the cog
def setup(bot):
    """
    Adds the Greetings Cog to the bot.

    Args:
        bot (commands.Bot): The bot instance.
    """
    bot.add_cog(Greetings(bot))
