from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID', "14438288")
API_HASH = environ.get('API_HASH', "51111ec90615944db5863c0b52e8d29c")
BOT_TOKEN = environ.get('BOT_TOKEN', "5635471956:AAGY7drOf95812iLUwtv_3MA2i5gJ62QJTE")
API_KEY = {}

bot = Client('gplink bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm DoLinker bot. Just send me link and get short link")

@bot.on_message(filters.private & filters.command('set_api'))
async def set_api(bot, message): 
    if len(message.command) == 1: 
        await message.reply("Give your API with command!", quote=True) 
        return 
    API_KEY[str(message.from_user.id)] = message.text
    await message.reply_text("API Set Successfully!", quote=True)

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        KEY = API_KEY.get(str(message.from_user.id))
        if KEY is None:
            await messagr.reply('Add you API using /set_api first!', quote=True)
            return
        short_link = await get_shortlink(link, KEY)
        await message.reply(f'Here is your [short link]({short_link})', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link, KEY):
    url = 'https://dolinker.ml/api'
    params = {'api': KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]

bot.run()
