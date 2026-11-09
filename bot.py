import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']
OWNER_ID = int(os.environ.get('OWNER_ID', '0'))
GUILD_ID = int(os.environ.get('GUILD_ID', '0'))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
selected_mode = 'Zero Build'
request_pending = False

epic = None
if os.environ.get('OWNER_EPIC_NAME'):
    from epic_client import FortBoxClient
    epic = FortBoxClient()


@bot.event
async def setup_hook():
    if epic:
        bot._epic_task = asyncio.create_task(epic.start())

async def authorized(interaction: discord.Interaction) -> bool:
    if OWNER_ID and interaction.user.id != OWNER_ID:
        await interaction.response.send_message('FortBox is private.', ephemeral=True)
        return False
    return True

@bot.tree.command(name='myid', description='Show your Discord User ID privately')
async def myid(interaction: discord.Interaction):
    await interaction.response.send_message(f'Your Discord User ID: `{interaction.user.id}`', ephemeral=True)

@bot.tree.command(name='mode', description='Select a Fortnite playlist (controller setting only)')
@app_commands.choices(mode=[app_commands.Choice(name=m, value=m) for m in ['Battle Royale', 'Zero Build', 'Reload']])
async def mode(interaction: discord.Interaction, mode: app_commands.Choice[str]):
    global selected_mode
    if not await authorized(interaction): return
    selected_mode = mode.value
    note = await epic.apply_mode(selected_mode) if epic else 'Epic bot not enabled (set OWNER_EPIC_NAME).'
    await interaction.response.send_message(f'Mode set to **{selected_mode}**. {note} Press Play in-game to queue.', ephemeral=True)

@bot.tree.command(name='search', description='Create a matchmaking request (not connected to Fortnite)')
async def search(interaction: discord.Interaction):
    global request_pending
    if not await authorized(interaction): return
    request_pending = True
    await interaction.response.send_message(f'🎮 Search requested for **{selected_mode}**. ⚠️ Fortnite matchmaking is NOT connected; no game was queued.', ephemeral=True)

@bot.tree.command(name='cancel', description='Cancel the pending controller request')
async def cancel(interaction: discord.Interaction):
    global request_pending
    if not await authorized(interaction): return
    request_pending = False
    await interaction.response.send_message('Controller request cancelled. This does not cancel in-game matchmaking.', ephemeral=True)

@bot.tree.command(name='party', description='View intended party configuration')
async def party(interaction: discord.Interaction):
    if not await authorized(interaction): return
    status = epic.party_summary() if epic else 'Epic bot not enabled (set OWNER_EPIC_NAME).'
    await interaction.response.send_message(f'{status}\nMode: {selected_mode}\nRequest pending: {request_pending}', ephemeral=True)

@bot.event
async def on_ready():
    if not getattr(bot, '_synced', False):
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
        else:
            await bot.tree.sync()
        bot._synced = True
    print(f'FortBox logged in as {bot.user}')

bot.run(TOKEN)
