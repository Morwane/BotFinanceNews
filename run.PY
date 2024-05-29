import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import openai
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Lire les valeurs des variables d'environnement
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Imprimer les valeurs pour débogage
print("TELEGRAM_BOT_TOKEN:", TELEGRAM_BOT_TOKEN)
print("OPENAI_API_KEY:", OPENAI_API_KEY)

# Vérifier si les tokens sont bien chargés
if TELEGRAM_BOT_TOKEN is None or OPENAI_API_KEY is None:
    raise ValueError("Les tokens Telegram et OpenAI doivent être définis dans le fichier .env")

# Initialiser OpenAI
openai.api_key = "sk-proj-sgb5h1UwCkw5gkwfWKU0T3BlbkFJgUDs1bEZ1DwQX85O6ZMw"

async def start(update: Update, context: CallbackContext) -> None:
    """Envoyer un message de bienvenue quand la commande /start est émise."""
    user = update.effective_user
    await update.message.reply_text(f"Bonjour {user.first_name}! Envoyez-moi un message pour commencer.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Gérer les messages envoyés par les utilisateurs."""
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response['choices'][0]['message']['content'].strip()
        await update.message.reply_text(reply_text)
    except Exception as e:
        print(f'Erreur lors de la génération de la réponse : {e}')
        await update.message.reply_text("Désolé, je ne peux pas répondre pour le moment, je suis en vaccance.")

def main() -> None:
    """Démarrer le bot."""
    try:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        application.run_polling()
    except Exception as e:
        print(f'Erreur lors de l\'initialisation de l\'application : {e}')

if __name__ == '__main__':
    main()
