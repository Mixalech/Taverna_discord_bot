import discord, asyncio
from Information import config


async def on_ready():
    print("Бот готов к работе!")
    await config.bot.change_presence(activity=discord.Activity(
        type = discord.ActivityType.listening, name='советы пьяного бомжа'))


async def on_raw_reaction_add(payload):
    if payload.message_id == config.ID_POST:
        channel = config.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = discord.utils.get(message.guild.members, id=payload.user_id)
        emoji = str(payload.emoji)

        role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])
        await user.add_roles(role)
        print(f"{user.name} получил роль {role.name}")


async def on_raw_reaction_remove(payload):
    channel = config.bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = discord.utils.get(message.guild.members, id=payload.user_id)

    emoji = str(payload.emoji)
    role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])
    await user.remove_roles(role)
    print(f"{user.name}, лишился роли {role.name}")


async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Трезвый")
    await member.add_roles(role)
    await asyncio.sleep(10 * 60)
    await member.remove_roles(role)