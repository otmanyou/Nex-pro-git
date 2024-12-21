from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import time
import subprocess
import threading
from datetime import datetime
from psutil import cpu_percent  # Requires psutil library
import asyncio
from main import *
# Database name
DB_NAME = 'groups.db'

# Allowed usernames
ALLOWED_USERNAME = ['souhil1231', 'L79AR12', 'Vendet4x', 'afdsdfaeawe', 'MOHAMED22134']

# Initialize database
def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        log_error(str(e))

# Add group to database
def add_group_to_db(group_id: int, group_title: str):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO groups (id, title)
            VALUES (?, ?)
        ''', (group_id, group_title))
        conn.commit()
        conn.close()
    except Exception as e:
        log_error(str(e))

# Get groups from database
def get_groups_from_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title FROM groups')
        groups = cursor.fetchall()
        conn.close()
        return groups
    except Exception as e:
        log_error(str(e))
        return []

# Log errors and messages
def log_to_db(message: str, log_type: str):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO logs (timestamp, type, message)
            VALUES (?, ?, ?)
        ''', (datetime.now().isoformat(), log_type, message))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to log to database: {e}")

def log_error(message: str):
    log_to_db(message, 'ERROR')

def log_message(message: str):
    log_to_db(message, 'MESSAGE')

# Send high CPU usage notification to all groups
async def notify_high_cpu_usage(app):
    try:
        groups = get_groups_from_db()
        if groups:
            for group_id, group_title in groups:
                try:
                    await app.send_message(chat_id=group_id, text="Server CPU usage is high.")
                except Exception as e:
                    log_error(f"Failed to send high CPU usage notification to group {group_title} (ID: {group_id}): {e}")
    except Exception as e:
        log_error(f"Failed to retrieve groups for high CPU usage notification: {e}")

# Start bot

EXCLUDED_GROUP_ID = -1002400297702
GROUP_URL = "https://t.me/+3EULIbZzM_s1M2Nk"

# Check if the message is from the allowed group
def is_allowed_group(update: Update) -> bool:
    return update.effective_chat.id == EXCLUDED_GROUP_ID

# Start bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_allowed_group(update):
        await update.message.reply_text(f"للاستعمال البوت يرجي استعمال الجروب الوحيد: {GROUP_URL}")
        return
    try:
        await update.message.reply_text(f'لارسال 100 لايك فقط لا غير /like \n مثال \n /like 123456789')
    except Exception as e:
        log_error(str(e))

# Handle user IDs
async def send_ids(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_allowed_group(update):
        await update.message.reply_text(f"للاستعمال البوت يرجي استعمال الجروب الوحيد: {GROUP_URL}")
        return
    try:
        username = update.message.from_user.username
        print(username)

        await update.message.reply_text(f'welcome')
        time.sleep(1)
        print('-----------------------------------------------------------------------')
        await update.message.reply_text(f'wait ')
        args = context.args

        if len(args) == 1:
            if all(id.isdigit() for id in args):
                ids_str = ', '.join(args)
                print(args)
                uid = args[0]
                threading.Thread(target=start_like, args=(uid,)).start()
                await update.message.reply_text(f"تم استقبال الايدي وجاري ارسال 100 لايك فقط لا غير: {ids_str}")
            else:
                await update.message.reply_text("IDs must be numeric.")
        else:
            await update.message.reply_text("Please provide exactly 4 IDs.")
    except Exception as e:
        log_error(str(e))

# Track groups
async def track_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_allowed_group(update):
        await update.message.reply_text(f"للاستعمال البوت يرجي استعمال الجروب الوحيد: {GROUP_URL}")
        return
    try:
        chat = update.effective_chat
        if chat.type in ['group', 'supergroup']:
            add_group_to_db(chat.id, chat.title)
            await update.message.reply_text(f"تمت إضافتي إلى المجموعة: {chat.title}")
    except Exception as e:
        log_error(str(e))

# Send group info
async def send_group_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_allowed_group(update):
        await update.message.reply_text(f"للاستعمال البوت يرجي استعمال الجروب الوحيد: {GROUP_URL}")
        return
    try:
        groups = get_groups_from_db()
        user = update.message.from_user.username
        if 'afdsdfaeawe' in user:
            await update.message.reply_text("جاري العمل")

            if groups:
                group_list = "\n".join([f"{title} (ID: {gid})" for gid, title in groups])
                message = f"عدد المجموعات: {len(groups)}\n\n{group_list}"
                await context.bot.send_message(chat_id=6763183174, text=message)
                await update.message.reply_text("تم إرسال معلومات المجموعات إلى حسابك.")
            else:
                await update.message.reply_text("لا يوجد أي مجموعات مسجلة.")
        else:
            await update.message.reply_text("  لا تمتلك صلاحيات المطور ")
    except Exception as e:
        log_error(str(e))

def main() -> None:
    # Initialize database
    init_db()

    # Create Telegram bot application
    app = ApplicationBuilder().token("bot_token:bot_token").build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("like", send_ids))
    app.add_handler(CommandHandler("send_groups", send_group_info))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_group))

    # Monitor CPU usage
    async def monitor_cpu_usage():
        while True:
            try:
                if cpu_percent(interval=1) > 80:
                    await notify_high_cpu_usage(app)
                await asyncio.sleep(60)  # Check every 60 seconds
            except Exception as e:
                log_error(str(e))
                # Continue running after handling exception

    # Start CPU monitoring and bot polling
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_cpu_usage())
    app.run_polling()

if __name__ == '__main__':
    main()