import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()

# Bot setup
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Sync failed: {e}")

# Prefix command


@bot.command()
async def test(ctx):
    await ctx.send("Test command works!")

# Slash command


@bot.tree.command(name="test", description="Test slash command")
async def slash_test(interaction: discord.Interaction):
    await interaction.response.send_message("Slash command works!")

# Run bot
bot.run(TOKEN)
