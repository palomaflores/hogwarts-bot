import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('HOGWARTS_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
Hogwarts = commands.Bot(command_prefix='/', intents=intents)

@Hogwarts.event
async def on_ready():
    await Hogwarts.tree.sync()
    print(f'O bot {Hogwarts.user} foi iniciado e seus comandos estão sincronizados!')

Hogwarts.run(token)