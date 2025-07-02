# Importa bibliotecas e utilitários
import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo '.env' e obtém o token do bot
load_dotenv()
token = os.getenv('HOGWARTS_TOKEN')

# Define as permissões do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
Hogwarts = commands.Bot(command_prefix='/', intents=intents)

# Carrega os aniversários do arquivo JSON, se existirem, ou retorna um dicionário vazio
def load_birthdays():
    if os.path.exists("aniversários.json"):
        try:
            with open("aniversários.json", "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Erro: Arquivo JSON corrompido!")
        except FileNotFoundError:
            print("Error: Arquivo não encontrado!")
    return {}

# Salva os aniversários em formato JSON com indentação
def save_birthdays(data):
    with open("aniversários.json", "w") as f:
        json.dump(data, f, indent=4)

birthdays = load_birthdays()

# Carregar as configurações do arquivo 'config.json'
def load_config():
    try:
        # Abre o arquivo 'config.json' no modo de leitura
        with open("config.json", "r") as f:
            return json.load(f) # Carrega e retorna os dados em formato de dicionário
    except FileNotFoundError:
        # Retorna um arquivo vazio se o dicionário não for encontrado
        return {}

# Salvar as configurações no arquivo 'config.json'
def save_config(data):
     # Abre o arquivo 'config.json' no modo de escrita
    with open("config.json", "w") as f:
        # Salva os dados no arquivo com indentação de 4 espaços para facilitar a leitura
        json.dump(data, f, indent=4)

# Evento disparado quando o bot estiver conectado
@Hogwarts.event
async def on_ready():
    await Hogwarts.tree.sync()
    print(f'O bot {Hogwarts.user} foi iniciado e seus comandos estão sincronizados!')

# Comando para atribuir o cargo 'Membro' automaticamente e enviar mensagem de boas-vindas a novos usuários
@Hogwarts.event
async def on_member_join(member):
    print(f"{member.name} entrou no servidor!")
    guild = member.guild

    # Adiciona o cargo 'Membro'
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
           print(f"Cargo não encontrado")

    # Busca o canal de boas-vindas configurado
    config = load_config()
    channel_id = config.get(str(guild.id))
    if not channel_id:
        print(f"Nenhum canal configurado para o servidor '{guild.name}' (ID: {guild.id}).")
        return
    else:
        print(f"Canal configurado para o servidor '{guild.name}': ID {channel_id}")

    # Verifica se o canal ainda existe no servidor
    channel = guild.get_channel(channel_id)
    if not channel:
        print(f"Canal com ID {channel_id} não encontrado no servidor '{guild.name}'!")
        return
    else:
        print(f"Canal encontrado: #{channel.name} (ID: {channel.id})")

    # Envia mensagem de boas-vindas para novos membros
    try:
        await channel.send(
            f"Prezado(a) Sr.(a) {member.mention}, temos o prazer de informar que V. Sa. tem uma vaga na Escola de Magia e Bruxaria de Hogwarts. Estamos anexando uma lista dos livros e equipamentos necessários. O ano letivo começa em 1º de setembro! Aguardamos sua coruja até 31 de julho, no mais tardar. 🧙‍♂️"
        )
        print(f"Mensagem de boas-vindas enviada para {member.name} no canal #{channel.name}")
    except Exception as e:
        print(f"Falha ao enviar mensagem de boas-vindas: {e}")
            
# Comando para escolher o canal da mensagem de boas-vindas
@Hogwarts.tree.command(name="boas-vindas", description="Define o canal onde as mensagem de boas-vindas serão enviadas")
@app_commands.describe(canal="Escolha o canal")
async def boas_vindas(interaction: discord.Interaction, canal: discord.TextChannel):
    config = load_config()
    config[str(interaction.guild.id)] = canal.id
    save_config(config)
    await interaction.response.send_message(f"Canal de boas-vindas definido como {canal.mention}")

# Comando para escolher o canal de aniversários
@Hogwarts.tree.command(name="canal-aniversário", description="Defina o canal onde as mensagens de aniversário serão enviadas")
@app_commands.describe(canal="Escolha o canal")
async def set_aniversario(interaction: discord.Interaction, canal: discord.TextChannel):
    config = load_config()
    config[str(interaction.guild.id)] = canal.id
    save_config(config)
    await interaction.response.send_message(f"Canal de aniversáiro definido como {canal.mention}")

# Carrega o bot
Hogwarts.run(token)