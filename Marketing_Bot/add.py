from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest

# Replace with your actual API ID, API Hash, and bot token
api_id = 'your api id'
api_hash = 'your api hash'
bot_token = 'your phone number'

with TelegramClient('bot_session', api_id, api_hash) as client:
    # Replace 'https://t.me/joinchat/...' with your actual invite link
    invite_link = 'https://t.me/joinchat/zRL6AlXSWtkzYTFk'

    # Import the chat using the invite link
    result = client(ImportChatInviteRequest(invite_link))

    # Get the chat ID from the result
    chat_id = result.chat.id

    # Join the group
    client(JoinChannelRequest(chat_id))

    print(f'Successfully joined the group from invite link: {invite_link}')
