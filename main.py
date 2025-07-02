import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('HOGWARTS_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
Hogwarts = commands.Bot(command_prefix='/', intents=intents)

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def save_config(data):
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

@Hogwarts.event
async def on_ready():
    await Hogwarts.tree.sync()
    print(f'O bot {Hogwarts.user} foi iniciado e seus comandos estão sincronizados!')

@Hogwarts.event
async def on_member_join(member):
    print(f"{member.name} entrou no servidor!")
    guild = member.guild

    role = discord.utils.get(guild.roles, name="Membro")

    if role:
        try:
            await member.add_roles(role)
            print(f"Cargo '{role.name}' adicionado ao membro: {member.name}")
        except discord.Forbidden:
            print(f"Permissões insuficientes para adicionar cargo.")
        except Exception as e:
            print("Erro HTTP ao atribuir o cargo: {e}")
    else:
            print(f"Cargo '{role.name}' não encontrado")
            
@Hogwarts.tree.command(name="boas-vindas", description="Define o canal onde as mensagem de boas-vindas serão enviadas")
@app_commands.describe(canal="Escolha o canal")
async def boas_vindas(interaction: discord.Interaction, canal: discord.TextChannel):
    config = load_config()
    config[str(interaction.guild.id)] = canal.id
    save_config(config)
    await interaction.response.send_message(f"Canal de boas-vindas definido como {canal.mention}")

Hogwarts.run(token)