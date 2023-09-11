import discord, datetime, youtube_dl
from player import supp_youtube as lq
from Information import config


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'}

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'noplaylist': True,
    'simulate': 'True',
    'preferredquality': '192',
    'preferredcodec': 'mp3',
    'key': 'FFmpegExtractAudio'}


songs_queue = lq.Queue()
loop_flag = False

#########################[JOIN BLOCK]#########################

async def join(ctx):
    if ctx.message.author.voice:
        if not ctx.voice_client:
            await ctx.message.author.voice.channel.connect(reconnect=True)
        else:
            await ctx.voice_client.move_to(ctx.message.author.voice.channel)
    else:
        await ctx.message.reply('❗ Вы должны находиться в голосовом канале ❗')


async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.message.reply(f'🍺 Ушёл в запой вместе с \
{ctx.message.author.mention} 🍺')
    else:
        await ctx.message.reply('Вы попытались разбудить бота,\
 но он в отключке 💤')

#########################[PLAY MUSIC BLOCK]#########################

async def add(ctx, *url):
    url = ' '.join(url)
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except:
            info = ydl.extract_info(f"ytsearch:{url}",
                                    download=False)['entries'][0]

    URL = info['formats'][0]['url']
    name = info['title']
    time = str(datetime.timedelta(seconds=info['duration']))
    songs_queue.q_add([name, time, URL])
    embed = discord.Embed(description=f'Записываю [{name}]({url}) в очередь 📝',
                          colour=discord.Colour.red())
    await ctx.message.reply(embed=embed)


def step_and_remove(voice_client):
    if loop_flag:
        songs_queue.q_add(songs_queue.get_value()[0])
    songs_queue.q_remove()
    audio_player_task(voice_client)


def audio_player_task(voice_client):
    if not voice_client.is_playing() and songs_queue.get_value():
        voice_client.play(discord.FFmpegPCMAudio(
                                  executable="C:/ffmpeg/bin/ffmpeg.exe",
                                  source=songs_queue.get_value()[0][2],
                                  **FFMPEG_OPTIONS),
                                  after=lambda e: step_and_remove(voice_client))


async def play(ctx, *url):
    await join(ctx)
    await add(ctx, ' '.join(url))
    voice_client = ctx.guild.voice_client
    audio_player_task(voice_client)


async def queue(ctx):
    if len(songs_queue.get_value()) > 0:
        only_names_and_time_queue = []
        for i in songs_queue.get_value():
            name = i[0]
            if len(i[0]) > 30:
                name = i[0][:30] + '...'
            only_names_and_time_queue.append(f'📀 `{name:<33}   {i[1]:>20}`\n')
        c = 0
        queue_of_queues = []
        while c < len(only_names_and_time_queue):
            queue_of_queues.append(only_names_and_time_queue[c:c + 10])
            c += 10

        embed = discord.Embed(title=f'ОЧЕРЕДЬ [LOOP: {loop_flag}]',
                              description=''.join(queue_of_queues[0]),
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)

        for i in range(1, len(queue_of_queues)):
            embed = discord.Embed(description=''.join(queue_of_queues[i]),
                                  colour=discord.Colour.red())
            await ctx.send(embed=embed)
    else:
        await ctx.send('Очередь пуста 📄')


async def pause(ctx):
    voice = discord.utils.get(config.bot.voice_clients, guild=ctx.guild)
    if voice:
        voice.pause()
        await ctx.message.reply('Шо ты сделал? Порвал струну. Без неё играй!')


async def resume(ctx):
    voice = discord.utils.get(config.bot.voice_clients, guild=ctx.guild)
    if voice:
        if voice.is_paused():
            voice.resume()
            await ctx.message.reply('Поменял струну.')


async def skip(ctx):
    voice = discord.utils.get(config.bot.voice_clients, guild=ctx.guild)
    if voice:
        voice.stop()


async def clear(ctx):
    voice = discord.utils.get(config.bot.voice_clients, guild=ctx.guild)
    if voice:
            voice.stop()
            while not songs_queue.is_empty():
                songs_queue.q_remove()


async def remove(ctx, index):
    try:
        if len(songs_queue.get_value()) > 0:
            index = int(index) - 1
            if index >= 0:
                d = songs_queue.q_rem_by_index(index)[0]
                await ctx.message.reply(f'Вычеркнул из списка: {d}')
        else:
            await ctx.message.reply('Нечего удалять')
    except:
        await ctx.message.reply(f'Песни с таким индексом не существует')