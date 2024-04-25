import os

import discord
from dotenv import load_dotenv
from discord import app_commands

import requests
from bs4 import BeautifulSoup
import pandas as pd

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('GUILD_NAME')
PREFIX = "-"

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    await tree.sync(guild=discord.Object(id=guild.id))
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await client.change_presence(activity=discord.Game("Journey of the Prairie King"))

@tree.command(
    name="wiki",
    description="search the Stardew Valley wiki",
    guild=discord.Object(id=1231735158315548673)
)
async def wiki(interaction, search : str):
    crops = pd.read_csv('crops.csv', dtype = str, sep = ',')
    args = search
    equipments = pd.read_csv('equipments.csv', dtype = str, sep = ',')
    combined = pd.concat([crops['Name'],equipments['Name']], ignore_index=True)
    print(combined)
    if args.lower() == 'catalog':
        ret = ""
        i = 0
        for name in combined.tolist():
            ret += '`'+fill_message(name,'aaaaaaaaaaaaaaa') + "`,"
            i += 1
            if i % 9 == 0:
                ret = ret[:len(ret)-1]
                ret += "\n"
        await interaction.response.send_message("Here's a list of available wiki pages: \n" + ret)
        return
    args = args.title()
    result = crops[crops['Name'] == args]
    crop = True
    if result.empty:
        crop = False
        result = equipments[equipments['Name'] == args]
        if result.empty:
            await interaction.response.send_message("Failed to retrieve page: " + args)
            return
    if crop:
        typ = result['Type'].values[0]
        link_arg = args.title().replace(" ","_")
        wiki = 'https://stardewvalleywiki.com/'
        url = wiki+link_arg
        seed = result['Seed'].values[0]
        growth_time = result['Growth'].values[0]
        season = result['Season'].values[0]
        XP = result['XP'].values[0]
        energy = result['Energy'].values[0]
        HP = result['HP'].values[0]
        base = result['Base'].values[0]
        tiller = result['Tiller'].values[0]
        base_artisan = result['Base Artisan'].values[0]
        artisan = result['Artisan'].values[0]
        desc = result['Description'].values[0]
        response = requests.get(url)
        if response.status_code == 200:            
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tags = soup.find_all('meta')
            image = meta_tags[4].get('content')
        else:
            await interaction.response.send_message("Failed to retrieve webpage: " + args)
            return
        energy = energy.split("/")
        HP = HP.split("/")
        base = base.split("/")
        tiller = tiller.split("/")
        base_artisan = base_artisan.split("/")
        artisan = artisan.split("/")
        if energy[0] == '-':
            energy = ['-','-','-','-']
        print(energy)
        if HP[0] == '-':
            HP = ['-','-','-','-']
        if not tiller[0] == '-':
            ehstable = (
                "```"+
                fill_message("rarity", "regular ")+"| energy | HP | Base | Tiller" + "\n" + 
                fill_line(" rarity  | energy | HP | Base | Tiller ") +
                fill_message("regular", "regular ") + "|" + fill_message(" " + energy[0], " energy ") + "|" + fill_message(" " + HP[0], " HP ") + "|" + fill_message(" " + base[0], " Base ") + "|" + fill_message(" " + tiller[0], " Tiller ") + "\n" + 
                fill_message("silver", "regular ")  + "|" + fill_message(" " + energy[1], " energy ") + "|" + fill_message(" " + HP[1], " HP ") + "|" + fill_message(" " + base[1], " Base ") + "|" + fill_message(" " + tiller[1], " Tiller ") + "\n" + 
                fill_message("gold", "regular ")    + "|" + fill_message(" " + energy[2], " energy ") + "|" + fill_message(" " + HP[2], " HP ") + "|" + fill_message(" " + base[2], " Base ") + "|" + fill_message(" " + tiller[2], " Tiller ") + "\n" + 
                fill_message("iridium", "regular ") + "|" + fill_message(" " + energy[3], " energy ") + "|" + fill_message(" " + HP[3], " HP ") + "|" + fill_message(" " + base[3], " Base ") + "|" + fill_message(" " + tiller[3], " Tiller ") + "\n" + 
                "```"
            )
        else:
            ehstable = (
                "```"+
                fill_message("rarity", "regular ")+"| energy | HP | Base " + "\n" + 
                fill_line(" rarity  | energy | HP | Base ") +
                fill_message("regular", "regular ") + "|" + fill_message(" " + energy[0], " energy ") + "|" + fill_message(" " + HP[0], " HP ") + "|" + fill_message(" " + base[0], " Base ") + "\n" + 
                fill_message("silver", "regular ")  + "|" + fill_message(" " + energy[1], " energy ") + "|" + fill_message(" " + HP[1], " HP ") + "|" + fill_message(" " + base[1], " Base ") + "\n" + 
                fill_message("gold", "regular ")    + "|" + fill_message(" " + energy[2], " energy ") + "|" + fill_message(" " + HP[2], " HP ") + "|" + fill_message(" " + base[2], " Base ") + "\n" + 
                fill_message("iridium", "regular ") + "|" + fill_message(" " + energy[3], " energy ") + "|" + fill_message(" " + HP[3], " HP ") + "|" + fill_message(" " + base[3], " Base ") + "\n" + 
                "```"
            )
        artisan_goods = "``` Base | Artisan \n" + fill_line(" Base | Artisan ")
        for base, artisan in zip(base_artisan, artisan):
            artisan_goods += (
                fill_message(" " + base, " Base ") + "|" + fill_message(" " + artisan, " Artisan ") + "\n"
            )
        artisan_goods += "```"
        embedVar = discord.Embed(title=args, description=desc, url = url, color=0x00ff00)
        embedVar.set_image(url=image)
        embedVar.add_field(name='Growth Time', value=growth_time, inline=False)
        embedVar.add_field(name='Season', value=season, inline=False)
        embedVar.add_field(name='XP', value=XP, inline=False)
        embedVar.add_field(name="Base Goods",value=ehstable, inline=False)
        embedVar.add_field(name="Artisan Goods",value=artisan_goods, inline=False)
        await interaction.response.send_message(embed=embedVar)
        return
        # await message.channel.send("Failed to retrieve webpage: " + args)
    else:
        link_arg = args.title().replace(" ","_")
        wiki = 'https://stardewvalleywiki.com/'
        url = wiki+link_arg
        season = result['Season'].values[0]
        unlock_method = result['Unlock Method'].values[0]
        recipe = result['Recipe'].values[0]
        recipe_cost = result['Recipe Cost'].values[0]
        products = result['Products'].values[0]
        desc = result['Description'].values[0]
        response = requests.get(url)
        if response.status_code == 200:            
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tags = soup.find_all('meta')
            image = meta_tags[4].get('content')
                
        else:
            await interaction.response.send_message("Failed to retrieve webpage: " + args)
            return
        if unlock_method[:-2] == 'Fishing' or unlock_method[:-2] == 'Foraging' or unlock_method[:-2] == 'Farming' or unlock_method[:-2] == 'Mining' or unlock_method[:-2] == 'Combat':
            unlock_method = '['+unlock_method[:-2]+']('+wiki+unlock_method[:-2]+')' + unlock_method[-2:] + "\n"
        recipe_text = "-"
        if not recipe == '-':
            recipe_text = ""
            recipe = recipe.split("/")
            for item in recipe:
                ingred = item[:item.index('(')]
                ingred_url = ingred.replace(" ","_")
                count = item[item.index('(')+1:item.index(')')]
                returl = wiki + ingred_url
                recipe_text += '['+ingred+']('+returl+'): ' + count + "\n"
        prod_text = "-"
        if not products == '-':
            prod_text = ""
            products = products.split("/")
            for item in products:
                prod_url = item.replace(" ","_")
                returl = wiki + prod_url
                prod_text += '['+item+']('+returl+') \n'
            
        embedVar = discord.Embed(title=args, description=desc, url = url, color=0x00ff00)
        embedVar.set_image(url=image)
        if not season == '-':
            embedVar.add_field(name='Season', value=season, inline=False)
        embedVar.add_field(name="Unlock Method",value=unlock_method, inline=False)
        if not recipe_cost == '-':
            embedVar.add_field(name='Recipe Cost', value=recipe_cost, inline=False)
        embedVar.add_field(name="Recipe",value=recipe_text, inline=False)
        embedVar.add_field(name="Products",value=prod_text, inline=False)
        await interaction.response.send_message(embed=embedVar)
        return
        # await message.channel.send("Failed to retrieve webpage: " + args)

