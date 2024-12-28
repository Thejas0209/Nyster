import nextcord
from nextcord.ext import commands
import random
import asyncio

class Utility(commands.Cog):
    """
    A cog that provides utility commands for basic operations such as math evaluation,
    random choice selection, and number rolling.
    """

    def __init__(self, bot):
        """
        Initializes the Utility cog with the bot instance.
        """
        self.bot = bot

    @commands.command(name='math')
    async def math(self, ctx, *, expression):
        """
        Evaluates a mathematical expression and sends the result as an embedded message.

        Parameters:
        - expression (str): The mathematical expression to evaluate (e.g., '2 + 2').

        Returns:
        - An embedded message displaying the evaluated expression and result.
        """
        try:
            result = eval(expression)
            embed = nextcord.Embed(
                title='Math Eval',
                description=f"Expression: {expression}\n Answer: {result}",
                color=nextcord.Color.dark_gold(),
                timestamp=ctx.message.created_at
            )
        except Exception as e:
            embed = nextcord.Embed(
                title='Math Eval Error',
                description=f"Invalid Math expression: {expression}",
                color=nextcord.Color.red(),
                timestamp=ctx.message.created_at
            )
        await ctx.send(embed=embed)

    @commands.command(name='choose')
    async def choose(self, ctx, *, args):
        """
        Chooses a random option from a list of options provided by the user.

        Parameters:
        - args (str): A string of options separated by slashes (e.g., 'apple/banana/cherry').

        Returns:
        - An embedded message displaying the chosen option after a brief 'thinking' animation.
        """
        options = args.split('/')
        if len(options) < 2:
            await ctx.reply("Please provide more than one option to choose from.")
            return

        choice = random.choice(options)
        embed = nextcord.Embed(
            title='Thinking....',
            color=nextcord.Color.dark_gold()
        )
        reply = await ctx.send(embed=embed)
        await asyncio.sleep(0.2)

        for i in range(5):
            embed = nextcord.Embed(
                title=f':clock{i+1}: Thinking.......',
                color=nextcord.Color.dark_gold()
            )
            await reply.edit(embed=embed)
            await asyncio.sleep(0.2)

        embed = nextcord.Embed(title=choice, color=nextcord.Color.dark_gold())
        await reply.edit(embed=embed)

    @nextcord.slash_command(name='roll', description='Rolls a random number')
    async def roll(self, interaction: nextcord.Interaction, max: int = 6):
        """
        Rolls a random number between 1 and the specified maximum value and sends the result.

        Parameters:
        - max (int): The maximum value for the roll. Default is 6.

        Returns:
        - An embedded message displaying the rolled number.
        """
        rand = random.randint(1, max)
        embed = nextcord.Embed(title=f'You rolled {rand}', color=nextcord.Color.dark_gold())
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))