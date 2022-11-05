import discord
import traceback
from discord.ext import commands
from os import getenv
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# チャンネル入退室時の通知処理
@bot.event
async def on_voice_state_update(member, before, after):

    if member.guild.id == 825601093802655775 and (before.channel != after.channel):
        now = datetime.utcnow() + timedelta(hours=9)
        alert_channel = bot.get_channel(825601094323011625)
        if before.channel is None:
            msg = f'{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に出勤しました。'
            await alert_channel.send(msg)
        elif after.channel is None:
            msg = f'{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退勤しました。'
            await alert_channel.send(msg)

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
