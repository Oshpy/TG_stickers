from dotenv import load_dotenv, find_dotenv
from telethon import TelegramClient
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
import json
import pandas as pd
import os
import time

load_dotenv(find_dotenv('credentials.env'))
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
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

def create_folder(folder):
    if os.path.isdir(folder):
        pass
    else:
        os.makedirs(folder,exist_ok=True)

# Initialize the client
client = TelegramClient(session='sticker_scraper',api_id=api_id,api_hash=api_hash)
main_folder = "stickers"
create_folder(main_folder)

try:
    with open('scraped_stickers.json', 'r') as file:
        stickers_dict = json.load(file)
except:
    stickers_dict = {}

async def scrape_and_send_stickers():
    # Channels to scrape stickers from
    for chanel in chanels:
        name = chanel['name']
        min_id = chanel['min_id']
        print(f"Started scraping chanel: {name}")
        try:
            async for message in client.iter_messages(entity=name, limit=10, min_id=min_id):
                # Filter only sticker messages
                if message.sticker:
                    sticker_set = message.media.document.attributes[1].stickerset
                    if str(sticker_set.id) not in stickers_dict.keys():
                        sub_folder = os.path.join(main_folder,str(sticker_set.id))
                        create_folder(sub_folder)
                        
                        # Fetch the sticker set
                        sticker_set_input = InputStickerSetID(id=sticker_set.id, access_hash=sticker_set.access_hash)
                        sticker_request = await client(GetStickerSetRequest(stickerset=sticker_set_input,hash=0))
                        stickers_dict[str(sticker_set.id)] = [str(sticker.id) for sticker in sticker_request.documents]
                        
                        for sticker in sticker_request.documents:
                            print(f"Downloading stickerset: {sticker_set.id}")
                            await client.download_media(sticker, file=os.path.join(sub_folder,str(sticker.id)))
        
        except Exception as e:
            print(f"Error in channel {name}: {e}")
        
        print(f"Stoped scraping chanel: {name}")
    await client.disconnect() 
    
    with open("scraped_stickers.json", "w") as f:
        json.dump(stickers_dict, f, indent=4)

if __name__=='__main__':
    with client:
        client.loop.run_until_complete(scrape_and_send_stickers())