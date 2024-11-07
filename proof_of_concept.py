from dotenv import load_dotenv
from telethon import TelegramClient
import pandas as pd
import os
import time

load_dotenv()
api_id = os.getenv('BOT_API_ID')
api_hash = os.getenv('BOT_API_HASH')

# Channels to scrape stickers from
chanels = pd.read_json('chanels.json')['chanels']
for chanel in chanels:
    if chanel.get('min_id', None) == None:
        chanel['min_id'] = 0

'''
d_min = 1  # Start day (inclusive)
m_min = 1  # Start month
y_min = 2000  # Start year
d_max = 1  # End day (exclusive)
m_max = 8  # End month
y_max = 2024  # End year
file_name = 'Test'  # Output file name
key_search = ''  # Keyword to search, leave empty if not needed
max_t_index = 1000000  # Maximum number of messages to scrape
time_limit = 6 * 60 * 60  # Timeout in hours (*seconds)
File = 'parquet'  # Set to 'parquet' or 'excel'

data = []  # List to store scraped data
t_index = 0  # Tracker for the number of messages processed
start_time = time.time()
'''

# Initialize the client
bot = TelegramClient(session='sticker_scraper',api_id=api_id,api_hash=api_hash)
async def scrape_and_send_stickers():
    # Channels to scrape stickers from
    for chanel in chanels:
        name = chanel['name']
        min_id = chanel['min_id']
        try:
            async for message in bot.iter_messages(entity=name, limit=100000, min_id=min_id):
                # Filter only sticker messages
                if message.sticker:
                    # Send the sticker to yourself
                    await bot.send_file('me', message.media)
                    print(f"Sticker {message.sticker} sent to 'me' from {chanel}")
        except Exception as e:
            print(f"Error in channel {chanel}: {e}")
    await bot.disconnect()

with bot:
    bot.loop.run_until_complete(scrape_and_send_stickers())