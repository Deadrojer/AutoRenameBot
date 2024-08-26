import aiohttp, asyncio, warnings, pytz
from datetime import datetime, timedelta
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import pyrogram.utils
import pyromod
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Setting SUPPORT_CHAT directly here
SUPPORT_CHAT = int(os.environ.get("SUPPORT_CHAT", "-1001953724858"))

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="codeflixbots",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        # Initialize the bot's start time for uptime calculation
        self.start_time = time.time()

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME     
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()       
            await web.TCPSite(app, "0.0.0.0", 8080).start()     
        print(f"{me.first_name} Is Started.....✨️")

        # Calculate uptime using timedelta
        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(timedelta(seconds=uptime_seconds))

        for chat_id in [Config.LOG_CHANNEL, SUPPORT_CHAT]:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time_str = curr.strftime('%I:%M:%S %p')
                
                # Send the message with the photo
                message = await self.send_photo(
                    chat_id=chat_id,
                    photo=Config.START_PIC,
                    caption=(
                        "**ᴀɴʏᴀ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ ᴀɢᴀɪɴ  !**\n\n"
                        f"ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ​: `{uptime_string}`"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/sewxiy"),
                            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/codeflix_bots")
                        ]]
                    )
                )
                
                # Debugging to check the message object
                print(f"Message object: {message}")

                # Check if the message was sent to SUPPORT_CHAT and schedule its deletion
                if chat_id == SUPPORT_CHAT:
                    # Assuming 'message_id' is the correct attribute; adjust if needed
                    message_id = message.message_id if hasattr(message, 'message_id') else None
                    if message_id:
                        await asyncio.sleep(120)  # Wait for 2 minutes (120 seconds)
                        await self.delete_messages(chat_id=chat_id, message_ids=[message_id])
                    else:
                        print("No message_id found in the message object")

            except Exception as e:
                print(f"Failed to send or delete message in chat {chat_id}: {e}")

Bot().run()
