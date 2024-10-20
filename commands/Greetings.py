from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def say_hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.name}!')

    @commands.command(name='goodbye')
    async def say_goodbye(self, ctx):
        await ctx.send(f'Goodbye, {ctx.author.name}!')

# Function to setup the cog
async def setup(bot):
    await bot.add_cog(Greetings(bot))
