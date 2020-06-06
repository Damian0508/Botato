try:
    import os
    import random
    import discord
    import asyncio
    from discord.ext import commands, tasks
except:
    raise Exception("Brak potrzebnego modulu")

client = commands.Bot(command_prefix='!')

# loading all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

def rangecheck(arg, min, max):
    if min <= arg <= max:
        return True
    else:
        return False

# @tasks.loop(hours = 168)
# async def it_is_wednesday():
#     general = client.get_channel(506961371590688779)
#     await general.send('It is wednesday my dudes')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Extension loaded')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('Extension unloaded')

@client.command()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.send('Extension reloaded')

@client.event
async def on_ready():
    print('PotatoBOT is runing')
    #it_is_wednesday.start()
    await client.change_presence(activity = discord.Game('Potatoes contain potassium!'))

# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send('There is no such command, check !help')

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 100):
    amount += 1
    await ctx.channel.purge(limit = amount)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Bad argument type')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def add(ctx, num1: float, num2:float):
    sum = num1 + num2
    await ctx.send(f'The sum of {num1} and {num2} is {sum}')
@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Bad argument type')

@client.command()
async def pi(ctx):
    await ctx.send('The number π is approximately equal 3,141592 653589 793238 462643 383279 502884')

@client.command(aliases = ['roll', 'dice'])
async def d(ctx, *args: int):

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
            await ctx.send('Your throws: {0} total: {1}'.format(throw_table, suma))
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
                await ctx.send('Your throws: {0} with modificator {1} total: {2}'.format(throw_table, args[2], suma))
            else:
                await ctx.send('I can only draw from 1 to 1000')
        else:
            await ctx.send('I can only make throws from range 1 to 200')
    else:
        await ctx.send('Invalid number of arguments')
@d.error
async def d_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Bad argument type')


client.run("NzAxNzk5NTg1NzAxNjkxNTMz.Xp3Trw.3RCNSpoDcMID06EGdU0eMNTdKzk")

