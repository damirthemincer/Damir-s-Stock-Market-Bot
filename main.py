import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import schedule

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Global Functions


def test_job():
    print("This is a second")


schedule.every().second.do(test_job)

# Global Variables


# Intents
intents = discord.Intents.default()
intents.message_content = True

# Tasks loop


@tasks.loop(seconds=0.5)
async def every_second_task():
    schedule.run_pending()


@every_second_task.before_loop
async def before_every_second_task():
    await bot.wait_until_ready()

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
        every_second_task.start()
        print("Started every_second_task()")
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
