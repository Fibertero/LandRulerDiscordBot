import sqlite3
from sqliteHelper import *
import discord

def createGame(ctx):
    db = sqlite3.connect('data.db')
    cur = db.cursor()

    #Creating the game db
    cur.execute('''CREATE TABLE IF NOT EXISTS game(player text, playerId integer, country text, wood integer, wheat integer, oil integer)''')
    db.commit()
    db.close()


def joinGame(ctx):
    db = sqlite3.connect('data.db')
    cur = db.cursor()
    #check if the player is already logged in
    for id in cur.execute('SELECT playerId FROM game'):
        if checkValues(ctx.author.id, id):
            return False
            break 
    else:
        # Add player at the game
        cur.execute('''INSERT INTO game VALUES(?,?,?,?,?,?)''', [str(ctx.author.name), str(ctx.author.id), "", 500, 500, 500])
        db.commit()
        return True

class ChoosingView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Escolha um país para jogar!", 
        min_values = 1, 
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                label="Império do Sertão",
                description="Clique aqui para governar o Império da Sertão"
            ),
            discord.SelectOption(
                label="Império do Amazonas",
                description="Clique aqui para governar o Império da Amazonas"
            ),
            discord.SelectOption(
                label="Império Farroupilha",
                description="Clique aqui para governar o Império da Farroupilha"
            ),
            discord.SelectOption(
                label="Império Sudestino",
                description="Clique aqui para governar o Império da Sudestino"
            ),
            discord.SelectOption(
                label="Império da Mata",
                description="Clique aqui para governar o Império da Mata"
            )
        ]

    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        db = sqlite3.connect('data.db')
        cur = db.cursor()
        #Define the forbidden countrys characters
        forbidden_characters = "'()[],"
        # List of countrys that are already selected
        countrys_already_selected = []
        # Fill the countrys_already_selected list
        for countrys in cur.execute('''SELECT country FROM game'''):
            newCountryName = str(countrys)
            for i in range(0, len(forbidden_characters)):
                newCountryName = newCountryName.replace(forbidden_characters[i], "")

            countrys_already_selected.append(str(newCountryName))
        # Check if the selected country are already selected
        if str(select.values[0]) in countrys_already_selected:
            await interaction.response.send_message(f"O país {select.values[0]} já foi selecionado. Selecione outro, por favor.")
        else:
            cur.execute(f'''UPDATE game SET country=? WHERE playerId=?''', [str(select.values[0]), interaction.user.id])
            db.commit()
            await interaction.response.send_message(f"O país {select.values[0]} foi selecionado. Aproveite a partida!")
