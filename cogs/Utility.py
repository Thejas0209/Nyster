import nextcord
from nextcord.ext import commands
import random
import asyncio

class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command(name='math')
    async def math(self, ctx, *, expression):
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
    async def choose(self,ctx,*,args):
        options=args.split('/')
        if len(options)<2:
            await ctx.reply("Nigga what am I supposed to choose when there is only one option")
            return
        choice=random.choice(options)
        embed=nextcord.Embed(
            title='Thinking....',
            color=nextcord.Color.dark_gold())
        reply=await ctx.send(embed=embed)
        await asyncio.sleep(0.2)
        for i in range(5):
            embed=nextcord.Embed(
                title=f':clock{i+1}: Thinking.......',
                color=nextcord.Color.dark_gold())
            await reply.edit(embed=embed)
            await asyncio.sleep(0.2)
        embed=nextcord.Embed(title=choice,color=nextcord.Color.dark_gold())
        await reply.edit(embed=embed)


    @nextcord.slash_command(name='roll',description='Rolls a random number')
    async def roll(self,interaction:nextcord.Interaction,max:int=6):
        rand=random.randint(1,max)
        embed=nextcord.Embed(title=f'You rolled {rand}',color=nextcord.Color.dark_gold())    
        await interaction.response.send_message(embed=embed)
        
def setup(bot):
    bot.add_cog(Utility(bot))