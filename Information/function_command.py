from discord.ext import commands
from player import play_youtuber
import discord, asyncio


bot = commands.Bot(command_prefix='/', intents = discord.Intents.all()) 


async def leave(ctx):
    channel = ctx.message.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send(f":wave: Покинул канал {channel}", delete_after = 60)
    else: await ctx.send("Бот должен находиться в голосовом канале для использования этой комманды", delete_after = 60)


async def joins(ctx):
    if ctx.message.author.voice:
        if not ctx.voice_client:
            await ctx.message.author.voice.channel.connect(reconnect=True)
        else:
            await ctx.voice_client.move_to(ctx.message.author.voice.channel)
    else:
        await ctx.message.reply('❗ Вы должны находиться в голосовом канале ❗', delete_after = 120)


async def check(ctx, url): #функция для проверки url
    if ("youtube.com" in url or "youtu.be" in url):
        await play_youtuber.play(ctx, url)
    elif "vk" in url:
        await ctx.send("Платформа 'vk', пока не поддерживается ботом.", delete_after = 180)
    else: 
        await ctx.send("Указанная вами платформа пока не поддерживается ботом.", delete_after = 180)


async def sobering(ctx):
    role = ctx.guild.get_role(1137609824025198683) #id_role
    await ctx.author.add_roles(role)
    await asyncio.sleep(10 * 60)
    await ctx.author.remove_roles(role)


async def vanish(ctx, num: int):
    channel = ctx.channel
    await ctx.channel.purge(limit=int(num))
    print(f"Удалены {num - 1} сообщений из канала {channel}")