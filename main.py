import discord
from discord.ext import commands
import pandas as pd
from bs4 import BeautifulSoup
import requests

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    
@bot.command()
async def jogos(ctx):
    try:

        url = "https://api.pandascore.co/csgo/matches?filter[status]=running"
        headers = {
            "Authorization": "Bearer TOKEN_API_PANDASCORE"  
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            jogos = response.json()
            
            if not jogos:
                await ctx.send("**Não há jogos de CS:GO em andamento no momento.**")
                return
            
            mensagem = "**Jogos de CS:GO em andamento:**\n\n"
            
            for jogo in jogos[:10]:  
                nome = jogo['name']
                equipe1 = jogo['opponents'][0]['opponent']['name'] if jogo['opponents'] and len(jogo['opponents']) > 0 else "Equipe 1 não definida"
                equipe2 = jogo['opponents'][1]['opponent']['name'] if jogo['opponents'] and len(jogo['opponents']) > 1 else "Equipe 2 não definida"
                horario = jogo['scheduled_at']
                
                mensagem += f"**{nome}**\n🆚 {equipe1} vs {equipe2}\n⏰ Horário: {horario}\n\n"
            
            await ctx.send(mensagem)
        else:
            await ctx.send("Erro ao buscar jogos. Tente novamente mais tarde.")
    
    except Exception as e:
        print(f"Erro no comando !jogos: {e}")
        await ctx.send(f"Ocorreu um erro ao buscar os jogos: {e}")

bot.run("BOT_TOKEN_DISCORD")
