import discord
from discord.ext.commands import has_permissions
import sqlite3
import json
from game_manage import *
from init_bot import *
bot = discord.Bot()

events = []

@bot.event
async def on_ready():
    startBot(bot.user)

@bot.slash_command()
@has_permissions(kick_members=True)
async def create_game(ctx):
    answer = await ctx.respond("Criando jogo...")
    createGame(ctx)
    await ctx.edit(content="Jogo criado! :white_check_mark:")

@bot.slash_command()
async def players_info(ctx):
    db = sqlite3.connect('data.db')
    cur = db.cursor()

    for players in cur.execute('''SELECT playerID, country FROM game'''):
        await ctx.respond(players)
    
@bot.slash_command()
async def join(ctx):
    game = joinGame(ctx)

    if game:
        msg = await ctx.respond("Você entrou nesse jogo")
        await ctx.edit(content="**Escolha seu país:**\n\nImpério Farroupilha\n Império da Mata\n Império Amazonas\n Império do Sertão\n Império Sudestino", view=ChoosingView())
    else:
        await ctx.respond("Você já está cadastrado neste jogo")


@bot.slash_command()
@has_permissions(kick_members=True)  
async def create_channel(ctx, channel_name, emoji, category_id):
    category = bot.get_channel(category_id)
    await category.create_text_channel(f'《{emoji}》{channel_name}')
    

bot.run('ODM3MzUwMTQ4MDY4NjA1OTcy.G6CyCN.3ok0hJEtf9769XpWmQh1twP34s9DxR2dS9Uxbs')