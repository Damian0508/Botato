import discord
from discord.ext import commands

def setup(client):
    client.add_cog(MathModule(client))

class MathModule(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('MathModule loaded')

    @commands.command()
    async def add(self, ctx, num1: float, num2:float):
        sum = num1 + num2
        await ctx.send(f'The sum of {num1} and {num2} is {sum}')
    # @add.error
    # async def add_error(ctx, error):
    #     if isinstance(error, commands.BadArgument):
    #         await ctx.send('Bad argument type')
    @commands.command()
    async def pi(self, ctx):
        await ctx.send('The number π is approximately equal 3,141592 653589 793238 462643 383279 502884')