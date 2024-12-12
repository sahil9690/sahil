
import os
import asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

TELEGRAM_BOT_TOKEN = '7230583552:AAHUCD3N_s-iPchx0TaIHlXNOMSFzCkwS3E'
ALLOWED_USER_ID = 6512242172
approved_users = set()  # For managing approved users

# Create the main keyboard for the bot
def create_main_keyboard():
    keyboard = [
        [KeyboardButton("/attack"), KeyboardButton("/admin")],
        [KeyboardButton("/info")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "*🔥 Welcome to the battlefield! 🔥*\n\n*Use the buttons below to navigate the bot commands.*", 
        parse_mode='Markdown', 
        reply_markup=create_main_keyboard()
    )

async def run_attack(chat_id, ip, port, context):
    # Removed timer functionality
    await context.bot.send_message(
        chat_id=chat_id, 
        text=f"*⚔️ Attack Launched!*\n*🎯 Target: {ip}:{port}*\n*🔥 Let the battlefield ignite! 💥*", 
        parse_mode='Markdown'
    )
    await context.bot.send_message(
        chat_id=chat_id, 
        text="*✅ Attack Completed! ✅*", 
        parse_mode='Markdown'
    )

async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if user_id != ALLOWED_USER_ID:
        return await context.bot.send_message(
            chat_id=chat_id, 
            text="*❌ You are not authorized to use this bot!*", 
            parse_mode='Markdown'
        )

    if len(context.args) != 2:
        return await context.bot.send_message(
            chat_id=chat_id, 
            text="*⚠️ Usage: /attack <ip> <port>*", 
            parse_mode='Markdown'
        )

    ip, port = context.args
    await run_attack(chat_id, ip, port, context)

async def add_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    
    if update.effective_user.id != ALLOWED_USER_ID:
        return await context.bot.send_message(
            chat_id=chat_id, 
            text="*❌ You are not authorized to use admin commands!*", 
            parse_mode='Markdown'
        )

    if len(context.args) != 1:
        return await context.bot.send_message(
            chat_id=chat_id, 
            text="*⚠️ Usage: /add <userId>*", 
            parse_mode='Markdown'
        )

    user_id = int(context.args[0])
    approved_users.add(user_id)  # Add user to approved list
    await context.bot.send_message(
        chat_id=chat_id, 
        text=f"*✅ User {user_id} has been added and will have access for 999999 days.*", 
        parse_mode='Markdown'
    )

async def admin(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    
    if update.effective_user.id != ALLOWED_USER_ID:
        return await context.bot.send_message(
            chat_id=chat_id, 
            text="*❌ You are not authorized to use admin commands!*", 
            parse_mode='Markdown'
        )
    
    response = "*Admin Commands:* \n"
    response += "\n💥 /add <userId> : Add a User."
    response += "\n💥 /remove <userId> : Remove a User."
    response += "\n💥 /allusers : Authorized Users Lists."
    response += "\n💥 /logs : All Users Logs."
    response += "\n\n*Admin: @offx_sahil*"
    
    await context.bot.send_message(
        chat_id=chat_id, 
        text=response, 
        parse_mode='Markdown'
    )

async def info(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = context.args[0] if context.args else None
    
    approved = "Approved" if user_id in approved_users else "Not Approved"
    response = f"User ID: {user_id}\nStatus: {approved}" if user_id else "No user ID provided."
    
    await context.bot.send_message(
        chat_id=chat_id, 
        text=response, 
        parse_mode='Markdown'
    )

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("add", add_user))  # Add the add_user command
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CommandHandler("info", info))
    
    # Message Handler to handle text messages and show main keyboard
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    application.run_polling()

# Ensure the script runs from the main block
if __name__ == '__main__':
    main()
