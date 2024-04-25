import os

import discord
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('GUILD_NAME')
PREFIX = "-"

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    if not message.content.startswith(PREFIX):
        return
    command = message.content[1:]
    
    if command.lower().startswith("wiki"):
        def nextTerm(list):
                ret = list[0]
                list.pop(0)
                return ret
        def find_keyword(list, keyword, skip):
            while True:
                cur = nextTerm(list)
                if cur.startswith(keyword):
                    for i in range(skip):
                        cur = nextTerm(list)
                    return cur
        # def trimhtml(html):
        #     return html[html.index('>')+1 : html.index('>')+html[html.index('>'):].index('<')]
        def trimhtml(html):
            rbrac = html.find('>')
            lbrac = html.find('<')
            if rbrac != -1 and lbrac != -1:
                ret = html[:lbrac] + html[rbrac+1:]
                return trimhtml(ret)
            return html
        
        def findnextelement(s, element):
                return s.find_next(id=element)
        def findelement(s, element):
            return s[s.index(element) + len(element) + 1 : s.index(element) + len(element) + s[s.index(element)+len(element)+2:].index('"')+2]
        def fillMessage(value, message):
            ret = value
            for i in range(len(message)-len(value)):
                ret += " "
            return ret
        
        args = command[len("wiki "):]
        link_arg = args.title().replace(" ","_")
        url = 'https://stardewvalleywiki.com/'+link_arg
        response = requests.get(url)
        if response.status_code == 200:            
            with open(args+".html", "w", encoding="utf-8") as file:
                file.write(response.text)
                # file.write(text)
            file.close()

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # title
            cur = soup.find(id="firstHeading")
            title = trimhtml(str(cur))

            # description
            cur = findnextelement(cur, "infoboxdetail")
            desc = trimhtml(str(cur))

            # growth time
            cur = findnextelement(cur, "infoboxdetail")
            cur = findnextelement(cur, "infoboxdetail")
            growth_time = trimhtml(str(cur))

            # season
            cur = findnextelement(cur, "infoboxdetail")
            season = trimhtml(str(cur))

            # xp
            cur = findnextelement(cur, "infoboxdetail")
            XP = trimhtml(str(cur))

            text = soup.get_text()
            text = text.replace("\n","`")
            while text.find("``") != -1:
                text = text.replace("``","`")
            
            texts = text[1:].split('`')
            energy = find_keyword(texts, 'Energy', 1)
            hp = nextTerm(texts)
            ehs = [[energy, hp]]
            inedible = False
            
            for i in range(4):
                if energy == 'Inedible':
                    inedible = True
                    ehs = []
                    nextTerm(texts)
                    break
                energy = nextTerm(texts)
                hp = nextTerm(texts)
                ehs.append([energy, hp])

            next = texts[0]
            sell_prices = []
            print(inedible)

            if next == "Base":
                nextTerm(texts)
                nextTerm(texts)
            
            for i in range(4):
                sell = nextTerm(texts)
                nextTerm(texts)
                sell_prices.append([sell])

            if next == "Base":
                for i in range(4):
                    sell = nextTerm(texts)
                    nextTerm(texts)
                    sell_prices[i].append(sell)

            for a,b in zip(ehs,sell_prices):
                a.append(b[0])
                if next == "Base":
                    a.append(b[1])

            print(ehs)
            if inedible:
                ehstable = (
                    "```"+
                    fillMessage("rarity", "regular ")+"| energy | HP | Sell " + "\n" + 
                    "—————————————————————————————————————\n"+
                    fillMessage("regular", "regular ") + "|" + fillMessage(' Inedible', ' energy | HP ') + '|' + fillMessage(' ' + sell_prices[0][0], " Sell ") + "|" "\n" + 
                    fillMessage("silver", "regular ")  + "|" + fillMessage(' Inedible', ' energy | HP ') + '|' + fillMessage(' ' + sell_prices[1][0], " Sell ") + "|" "\n" + 
                    fillMessage("gold", "regular ")    + "|" + fillMessage(' Inedible', ' energy | HP ') + '|' + fillMessage(' ' + sell_prices[2][0], " Sell ") + "|" "\n" + 
                    fillMessage("iridium", "regular ") + "|" + fillMessage(' Inedible', ' energy | HP ') + '|' + fillMessage(' ' + sell_prices[3][0], " Sell ") + "|" "\n" + 
                    "```"
                )
            elif next == "Base":
                ehstable = (
                    "```"+
                    fillMessage("rarity", "regular ")+"| energy | HP | Base | Tiller" + "\n" + 
                    "—————————————————————————————————————\n"+
                    fillMessage("regular", "regular ") + "|" + fillMessage(" " + ehs[0][0], " energy ") + "|" + fillMessage(" " + ehs[0][1], " HP ") + "|" + fillMessage(" " + ehs[0][2], " Base ") + "|" + fillMessage(" " + ehs[0][3], " Tiller ") + "\n" + 
                    fillMessage("silver", "regular ")  + "|" + fillMessage(" " + ehs[1][0], " energy ") + "|" + fillMessage(" " + ehs[1][1], " HP ") + "|" + fillMessage(" " + ehs[1][2], " Base ") + "|" + fillMessage(" " + ehs[1][3], " Tiller ") + "\n" + 
                    fillMessage("gold", "regular ")    + "|" + fillMessage(" " + ehs[2][0], " energy ") + "|" + fillMessage(" " + ehs[2][1], " HP ") + "|" + fillMessage(" " + ehs[2][2], " Base ") + "|" + fillMessage(" " + ehs[2][3], " Tiller ") + "\n" + 
                    fillMessage("iridium", "regular ") + "|" + fillMessage(" " + ehs[3][0], " energy ") + "|" + fillMessage(" " + ehs[3][1], " HP ") + "|" + fillMessage(" " + ehs[3][2], " Base ") + "|" + fillMessage(" " + ehs[3][3], " Tiller ") + "\n" + 
                    "```"
                )
            else:
                ehstable = (
                    "```"+
                    fillMessage("rarity", "regular ")+"| energy | HP | Sell " + "\n" + 
                    "———————————————————————————\n"+
                    fillMessage("regular", "regular ") + "|" + fillMessage(" " + ehs[0][0], " energy ") + "|" + fillMessage(" " + ehs[0][1], " HP ") + "|" + fillMessage(" " + ehs[0][2], " Sell ") + "\n" + 
                    fillMessage("silver", "regular ")  + "|" + fillMessage(" " + ehs[1][0], " energy ") + "|" + fillMessage(" " + ehs[1][1], " HP ") + "|" + fillMessage(" " + ehs[1][2], " Sell ") + "\n" + 
                    fillMessage("gold", "regular ")    + "|" + fillMessage(" " + ehs[2][0], " energy ") + "|" + fillMessage(" " + ehs[2][1], " HP ") + "|" + fillMessage(" " + ehs[2][2], " Sell ") + "\n" + 
                    fillMessage("iridium", "regular ") + "|" + fillMessage(" " + ehs[3][0], " energy ") + "|" + fillMessage(" " + ehs[3][1], " HP ") + "|" + fillMessage(" " + ehs[3][2], " Sell ") + "\n" + 
                    "```"
                )

            embedVar = discord.Embed(title=title, description=desc, url = url, color=0x00ff00)
            embedVar.add_field(name="Growth Time", value=growth_time, inline=False)
            embedVar.add_field(name="Season", value=season, inline=False)
            embedVar.add_field(name="XP", value=XP, inline=False)
            embedVar.add_field(name="test_table",value=ehstable, inline=False)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("Failed to retrieve webpage: " + args)
client.run(TOKEN)