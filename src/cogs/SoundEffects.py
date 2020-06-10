import discord
from discord.ext import commands

def setup(client):
    client.add_cog(SoundEffects(client))

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

async def play_sound(ctx, file):
    vc = await create_voice_client(ctx)
    vc.play(discord.FFmpegPCMAudio(f'Sound_Effects/{file}'))

class SoundEffects(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('SoundEffects loaded')

    @commands.command(description = 'Only cricets sound', usage = '(no argumens needed)')
    async def silence(self, ctx):
        await play_sound(ctx, 'Cricets.mp3')

    @commands.command(description = 'Mayushi tuturu! Steins;Gate - the best anime ;)', usage = '(no argumens needed)')
    async def tuturu(self, ctx):
        await play_sound(ctx, 'Tuturu.mp3')

    @commands.command(description = 'Seinfeld Theme Song', usage = '(no argumens needed)')
    async def gold(self, ctx):
        await play_sound(ctx, 'Seinfield.mp3')

    @commands.command(description = 'Bruh!', usage = '(no argumens needed)')
    async def bruh(self, ctx):
        await play_sound(ctx, 'Bruh.mp3')

    @commands.command(description = 'Chewbacca roar', usage = '(no argumens needed)')
    async def chew(self, ctx):
        await play_sound(ctx, 'Chewbacca.mp3')

    @commands.command(description = 'Loud horn melody', usage = '(no argumens needed)')
    async def horn(self, ctx):
        await play_sound(ctx, 'Horn.mp3')

    @commands.command(description = "Fuck, that's the laser raptor", usage = '(no argumens needed)')
    async def jasny(self, ctx):
        await play_sound(ctx, 'Jasny.mp3')

    @commands.command(description = 'Suprise motherfucker!', usage = '(no argumens needed)')
    async def suprise(self, ctx):
        await play_sound(ctx, 'Surprise.mp3')
