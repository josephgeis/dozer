from discord.ext.commands import Bot
import discord
import aiohttp

import config

bot = Bot(command_prefix='!')


@bot.command()
async def move(ctx, after: str, dest: str):
    print(f'{ctx.author} moved {after} to {dest}')
    after: int = int(after)

    dest = dest.strip("<#").strip(">")
    dest: int = int(dest)

    after_msg = await ctx.channel.fetch_message(after)

    dest_channel = ctx.guild.get_channel(dest)
    hook = await dest_channel.create_webhook(name=f"dozer_hook")

    async with dest_channel.typing():
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(
                hook.url, session=session)
            async for message in ctx.channel.history(limit=None, after=after_msg, before=ctx.message):
                await webhook.send(message.content, username=f"{message.author.name} (moved from {message.channel.name})", avatar_url=message.author.avatar)
                await message.delete()

    await hook.delete()
    await ctx.message.delete()

if __name__ == '__main__':
    bot.run(config.BOT_TOKEN)
