Starfruit Bot
---
Starfruit Bot is a Discord bot meant to easen your Stardew Valley experience.

**Add the bot to your server:** [OAuth Link](https://discord.com/oauth2/authorize?client_id=1232793127031672904)

Functionalities of Starfruit Bot:
- '-wiki arg'
  - searches the Stardew Valley wiki for 'arg'

| ![crop-search](https://github.com/kangheel/starfruit-bot/assets/27700068/fbb28832-9a6f-4405-b323-0802c935aa0a) | ![equipment-search](https://media.discordapp.net/attachments/1184748696215224330/1233019287288021073/image.png?ex=662b9232&is=662a40b2&hm=a732d7e183377e086ee1cdea722046f59c06fdc8521393cddb6a687ae40e87f5&=&format=webp&quality=lossless) |
| -- | -- |

- '-wiki catalog'
  - brings up a list of pages you can view
![catalog](https://cdn.discordapp.com/attachments/1184748696215224330/1233020153814319134/image.png?ex=662b9301&is=662a4181&hm=a79370af9f1748c2a12fc3175603de101f8f9f6928b57166b2143804a9e83b9b&)

How to run your own fork of the bot:
1. Prerequisites: python3, discord.py, dotenv, requests, bs4, pandas
   - install python3 first then run the following command for the packages
   - pip install 'package-name'
3. Download the files
4. Generate your discord bot and token
5. Make a .env file in your directory with the following two lines
   - BOT_TOKEN = 'your-bot-token'
   - GUILD_NAME = 'your-guild-name'
6. Run 'wiki_reader.py' and the bot should be up and running!
