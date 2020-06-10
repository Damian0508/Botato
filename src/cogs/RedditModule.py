import discord
from discord.ext import commands
import random
import os
import praw #reddit

def setup(client):
    client.add_cog(RedditModule(client))

cl_id = os.getenv("ID")
secret = os.getenv("SECRET")
agent = os.getenv("AGENT")

reddit = praw.Reddit(client_id=cl_id,
                    client_secret=secret,
                    user_agent=agent)

async def post_hot_from_sub(ctx, sub):
    print(sub)
    memes_submissions = reddit.subreddit(f'{sub}').hot()
    post_to_pick = random.randint(1, 50)
    for i in range(post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send(submission.url)

async def post_top_from_sub(ctx, sub, time):
    print(sub)
    memes_submissions = reddit.subreddit(f'{sub}').top(f'{time}')
    for x in range(3):
        submission = next(x for x in memes_submissions if not x.stickied)
        await ctx.send(submission.url)

class RedditModule(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('RedditModule loaded')

    @commands.command(description = 'Posts single random "Hot" url from "memes" subreddit', usage = '(no argumens needed)')
    async def meme(self, ctx):
        await post_hot_from_sub(ctx, "memes")

    @commands.command(description = 'Posts single random "Hot" url from "cats" subreddit', usage = '(no argumens needed)')
    async def kitty(self, ctx):
        await post_hot_from_sub(ctx, "cats")

    @commands.command(description = 'Posts single random "Hot" url from <subreddit>', usage = 'string', brief = '<subreddit>')
    async def rd(self, ctx, *, sub:str):
        await post_hot_from_sub(ctx, f'{sub}')

    @commands.command(description = 'Posts three "top" of "Today" urls from <subreddit>', usage = 'string', brief = '<subreddit>')
    async def daytop3(self, ctx, *, sub:str):
        await post_top_from_sub(ctx, sub, "day")

    @commands.command(description = 'Posts three "Top" of "This Week" urls from <subreddit>', usage = 'string', brief = '<subreddit>')
    async def weektop3(self, ctx, *, sub:str):
        await post_top_from_sub(ctx, sub, "week")

    @commands.command(description = 'Posts three "Top" of "This Month" urls from <subreddit>', usage = 'string', brief = '<subreddit>')
    async def monthtop3(self, ctx, *, sub:str):
        await post_top_from_sub(ctx, sub, "month")

    @commands.command(description = 'Posts three "Top" of "This Year" urls from <subreddit>', usage = 'string', brief = '<subreddit>')
    async def yeartop3(self, ctx, *, sub:str):
        await post_top_from_sub(ctx, sub, "year")

    @commands.command(description = 'Posts three "Top" of "All Time" urls from <subreddit>', usage = 'string', brief = '<subreddit>')
    async def top3(self, ctx, *, sub:str):
        await post_top_from_sub(ctx, sub, "all")

    # @top3.error
    # async def top3_error(ctx, error):
    #     if isinstance(error, commands.CommandInvokeError):
    #         await ctx.send("There's no subreddit with this name")