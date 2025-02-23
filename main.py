import tweepy
import discord
import asyncio
from discord.ext import commands, tasks


TWITTER_API_KEY = "****5x0S1W"
TWITTER_API_SECRET = "****5x0S1W"
TWITTER_ACCESS_TOKEN = "1716846301583724544-J1XoXESGUn3GugNrUQc0NIX9Fh9793"
TWITTER_ACCESS_SECRET = "joSr9uFJ6w21RXZd2R8PosjQoO2OttUd2yPPwaT2vRKfL"

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

#
DISCORD_TOKEN = "MTM0MzMwODc2OTY4MDk0OTM2MA.GmHnjE.3tn9bKbBIpFiI_7J3p5sB6U9oQ5_qvqPR3ozzY"
CHANNEL_ID = 1339072257707868233

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


ultimo_tweet_id = None

@tasks.loop(minutes=1)
async def verificar_tweets():
    global ultimo_tweet_id
    try:
        
        tweets = api.user_timeline(screen_name="Iannzits", count=5, tweet_mode="extended")
        
        for tweet in reversed(tweets):
            if ultimo_tweet_id is None or tweet.id > ultimo_tweet_id:
                
                palavras_proibidas = ["RT", "Retuitado", "Retweet", "curta o post"]
                if any(palavra in tweet.full_text for palavra in palavras_proibidas):
                    continue
                
                
                texto_formatado = tweet.full_text.replace("iannzits", "Spindula")

                
                embed = discord.Embed(
                    title="NOVIDADES E VAZAMENTOSSS!",
                    description=texto_formatado,
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Post original de @Iannzits")

                
                if "media" in tweet.entities:
                    for media in tweet.entities["media"]:
                        embed.set_image(url=media["media_url"])

                
                canal = bot.get_channel(CHANNEL_ID)
                if canal:
                    await canal.send(embed=embed)

                
                ultimo_tweet_id = tweet.id

    except Exception as e:
        print(f"Erro ao verificar tweets: {e}")

@bot.event
async def on_ready():
    print(f"Bot {bot.user} está online!")
    verificar_tweets.start()  

bot.run("MTM0MzMwODc2OTY4MDk0OTM2MA.GmHnjE.3tn9bKbBIpFiI_7J3p5sB6U9oQ5_qvqPR3ozzY")