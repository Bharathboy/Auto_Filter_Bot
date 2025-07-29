#Join Telegram Channel - @DREAMXBOTZ

from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_REQ_CHANNELS
from utils import get_settings


#credits @bharath_boy (atleast dont remove credits if steal this code)
@Client.on_chat_join_request()
async def join_reqs(client, message: ChatJoinRequest):
    user_id = message.from_user.id
    chat_id = message.chat.id
    invite_link = message.invite_link

    if chat_id in AUTH_REQ_CHANNELS:
        await db.add_join_req(user_id, chat_id)
 
    if invite_link and invite_link.name and invite_link.name.startswith("req_"):
        print ("Invite link name:", invite_link.name)
        print (invite_link)
        try:
            _, group_id_str = invite_link.name.split("_")
            group_id = int(group_id_str)
            
            settings = await get_settings(group_id)
            req_channels = settings.get('reqfsub', [])

            if chat_id in req_channels:
                await db.add_join_req(user_id, chat_id)

        except (ValueError, IndexError) as e:
            print(f"Could not parse invite link name '{invite_link.name}': {e}")
        except Exception as e:
            print(f"An error occurred in join_reqs handler: {e}")
    
        


@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()    
    await message.reply("<b>⚙️ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")