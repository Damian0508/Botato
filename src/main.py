try:
    import os
    from os.path import join, dirname
    import discord
    import asyncio
    from dotenv import load_dotenv
    from discord.ext import commands, tasks
except:
    raise Exception("Brak potrzebnego modulu")

env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

client = commands.Bot(command_prefix='!')

# loading all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# @tasks.loop(hours = 168)
# async def it_is_wednesday():
#     general = client.get_channel(506961371590688779)
#     await general.send('It is wednesday my dudes')

@client.command(description = 'Loads <extension>', usage = 'string', brief = '<extension_name>')
async def load(ctx, extension:str):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Extension loaded')

# @client.command()
# async def unload(ctx, extension):
#     client.unload_extension(f'cogs.{extension}')
#     await ctx.send('Extension unloaded')

@client.command(description = 'Reloads <extension>', usage = 'string', brief = '<extension_name>')
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

@client.command(description = 'Deletes <x> last messeges on channel. If argument is not given - deletes 100 last messeges\n\
                You need to have message managment permission to use this command', 
                usage = 'int', brief = '<x>')
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount:int = 100):
    amount += 1
    await ctx.channel.purge(limit = amount)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Bad argument type')

@client.command(description = 'Writes Pong! and bot latency', usage = '(no argumens needed)')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


your_token = os.getenv("TOKEN")
client.run(your_token)

