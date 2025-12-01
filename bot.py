import discord
from discord.ext import commands

TOKEN = MTQ0NDc0MjExNzU3MzM5NDUwNQ.GXUQ1k.3jiMHNKf0t5F88Ucgl5oTET6A7dd091Ijpqz1U
TARGET_CHANNEL_ID = X  # DO ZMIANY
REACTION_THRESHOLD = 3
FIRE_EMOJI = "🔥"

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
    # payload.member dostępny tylko jeśli zdarzenie pochodzi z guild i intents są ustawione
    # ignoruj reakcje botów (jeśli payload.member istnieje)
    if payload.member and payload.member.bot:
        return

    # sprawdź czy to fire emoji
    # payload.emoji może być PartialEmoji — porównamy po nazwie/znaku
    emoji_str = str(payload.emoji)
    if emoji_str != FIRE_EMOJI:
        return

    channel = bot.get_channel(payload.channel_id)
    if channel is None:
        # jeśli kanał nie w cache, pobierz przez API
        channel = await bot.fetch_channel(payload.channel_id)

    message = await channel.fetch_message(payload.message_id)

    # znajdź reakcję odpowiadającą 🔥 (może być kilka typów emoji, więc porównujemy str)
    fire_reaction = next((r for r in message.reactions if str(r.emoji) == FIRE_EMOJI), None)
    if not fire_reaction:
        return

    count = fire_reaction.count

    if count >= REACTION_THRESHOLD and message.id not in already_posted:
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel is None:
            target_channel = await bot.fetch_channel(TARGET_CHANNEL_ID)

        embed = discord.Embed(
            title="TAK ZWANA BOMBA",
            description=message.content or "(brak treści — sprawdź Message Content Intent)",
            color=discord.Color.orange()
        )
        embed.set_author(name=str(message.author), icon_url=getattr(message.author.avatar, "url", None))
        # dodaj link do oryginalnej wiadomości jeśli chcesz:
        try:
            embed.add_field(name="Link", value=f"[Kliknij aby przejść]({message.jump_url})", inline=False)
        except Exception:
            pass

        await target_channel.send(embed=embed)
        already_posted.add(message.id)

bot.run(TOKEN)