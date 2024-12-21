from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time
from byte import *
from datetime import datetime


#"3023108786": "d1sdquch7g1fon"
# The rest of the elements are the command-line arguments
#3023147506": "st3853qcnx6mzb""

 
ALLOWED_USERNAME =['souhil1231','L79AR12','Vendet4x','afdsdfaeawe','MOHAMED22134']
import threading
import time

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
 
from main import *

import subprocess
import time
import socket
import requests
import random
from protobuf_decoder.protobuf_decoder import Parser
import json
import time
import threading
from byte import *
from datetime import datetime
import base64
 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'لارسال 100 لايك فقط لا غير /like \n مثال \n /like 123456789')
# Define a handler to handle user input
async def send_ids(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global TOKENS
    username = update.message.from_user.username
    print(username) 
    
    await update.message.reply_text(f'welcome')
    time.sleep(1)
    print('-----------------------------------------------------------------------')
    await update.message.reply_text(f'wait ')
    args = context.args

    # Ceck if exactly 4 IDs are provided
    if len(args) == 1:  
        # Check if all IDs are numeric
        if all(id.isdigit() for id in args):
            # Process the IDs (example: join them into a string)
            ids_str = ', '.join(args)
            print(args)
            uid= args[0]
            threading.Thread(target=start_like,args=(uid,)).start()
            await update.message.reply_text(f"تم استقبال الايدي وجاري ارسال 100 لايك فقط لا غير: {ids_str}")
        else:
            await update.message.reply_text("IDs must be numeric.")
    else:
        await update.message.reply_text("Please provide exactly 4 IDs.")
    # else:
    #     await update.message.reply_text(f'انت غير مسموح لك ب استخدام هذا الامر .')
    # Extract the command arguments
 
async def lag(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.message.from_user.username
    print(username)
    if username in  ALLOWED_USERNAME:
        await update.message.reply_text(f'welcome')
     
 
# from telegram import Update 

# async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# app = ApplicationBuilder().token("7049012992:AAHtdkdsx9AqG1PQKxACDIRohdO4gITMq34").build()

# app.add_handler(CommandHandler("hello", hello))

# app.run_polling()

def main() -> None:
    # Create an Updater object to fetch updates from Telegram
    app = ApplicationBuilder().token("5335475397:AAFiOlahN5qbMoazi7SYBnd2XPsfz4xzvRs").build()

    # Get the dispatcher to register handlers
    

    # Register a handler for the /start command
    app.add_handler(CommandHandler("start", start))

    # Register a handler for the custom command to send IDs
    app.add_handler(CommandHandler("like", send_ids))
    time.sleep(1)
    app.add_handler(CommandHandler("lag", lag))

    # Start the bot
    app.run_polling()

    # Run the bot until you press Ctrl-C
    app.idle()
if __name__ == '__main__':
    main()
