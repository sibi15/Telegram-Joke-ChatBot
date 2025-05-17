import os   # operating system
import re   # regular expression
from dotenv import load_dotenv  # extract api keys from .env file
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()  # load environment variables from .env file

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"   # used to trace API calls on LangChain
groq_api_key = os.getenv("GROQ_API_KEY")

def setup_llm_chain(topic="technology"):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Joking AI. Give me only ONE joke on the given topic."),
        ("user", f"Generate a joke on the topic: {topic}"),
    ])
    llm = ChatGroq(
        model = "Gemma2-9b-It",
        groq_api_key = groq_api_key
    )
    return prompt | llm | StrOutputParser()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Mention me with a topic like '@Binary_1_Joker_Bot topic' to get a joke.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Mention me with a topic like '@Binary_1_Joker_Bot topic', to get some funny jokes.")

async def generate_joke(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
    await update.message.reply_text(f"Generating a joke about '{topic}'.")
    joke = setup_llm_chain(topic).invoke({}).strip()
    await update.message.reply_text(joke)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    bot_username = context.bot.username
    if f'@{bot_username}' in msg:
        match = re.search(f'@{bot_username}\\s+(.*)', msg)
        if match and match.group(1).strip():
            await generate_joke(update, context, match.group(1).strip())
        else:
            await update.message.reply_text("Please specify a topic after mentioning me.")

def main():
    token = os.getenv("TELEGRAM_API_KEY")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(allowed_updates = Update.ALL_TYPES)

if __name__ == "__main__":
    main()

# This is a simple Telegram bot that generates jokes using the LangChain API and the Groq model.