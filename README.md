# Hogwarts Discord Bot
Um bot personalizado para servidores do Discord inspirado no universo de **Harry Potter**!
Este bot automatiza mensagens de boas-vindas, registro de aniversários e envio automático de felicitações.

## Funcionalidades
- <b>Mensagens de Boas-Vindas:</b> Envia mensagens temáticas ao estilo Hogwarts para novos membros ao entrarem no servidor.
- <b>Lembretes de Aniversário:</b> Permite que usuários registrem seus aniversários e envia automaticamente uma mensagem especial no dia.
- <b>Personalização de Canais:</b> Admins podem configurar os canais onde as mensagens de boas-vindas e de aniversário serão enviadas.
- <b>Mensagens de Aniversário Personalizadas:</b> Admins podem definir mensagens personalizadas com a variável {user} para mencionar o aniversariante.

## Instalação
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/hogwarts-discord-bot.git
cd hogwarts-discord-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo .env com o token do seu bot:
```bash
pip install -r requirements.txt
```

4. Certifique-se de que os arquivos `config.json`, `aniversários.json` e `mensagens.json` existam (podem começar vazios).

 5. Execute o bot:
```bash
python -3 nome_do_arquivo.py
```

## Comandos Disponíveis

| Comando                     | Descrição                                                                       |
| --------------------------- | ------------------------------------------------------------------------------- |
| `/boas-vindas`              | Define o canal onde a mensagem de boas-vindas será enviada                      |
| `/canal-aniversário`        | Define o canal onde as mensagens de aniversário serão enviadas                  |
| `/meu-aniversário`          | Registra seu dia e mês de aniversário do usuário                                |
| `/mensagem-=aniversário`    | Define uma mensagem de aniversário personalizada (com {user} para menção)       |

## Estrutura de Arquivos
- `aniversários.json:` Armazena os aniversários registrados.
- `config.json:` Configurações por servidor (canais de boas-vindas e aniversários).
- `mensagens.json:` Mensagens de aniversário personalizadas por servidor.
- `.env:` Contém o token do bot.
- `requirements.txt:` Bibliotecas necessárias.

## Permissões Necessárias
O bot precisa das seguintes permissões para funcionar corretamente:
- Gerenciar Cargos (para atribuir o cargo "Membro")
- Ler e Enviar Mensagens
- Usar comandos de aplicação (Slash Commands)

## Exemplo de Boas-Vindas
> Prezado(a) Sr.(a) {member.mention}, temos o prazer de informar que V. Sa. tem uma vaga na <b>Escola de Magia e Bruxaria de Hogwarts.</b> Estamos anexando uma lista dos livros e equipamentos necessários. O ano letivo começa em 1º de setembro! Aguardamos sua coruja até 31 de julho, no mais tardar. 🧙‍♂️

## Agendamento de Aniversários
O bot verifica aniversários diariamente às 00:00 (horário de São Paulo) e envia a mensagem no canal configurado.

## Licença
Este projeto está licenciado sob a MIT License.