def fill_message(value, message):
    ret = value
    for i in range(len(message)-len(value)):
        ret += " "
    return ret
def fill_line(message):
    ret = ""
    for i in range(len(message)):
        ret += "—"
    return ret+"\n"

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    if not message.content.startswith(PREFIX):
        return
    command = message.content[1:]
    
    if command.lower().startswith("wiki"):        
        crops = pd.read_csv('crops.csv', dtype = str, sep = ',')
        args = command[len("wiki "):]

        equipments = pd.read_csv('equipments.csv', dtype = str, sep = ',')

        combined = pd.concat([crops['Name'],equipments['Name']], ignore_index=True)
        print(combined)
        if args.lower() == 'catalog':
            ret = ""
            i = 0
            for name in combined.tolist():
                ret += '`'+fill_message(name,'aaaaaaaaaaaaaaa') + "`,"
                i += 1
                if i % 9 == 0:
                    ret = ret[:len(ret)-1]
                    ret += "\n"
            await message.channel.send("Here's a list of available wiki pages: \n" + ret)
            return

        args = args.title()

        result = crops[crops['Name'] == args]
        crop = True
        if result.empty:
            crop = False
            result = equipments[equipments['Name'] == args]
            if result.empty:
                await message.channel.send("Failed to retrieve page: " + args)
                return
        if crop:
            typ = result['Type'].values[0]
            link_arg = args.title().replace(" ","_")
            wiki = 'https://stardewvalleywiki.com/'
            url = wiki+link_arg
            seed = result['Seed'].values[0]
            growth_time = result['Growth'].values[0]
            season = result['Season'].values[0]
            XP = result['XP'].values[0]
            energy = result['Energy'].values[0]
            HP = result['HP'].values[0]
            base = result['Base'].values[0]
            tiller = result['Tiller'].values[0]
            base_artisan = result['Base Artisan'].values[0]
            artisan = result['Artisan'].values[0]
            desc = result['Description'].values[0]
            response = requests.get(url)
            if response.status_code == 200:            
                soup = BeautifulSoup(response.text, 'html.parser')
                meta_tags = soup.find_all('meta')
                image = meta_tags[4].get('content')
            else:
                await message.channel.send("Failed to retrieve webpage: " + args)
                return
            energy = energy.split("/")
            HP = HP.split("/")
            base = base.split("/")
            tiller = tiller.split("/")
            base_artisan = base_artisan.split("/")
            artisan = artisan.split("/")
            if energy[0] == '-':
                energy = ['-','-','-','-']
            print(energy)
            if HP[0] == '-':
                HP = ['-','-','-','-']
            if not tiller[0] == '-':
                ehstable = (
                    "```"+
                    fill_message("rarity", "regular ")+"| energy | HP | Base | Tiller" + "\n" + 
                    fill_line(" rarity  | energy | HP | Base | Tiller ") +
                    fill_message("regular", "regular ") + "|" + fill_message(" " + energy[0], " energy ") + "|" + fill_message(" " + HP[0], " HP ") + "|" + fill_message(" " + base[0], " Base ") + "|" + fill_message(" " + tiller[0], " Tiller ") + "\n" + 
                    fill_message("silver", "regular ")  + "|" + fill_message(" " + energy[1], " energy ") + "|" + fill_message(" " + HP[1], " HP ") + "|" + fill_message(" " + base[1], " Base ") + "|" + fill_message(" " + tiller[1], " Tiller ") + "\n" + 
                    fill_message("gold", "regular ")    + "|" + fill_message(" " + energy[2], " energy ") + "|" + fill_message(" " + HP[2], " HP ") + "|" + fill_message(" " + base[2], " Base ") + "|" + fill_message(" " + tiller[2], " Tiller ") + "\n" + 
                    fill_message("iridium", "regular ") + "|" + fill_message(" " + energy[3], " energy ") + "|" + fill_message(" " + HP[3], " HP ") + "|" + fill_message(" " + base[3], " Base ") + "|" + fill_message(" " + tiller[3], " Tiller ") + "\n" + 
                    "```"
                )
            else:
                ehstable = (
                    "```"+
                    fill_message("rarity", "regular ")+"| energy | HP | Base " + "\n" + 
                    fill_line(" rarity  | energy | HP | Base ") +
                    fill_message("regular", "regular ") + "|" + fill_message(" " + energy[0], " energy ") + "|" + fill_message(" " + HP[0], " HP ") + "|" + fill_message(" " + base[0], " Base ") + "\n" + 
                    fill_message("silver", "regular ")  + "|" + fill_message(" " + energy[1], " energy ") + "|" + fill_message(" " + HP[1], " HP ") + "|" + fill_message(" " + base[1], " Base ") + "\n" + 
                    fill_message("gold", "regular ")    + "|" + fill_message(" " + energy[2], " energy ") + "|" + fill_message(" " + HP[2], " HP ") + "|" + fill_message(" " + base[2], " Base ") + "\n" + 
                    fill_message("iridium", "regular ") + "|" + fill_message(" " + energy[3], " energy ") + "|" + fill_message(" " + HP[3], " HP ") + "|" + fill_message(" " + base[3], " Base ") + "\n" + 
                    "```"
                )

            artisan_goods = "``` Base | Artisan \n" + fill_line(" Base | Artisan ")

            for base, artisan in zip(base_artisan, artisan):
                artisan_goods += (
                    fill_message(" " + base, " Base ") + "|" + fill_message(" " + artisan, " Artisan ") + "\n"
                )
            artisan_goods += "```"

            embedVar = discord.Embed(title=args, description=desc, url = url, color=0x00ff00)
            embedVar.set_image(url=image)
            embedVar.add_field(name='Growth Time', value=growth_time, inline=False)
            embedVar.add_field(name='Season', value=season, inline=False)
            embedVar.add_field(name='XP', value=XP, inline=False)
            embedVar.add_field(name="Base Goods",value=ehstable, inline=False)
            embedVar.add_field(name="Artisan Goods",value=artisan_goods, inline=False)
            await message.channel.send(embed=embedVar)
            return
            # await message.channel.send("Failed to retrieve webpage: " + args)
        else:
            link_arg = args.title().replace(" ","_")
            wiki = 'https://stardewvalleywiki.com/'
            url = wiki+link_arg

            season = result['Season'].values[0]
            unlock_method = result['Unlock Method'].values[0]
            recipe = result['Recipe'].values[0]
            recipe_cost = result['Recipe Cost'].values[0]
            products = result['Products'].values[0]
            desc = result['Description'].values[0]

            response = requests.get(url)
            if response.status_code == 200:            
                soup = BeautifulSoup(response.text, 'html.parser')
                meta_tags = soup.find_all('meta')
                image = meta_tags[4].get('content')
                    
            else:
                await message.channel.send("Failed to retrieve webpage: " + args)
                return

            if unlock_method[:-2] == 'Fishing' or unlock_method[:-2] == 'Foraging' or unlock_method[:-2] == 'Farming' or unlock_method[:-2] == 'Mining' or unlock_method[:-2] == 'Combat':
                unlock_method = '['+unlock_method[:-2]+']('+wiki+unlock_method[:-2]+')' + unlock_method[-2:] + "\n"

            recipe_text = "-"
            if not recipe == '-':
                recipe_text = ""
                recipe = recipe.split("/")
                for item in recipe:
                    ingred = item[:item.index('(')]
                    ingred_url = ingred.replace(" ","_")
                    count = item[item.index('(')+1:item.index(')')]
                    returl = wiki + ingred_url
                    recipe_text += '['+ingred+']('+returl+'): ' + count + "\n"

            prod_text = "-"
            if not products == '-':
                prod_text = ""
                products = products.split("/")
                for item in products:
                    prod_url = item.replace(" ","_")
                    returl = wiki + prod_url
                    prod_text += '['+item+']('+returl+') \n'
                
            embedVar = discord.Embed(title=args, description=desc, url = url, color=0x00ff00)
            embedVar.set_image(url=image)
            if not season == '-':
                embedVar.add_field(name='Season', value=season, inline=False)
            embedVar.add_field(name="Unlock Method",value=unlock_method, inline=False)
            if not recipe_cost == '-':
                embedVar.add_field(name='Recipe Cost', value=recipe_cost, inline=False)
            embedVar.add_field(name="Recipe",value=recipe_text, inline=False)
            embedVar.add_field(name="Products",value=prod_text, inline=False)
            await message.channel.send(embed=embedVar)
            return
            # await message.channel.send("Failed to retrieve webpage: " + args)


client.run(TOKEN)