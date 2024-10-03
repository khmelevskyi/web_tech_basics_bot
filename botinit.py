import os
import sys
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    PicklePersistence,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

from data import States
from handlers import (
    start,
    main_menu,
    answer_student,
    answer_it_tech,
    answer_contacts,
    ask_chatgpt,
    answer_chatgpt,
    done,
    echo_service
)


load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

print("-------- succesful import --------")


async def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    persistence = PicklePersistence(filepath="conv_storage.pickle")
    bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
    application = Application.builder().token(bot_token).persistence(persistence).build()

    if ("--service" in sys.argv) or ("-s" in sys.argv):
        print("!!!!!!!! bot on service !!!!!!!!")
        application.add_handler(MessageHandler((filters.TEXT | filters.COMMAND), echo_service))
    else:
        necessary_handlers = [CommandHandler('start', start)
                            ]
        conv_handler = ConversationHandler(
            name="conversation",
            persistent=True,
            entry_points=necessary_handlers,
            states={

            States.MAIN_MENU: [
                *necessary_handlers,
                CallbackQueryHandler(answer_student, pattern="student"),
                CallbackQueryHandler(answer_it_tech, pattern="it_tech"),
                CallbackQueryHandler(answer_contacts, pattern="contacts"),
                CallbackQueryHandler(ask_chatgpt, pattern="chatgpt"),
                CallbackQueryHandler(main_menu, pattern="back")
            ],

            States.CHATGPT: [
                *necessary_handlers,
                MessageHandler(filters.TEXT, answer_chatgpt),
                CallbackQueryHandler(main_menu, pattern="back")
            ]

        },
        fallbacks=[CommandHandler('stop', done)],
    )

        application.add_handler(conv_handler)
    

    application.add_error_handler(error_handler)

    print("-------- starting polling --------")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
