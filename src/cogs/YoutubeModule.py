import discord
from discord.ext import commands
import youtube_dl #youtube
from youtube import YTDLSource

def setup(client):
    client.add_cog(YoutubeModule(client))

async def create_voice_client(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send('You need to type this command on server where you are on voice channel')
        return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client
    return vc

class YoutubeModule(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('YoutubeModule loaded')

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    # @join.error
    # async def join_error(ctx, error):
    #     if isinstance(error, commands.CommandInvokeError):
    #         await ctx.send('You need to type this command on server where you are on voice channel')

    @commands.command()
    async def leave(self, ctx):
        server = ctx.message.guild
        voice_client = server.voice_client
        await voice_client.disconnect()
    # @leave.error
    # async def leave_error(ctx, error):
    #     if isinstance(error, commands.CommandInvokeError):
    #         await ctx.send('You need to type this command on server where you are on voice channel')

    @commands.command()
    async def stop(self, ctx):
        vc = await create_voice_client(ctx)
        vc.stop()
        await ctx.send('Sound has been stopped')

    @commands.command()
    async def pause(self, ctx):
        vc = await create_voice_client(ctx)
        vc.pause()
        await ctx.send('Sound has been paused')

    @commands.command()
    async def resume(self, ctx):
        vc = await create_voice_client(ctx)
        vc.resume()
        await ctx.send('Sound has been resumed')

    @commands.command()
    async def p(self, ctx, *, url):
        print(url)
        vc = await create_voice_client(ctx)
        player = await YTDLSource.from_url(url)
        vc.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))