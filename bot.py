import discord
import os
from discord.ext import commands

TWOJ_TOKEN = os.getenv("TWOJ_TOKEN")
TWOJE_ID_KANAU = os.getenv("TWOJE_ID_KANAU")


TOKEN = TWOJ_TOKEN
TARGET_CHANNEL_ID = TWOJE_ID_KANAU
REACTION_THRESHOLD = 3
EMOJI = "🔥"

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
already_posted = set()

@bot.event
async def on_ready():
    print(f"Zalogowano jako: {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member and payload.member.bot:
        return
    if str(payload.emoji) != EMOJI:
        return

    channel = bot.get_channel(payload.channel_id)
    if channel is None:
        channel = await bot.fetch_channel(payload.channel_id)

    message = await channel.fetch_message(payload.message_id)

    fire_reaction = next((r for r in message.reactions if str(r.emoji) == EMOJI), None)
    if fire_reaction and fire_reaction.count >= REACTION_THRESHOLD and message.id not in already_posted:
        target = bot.get_channel(TARGET_CHANNEL_ID)
        if target is None:
            target = await bot.fetch_channel(TARGET_CHANNEL_ID)

        files = []
        for attach in message.attachments:
            fp = await attach.to_file()
            files.append(fp)

        content = message.content or None
        jump = f"\n\n[🔗 Od oryginału]({message.jump_url})"

        embed = discord.Embed(
            description=message.content or "(brak treści — sprawdź Message Content Intent)",
            color=discord.Color.orange()
        )
        embed.set_author(name=str(message.author), icon_url=getattr(message.author.avatar, "url", None))
        try:
            embed.add_field(name="",value=f"[Kliknij aby przejść]({message.jump_url})", inline=False)
        except Exception:
            pass

        await target.send(embed=embed)
        already_posted.add(message.id)


bot.run(TOKEN)






