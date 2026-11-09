import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']
OWNER_ID = int(os.environ['OWNER_ID'])
GUILD_ID = int(os.environ['GUILD_ID'])
if OWNER_ID <= 0 or GUILD_ID <= 0:
    raise RuntimeError('Set nonzero OWNER_ID and GUILD_ID before starting')

MODES = ['Battle Royale', 'Zero Build', 'Reload']
mode = 'Zero Build'
request_pending = False
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

async def allowed(interaction: discord.Interaction) -> bool:
    if interaction.user.id != OWNER_ID or interaction.guild_id != GUILD_ID:
        await interaction.response.send_message('🔒 Private FortBox controller: access denied.', ephemeral=True)
        return False
    return True

class Control(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Search', emoji='🔎', style=discord.ButtonStyle.success, custom_id='fortbox:search')
    async def search(self, interaction: discord.Interaction, button: discord.ui.Button):
        global request_pending
        if not await allowed(interaction): return
        request_pending = True
        await interaction.response.send_message(f'🟡 {mode}: request recorded. Fortnite matchmaking is NOT connected; no match has started.', ephemeral=True)

    @discord.ui.button(label='Cancel', emoji='✖️', style=discord.ButtonStyle.secondary, custom_id='fortbox:cancel')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        global request_pending
        if not await allowed(interaction): return
        request_pending = False
        await interaction.response.send_message('Controller request cleared. No in-game cancellation was performed.', ephemeral=True)

    @discord.ui.button(label='Party', emoji='👑', style=discord.ButtonStyle.primary, custom_id='fortbox:party')
    async def party(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await allowed(interaction): return
        await interaction.response.send_message(party_text(), ephemeral=True)

def party_text():
    return (f'👑 Bot 1 — designated leader (not connected)\n🤖 Bot 2 — not connected\n🤖 Bot 3 — not connected\n'
            f'🎮 Owner — Discord authorized\nMode: {mode}\nRequest pending: {request_pending}\n'
            '⚠️ Fortnite party and matchmaking are not connected.')

@bot.tree.command(name='panel', description='Show the private FortBox control panel')
async def panel(interaction: discord.Interaction):
    if not await allowed(interaction): return
    await interaction.response.send_message('🎮 **FortBox V2** — private control panel\nFortnite matchmaking is not connected.', view=Control(), ephemeral=True)

@bot.tree.command(name='myid', description='Show your own Discord user ID')
async def myid(interaction: discord.Interaction):
    await interaction.response.send_message(f'Your ID: `{interaction.user.id}`', ephemeral=True)

@bot.tree.command(name='mode', description='Select the intended Fortnite mode')
@app_commands.choices(playlist=[app_commands.Choice(name=m, value=m) for m in MODES])
async def set_mode(interaction: discord.Interaction, playlist: app_commands.Choice[str]):
    global mode
    if not await allowed(interaction): return
    mode = playlist.value
    await interaction.response.send_message(f'Mode set to **{mode}** (controller setting only).', ephemeral=True)

@bot.tree.command(name='search', description='Record a search request; does not queue Fortnite')
async def search_cmd(interaction: discord.Interaction):
    global request_pending
    if not await allowed(interaction): return
    request_pending = True
    await interaction.response.send_message(f'🟡 Request recorded for {mode}. No Fortnite match was queued.', ephemeral=True)

@bot.tree.command(name='cancel', description='Clear the controller search request')
async def cancel_cmd(interaction: discord.Interaction):
    global request_pending
    if not await allowed(interaction): return
    request_pending = False
    await interaction.response.send_message('Request cleared. This does not cancel Fortnite matchmaking.', ephemeral=True)

@bot.tree.command(name='party', description='Show planned party and real integration status')
async def party_cmd(interaction: discord.Interaction):
    if not await allowed(interaction): return
    await interaction.response.send_message(party_text(), ephemeral=True)

@bot.event
async def setup_hook():
    bot.add_view(Control())
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

@bot.event
async def on_ready():
    print(f'FortBox V2 online: {bot.user} | Guild: {GUILD_ID}')

bot.run(TOKEN)
