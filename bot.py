from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)
import os

TOKEN = os.getenv("BOT_TOKEN")

# مراحل التسجيل
NAME, AGE, GENDER, INTERESTS = range(4)

user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to MobMatch!\n\nType /register to get started."
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 What is your name?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("🎂 How old are you?")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("⚧️ What is your gender?")
    return GENDER

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gender"] = update.message.text
    await update.message.reply_text("❤️ List your interests (comma separated):")
    return INTERESTS

async def get_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["interests"] = update.message.text

    user_id = update.message.from_user.id
    user_data_store[user_id] = context.user_data.copy()

    await update.message.reply_text(
        "✅ Profile created successfully!\n\n"
        f"Name: {context.user_data['name']}\n"
        f"Age: {context.user_data['age']}\n"
        f"Gender: {context.user_data['gender']}\n"
        f"Interests: {context.user_data['interests']}\n\n"
        "Type /find to get matched ❤️"
    )

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gender)],
        INTERESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_interests)],
    },
    fallbacks=[]
)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)

app.run_polling()
