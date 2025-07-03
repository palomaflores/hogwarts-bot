# Importa bibliotecas e utilitários
import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
from datetime import datetime, time
from zoneinfo import ZoneInfo
from datetime import time as dt_time
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

# Carregar as configurações do arquivo 'config.json'
def load_config():
    try:
        # Abre o arquivo 'config.json' no modo de leitura
        with open("config.json", "r") as f:
            return json.load(f) # Carrega e retorna os dados em formato de dicionário
    except (FileNotFoundError, json.JSONDecodeError):
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
    check_birthdays.start()
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
            print(f"Erro HTTP ao atribuir o cargo: {e}")
    else:
           print(f"Cargo não encontrado")

    # Busca o canal de boas-vindas configurado
    config = load_config()
    guild_config = config.get(str(guild.id), {})
    channel_id = guild_config.get("boas_vindas")
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
    guild_id = str(interaction.guild.id)

    if guild_id not in config or not isinstance(config[guild_id], dict):
        config[guild_id] = {}

    config[guild_id]["boas_vindas"] = canal.id
    save_config(config)
    await interaction.response.send_message(f"Canal de boas-vindas definido como {canal.mention}")

# Comando para registrar aniversário
@Hogwarts.tree.command(name="meu-aniversário", description="Registre seu aniversário!")
@app_commands.describe(
    day="Dia do seu aniversário",
    month="Mês do seu aniversário"
)
async def my_birthday(interaction: discord.Interaction, day: int, month: int):
    try:
        # Valida se o dia/mês formam uma data válida (ano fixo apenas para validação)
        datetime(year=2000, month=month, day=day)
    except ValueError:
        await interaction.response.send_message(
            "Data inválida. Use um dia e mês corretos"
        )
        return
    
    # Carrega os aniversários salvos, salva a data do usuário que executou o comando e atualiza o arquivo com o novo aniversário
    data = load_birthdays()
    data[str(interaction.user.id)] = {"day": day, "month": month}
    save_birthdays(data)

    await interaction.response.send_message(
        f"Aniversário registrado para **{day:02d}/{month:02d}**, {interaction.user.mention}!",
    )
    
# Comando para escolher o canal de aniversários
@Hogwarts.tree.command(name="canal-aniversário", description="Defina o canal onde as mensagens de aniversário serão enviadas")
@app_commands.describe(canal="Escolha o canal")
async def set_aniversario(interaction: discord.Interaction, canal: discord.TextChannel):
    config = load_config()
    # Obtém o ID do servidor (guild) como uma string
    guild_id = str(interaction.guild.id)

    # Verifica se o servidor ainda não possui configurações salvas
    if guild_id not in config:
        config[guild_id] = {} # Cria uma nova entrada para o servidor

    # Define o ID do canal onde as mensagens de aniversário serão enviadas
    config[guild_id]["aniversario"] = canal.id
    save_config(config)
    
    await interaction.response.send_message(f"Canal de aniversário definido como {canal.mention}")

# Tarefa que roda a cada 1 minuto para verificar aniversários
@tasks.loop(minutes=1)
async def check_birthdays():
    await Hogwarts.wait_until_ready()
    
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    if now.hour != 21 or now.minute != 50:
        return

    # Carrega os dados de aniversários e configurações dos servidores
    birthdays = load_birthdays()
    config = load_config()

    # Itera sobre todos os servidores em que o bot está
    for guild in Hogwarts.guilds:
        guild_config = config.get(str(guild.id), {})
        channel_id = guild_config.get("aniversario")
        
        if not channel_id:
            print(f"Nenhum canal configurado para aniversários em {guild.name}")
            continue

        channel = guild.get_channel(channel_id)
        if not channel:
            print(f"Canal não encontrado no servidor {guild.name}")
            continue

        # Itera sobre os aniversários registrados
        for user_id, date in birthdays.items():
            if date["day"] == now.day and date["month"] == now.month:
                try:
                    # Busca o membro no servidor usando o ID
                    user = await guild.fetch_member(int(user_id))
                except discord.NotFound:
                     # Se o usuário não estiver mais no servidor, ignora
                    continue

                try:
                     # Carrega uma mensagem personalizada de aniversário, se houver
                    with open("mensagens.json", "r", encoding="utf-8") as f:
                        mensagens = json.load(f)
                    mensagem = mensagens.get(str(guild.id))
                except FileNotFoundError:
                    mensagem = None

                 # Mensagem padrão caso não tenha uma personalizada
                if not mensagem:
                    mensagem = "{user}, feliz aniversário! Esperamos que o seu dia seja tão incrível quanto um banquete no Salão Principal! 🎂"

                # Substitui o placeholder {user} pela menção do usuário            
                mensagem_final = mensagem.replace("{user}", user.mention)

                embed = discord.Embed(
                    title="FELIZ ANIVERSÁRIO!",
                    description=mensagem_final,
                    color=discord.Color.gold()
                )
                
                # Envia a mensagem no canal configurado, com menção ao usuário
                await channel.send(embed=embed, allowed_mentions=discord.AllowedMentions(users=True))

# Comando para configurar mensagem de feliz aniversário
@Hogwarts.tree.command(name="mensagem-aniversario", description="Configure a mensagem personalizada de feliz aniversário.")
@app_commands.describe(mensagem="Use {user} para mencionar o aniversariante automaticamente.")
async def set_birthday_message(interaction: discord.Interaction, mensagem: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Apenas administradores podem usar este comando.")
        return

    # Carrega o arquivo de mensagens personalizadas
    try:
        with open("mensagens.json", "r", encoding="utf-8") as f:
            mensagens = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        mensagens = {}

    mensagens[str(interaction.guild.id)] = mensagem

    # Salva a mensagem personalizada no arquivo 'mensagens.json'
    with open("mensagens.json", "w", encoding="utf-8") as f:
        json.dump(mensagens, f, indent=4, ensure_ascii=False)

    await interaction.response.send_message("Mensagem de aniversário configurada com sucesso!")

Hogwarts.run(token)