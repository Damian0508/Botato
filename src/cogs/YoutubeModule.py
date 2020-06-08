import discord
from discord.ext import commands
import youtube_dl #youtube
import asyncio

def setup(client):
    client.add_cog(YoutubeModule(client))

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

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

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.8):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

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