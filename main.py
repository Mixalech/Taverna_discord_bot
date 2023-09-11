from Information import config, function_command, function_event


@config.bot.event
async def on_ready():
    await function_event.on_ready()


@config.bot.event
async def on_raw_reaction_add(payload):
    await function_event.on_raw_reaction_add(payload)


@config.bot.event
async def on_raw_reaction_remove(payload):
    await function_event.on_raw_reaction_remove(payload)


@config.bot.event
async def on_member_join(member):
    await function_event.on_member_join(member)


@config.bot.command(name = "sobering")
async def sobering(ctx):
    await function_command.sobering(ctx)


@config.bot.command(name = "playblya")
async def playblya(ctx, url: str):
    await function_command.check(ctx, url) 
  

@config.bot.command(name = "joins")
async def joins(ctx):
    await function_command.joins(ctx)


@config.bot.command(name = "vanish")
async def vanish(ctx, num: int):        #num - число сообщений необходимых удалить
    await function_command.vanish(ctx, num)


@config.bot.command(name = "disconnect")
async def leave(ctx):
    await function_command.leave(ctx)


config.bot.run(config.TOKEN)