import discord
from discord.ext import commands
import requests
import os
import random

#MTM2NTAwMjkxNzMyODg1MDk4NA.GA7kdT.zexIq-sF8ttI1cwzSzSJVi1gKUXPAt16G2a37c - Token Bot
# 1726e65078ed4681a86989ca49624e7b - API KEY
# ifrZU8JBebN9Ryg0QfhpEGtH4QTAJUPP5Ul1U7Z6xyJno5DdJ20 - Pandascore


NEWS_API_KEY = "1726e65078ed4681a86989ca49624e7b"    
DISCORD_TOKEN = "MTM2NTAwMjkxNzMyODg1MDk4NA.GA7kdT.zexIq-sF8ttI1cwzSzSJVi1gKUXPAt16G2a37c"
PANDASCORE_API_KEY = "ifrZU8JBebN9Ryg0QfhpEGtH4QTAJUPP5Ul1U7Z6xyJno5DdJ20"



intents = discord.Intents.all()
bot = commands.Bot("!", intents=intents)

def get_news(query="FURIA esports CS:GO", language="pt"):
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        if articles:
            news = []
            for article in articles[:5]:  
                news.append(f"**{article['title']}**\n{article['url']}")
            return news
        else:
            return ["Nenhuma notícia encontrada sobre a FURIA no momento."]
    else:
        return [f"Erro ao acessar a API de notícias: {response.status_code}"]
    
def get_furia_games():
    url = "https://api.pandascore.co/csgo/matches/upcoming"
    headers = {"Authorization": f"Bearer {PANDASCORE_API_KEY}"}
    
   
    response = requests.get(url, headers=headers)
    
    
    print(f"URL chamada: {url}")
    print(f"Headers enviados: {headers}")
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    
    if response.status_code == 200:
        try:
            matches = response.json()
          
            furia_matches = [
                match for match in matches if "FURIA" in (team.get("name", "Desconhecido") for team in match.get("opponents", []))
            ]
            if furia_matches:
                games = []
                for match in furia_matches[:5]:  
                    date = match.get("begin_at", "Data não disponível")
                    opponents = " vs ".join(team.get("name", "Equipe Desconhecida") for team in match.get("opponents", []))
                    tournament = match.get("tournament", {}).get("name", "Torneio Desconhecido")
                    games.append(f"**Data:** {date} | **Jogo:** {opponents} | **Torneio:** {tournament}")
                return games
            else:
                return ["Nenhum jogo da FURIA encontrado nos próximos dias."]
        except Exception as e:
            return [f"Erro ao processar dados da API: {e}"]
    else:

        return [f"Erro ao acessar a API: {response.status_code} - {response.text}"]
    
def get_team_stats(team_name="FURIA"):
    url = f"https://api.pandascore.co/csgo/teams?search[slug]={team_name.lower()}"
    headers = {"Authorization": f"Bearer {PANDASCORE_API_KEY}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            team_data = response.json()
            if team_data:
                team = team_data[0]
                name = team.get("name", "Desconhecido")
                acronym = team.get("acronym", "N/A")
                ranking = team.get("rank", "Não ranqueado")
                players = team.get("players", [])
                
                player_stats = []
                for player in players:
                    player_name = player.get("name", "Desconhecido")
                    player_role = player.get("role", "Função não disponível") 
                    if player_role is None or player_role.strip() == "":
                        player_role = "Função não especificada"

                    player_stats.append(f"🌟 **Jogador:** {player_name}\n💼 **Função:** {player_role}")
                
                return [
                    f"👾 **Equipe:** {name} ({acronym})\n🌍 **Ranking Mundial:** {ranking}\n",
                    "🎮 **Estatísticas dos jogadores:**",
                    *player_stats
                ]
            else:
                return ["⚠️ Opa, parece que não encontramos informações sobre o time especificado! Tente novamente mais tarde."]
        except Exception as e:
            return [f"❌ Putz! Algo deu errado ao processar os dados. Aqui está o erro técnico: {e}"]
    else:
        return [f"❌ Ops! Não conseguimos acessar os dados da API. Código de erro: {response.status_code} - {response.text}"]
    


furia_memes = [
    "https://pbs.twimg.com/media/EuXFD3PXUAAR4OH.jpg",
    "https://s2.glbimg.com/fTZIKsUqStwdFNEvTZPegqT4xm0=/0x0:628x562/984x0/smart/filters:strip_icc()/s.glbimg.com/es/ge/f/original/2019/06/07/meme_furia.jpeg",
    "https://pbs.twimg.com/media/E3icwitXoAU-zFq.jpg"
]


@bot.event
async def on_member_join(member:discord.Member):

        channel = bot.get_channel(1365389204439433316)
        await channel.send (f"🎉 Olá, {member.mention}! Seja muito bem-vindo(a) ao **{member.guild.name}**! 🐯\n"
            "💬 Sinta-se à vontade para explorar e interagir com a galera.\n"
            "✨ Não esqueça de conferir as regras no canal correspondente!\n"
            "Divirta-se e vamos rugir juntos com a FURIA! 🐾🔥\n"
            "https://cdn.dribbble.com/userupload/11627518/file/original-7bbb026895a1d34240048e24e5e912e9.gif\n")
    
    
@bot.event
async def on_ready():
    print(f"🚀 | Bot da FURIA pronto para agitar o servidor com novidades e estatísticas! Vamos nessa!")
    await bot.change_presence(activity=discord.Game(name="na 🔥 FURIA!"))

@bot.command(name="noticias")
async def noticias(ctx):
    await ctx.send("> __ 📰 **Estamos procurando as últimas manchetes sobre a FURIA... Prepare-se para ficar por dentro!** 🕵️ __")
    news = get_news()
    for item in news:
        await ctx.send(item)
        
@bot.command(name="jogos")
async def jogos(ctx):
    await ctx.send("> __ ⚔️ **Procurando os próximos confrontos da FURIA... Que a batalha comece!** 🏆 __")
    games = get_furia_games()
    for game in games:
        await ctx.send(game)
        
@bot.command(name="ranking")
async def ranking(ctx):
    await ctx.send("> __ 🔍 **Preparando informações detalhadas sobre a FURIA... Segure firme!** 🏆 __" )
    stats = get_team_stats()
    for stat in stats:
        await ctx.send(stat)
        
@bot.command(name="meme")
async def meme_furia(ctx):
    await ctx.send("> __ 🐯 **Aqui está um meme exclusivo da FURIA!** 🎮 __")
    meme_url = random.choice(furia_memes)
    await ctx.send(meme_url)

bot.run("MTM2NTAwMjkxNzMyODg1MDk4NA.GA7kdT.zexIq-sF8ttI1cwzSzSJVi1gKUXPAt16G2a37c")