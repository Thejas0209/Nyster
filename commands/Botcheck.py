import discord
import random
import asyncio
from discord.ext import commands

class Botcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='math')
    async def math(self, ctx, *, expression):
        try:
            result = eval(expression)
            embed = discord.Embed(
                title='Math Eval',
                description=f"Expression: {expression}\n Answer: {result}",
                color=discord.Color.dark_gold(),
                timestamp=ctx.message.created_at
            )
        except Exception as e:
            embed = discord.Embed(
                title='Math Eval Error',
                description=f"Invalid Math expression: {expression}",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
        await ctx.send(embed=embed)

    @commands.command(name='choose')
    async def choose(self,ctx,*,args):
        options=args.split('/')
        if len(options)<2:
            await ctx.reply("Nigga what am I supposed to choose when there is only one option")
            return
        choice=random.choice(options)
        embed=discord.Embed(
            title='Thinking....',
            color=discord.Color.dark_gold())
        reply=await ctx.send(embed=embed)
        await asyncio.sleep(0.2)
        for i in range(5):
            embed=discord.Embed(
                title=f':clock{i+1}: Thinking.......',
                color=discord.Color.dark_gold())
            await reply.edit(embed=embed)
            await asyncio.sleep(0.2)
        embed=discord.Embed(title=choice,color=discord.Color.dark_gold())
        await reply.edit(embed=embed)

# Function to setup the cog
async def setup(bot):
    await bot.add_cog(Botcheck(bot))
