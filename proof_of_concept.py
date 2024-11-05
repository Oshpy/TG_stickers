from telethon import TelegramClient, events

api_id = ****
api_hash = '****'


client = TelegramClient('session_name', api_id, api_hash)

with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, world!'))