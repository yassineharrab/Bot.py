import logging
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# API keys
TELEGRAM_TOKEN = '7289784916:AAHubVMw9nLI9k7AVIUvI-mgWgB9kaXGuts'
GEMINI_API_KEY = 'AIzaSyAt-XpMxt13W4EZj1Svor6cLAHbE_VwXCU'

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Function to call Gemini API
async def call_gemini_api(text: str) -> str:
    prompt_parts = [
        f"input: {text}",
        "output: ",
    ]
    try:
        response = model.generate_content(prompt_parts)
        logger.info(f'Response data: {response}')
        return response.text
    except Exception as err:
        logger.error(f'Error occurred: {err}')
        return 'Sorry, I am unable to process your request at the moment.'

# Command handler to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! I am your AI bot. Ask me anything!')

# Message handler for user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logger.info(f'Received message: {user_message}')
    ai_response = await call_gemini_api(user_message)
    await update.message.reply_text(ai_response)

def main() -> None:
    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non-command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
