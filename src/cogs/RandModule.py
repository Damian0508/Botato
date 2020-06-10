import discord
from discord.ext import commands
import random

def setup(client):
    client.add_cog(RandModule(client))

def rangecheck(arg, min, max):
    if min <= arg <= max:
        return True
    else:
        return False

class RandModule(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('RandModule loaded')

    @commands.command(aliases = ['roll', 'dice'], brief = '<x> | <x> <y> | <x> <y> <z>', 
                      description = 'One argument: displays random intager from 1 to <x> (dice roll)\n\
                      Two arguments: displays table of <x> integers from 1 to <y> and shows thier sum (several dice rolls)\n\
                      Three arguments: displays table of <x> integers from 1 to <y> and shows thier sum with <z> modifier (several dice rolls with modifier)',
                      usage = 'int int int')
    async def d(self, ctx, *args: int):

        argument_number = len(args)

        if argument_number == 1:
            if rangecheck(args[0], 1, 1000):
                rnd = random.randint(1, args[0])
                await ctx.send(rnd)
            else:
                await ctx.send('I can only draw from 1 to 1000')

        elif argument_number == 2:
            if rangecheck(args[0], 1, 200):
                suma = 0
                throw_table = []
                for x in range(args[0]):
                    rnd = random.randint(1, args[1])
                    suma += rnd
                    throw_table.append(rnd)
                await ctx.send(f'Your throws: {throw_table} total: {suma}')
            else:
                await ctx.send('I can only make throws from range 1 to 200')

        elif argument_number == 3:
            if rangecheck(args[0], 1, 200):
                if rangecheck(args[1], 1, 1000):
                    suma = 0
                    throw_table = []
                    for x in range(args[0]):
                        rnd = random.randint(1, args[1])
                        suma += rnd
                        throw_table.append(rnd)
                    suma += args[2]
                    await ctx.send(f'Your throws: {throw_table} with modificator {args[2]} total: {suma}')
                else:
                    await ctx.send('I can only draw from 1 to 1000')
            else:
                await ctx.send('I can only make throws from range 1 to 200')
        else:
            await ctx.send('Invalid number of arguments')
    # @d.error
    # async def d_error(ctx, error):
    #     if isinstance(error, commands.BadArgument):
    #         await ctx.send('Bad argument type')