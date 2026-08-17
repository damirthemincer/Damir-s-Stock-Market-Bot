import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import schedule
from pathlib import Path
import json
from discord import app_commands

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


@bot.command()
async def market(ctx):
    message = ""
    for file_path in Path('companies/').iterdir():
        with open(f"companies/{file_path.name}", "r") as file:
            data = json.load(file)
            message += f"\n{data["name"]}: {data["current_stock"]} 💰"
    await ctx.reply(message)


@bot.command()
async def company(ctx, target):
    target = target.lower()
    check_path = Path(f"companies/{target}.json")
    if not check_path.is_file():
        await ctx.reply("Company does not exist, or you made a typo. Please double check your message.")
        return
    with open(f"companies/{target}.json", "r") as file:
        data = json.load(file)
        message = f"Name: **{data["name"]}** \nDescription: *{data["desc"]}* \nCurrent individual share price: **{str(data["current_stock"])}** \nRisk: **{str(data["risk"])}/10** \nOutstanding Shares: **{str(data["shares"])}**"
    await ctx.reply(message)


# Slash command

@bot.tree.command(name="test", description="Test slash command")
async def slash_test(interaction: discord.Interaction):
    await interaction.response.send_message("Slash command works!")


@bot.tree.command(name="market", description="Views the current stock market!")
async def market(interaction: discord.Interaction):
    message = ""
    for file_path in Path('companies/').iterdir():
        with open(f"companies/{file_path.name}", "r") as file:
            data = json.load(file)
            message += f"\n{data["name"]}: {data["current_stock"]} 💰"
    await interaction.response.send_message(message)


@bot.tree.command(name="company", description="View more details about a specific company!")
@app_commands.describe(target="Put a companies name, capitalization doesn't matter.")
async def company(interaction: discord.Interaction, target: str):
    target = target.lower()
    check_path = Path(f"companies/{target}.json")
    if not check_path.is_file():
        await interaction.response.send_message("Company does not exist, or you made a typo. Please double check your message.")
        return
    with open(f"companies/{target}.json", "r") as file:
        data = json.load(file)
        message = f"Name: **{data["name"]}** \nDescription: *{data["desc"]}* \nCurrent individual share price: **{str(data["current_stock"])}** \nRisk: **{str(data["risk"])}/10** \nOutstanding Shares: **{str(data["shares"])}**"
    await interaction.response.send_message(message)

# Run bot
bot.run(TOKEN)
