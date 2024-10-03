from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, constants

from data import States, text
from chatgpt_api_handler import request_chatgpt_reply


main_menu_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Студент", callback_data="student")],
        [InlineKeyboardButton("ІТ-технології", callback_data="it_tech")],
        [InlineKeyboardButton("Контакти", callback_data="contacts")],
        [InlineKeyboardButton("Спитати ChatGPT", callback_data="chatgpt")]
    ])
back_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Назад", callback_data="back")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text["start"], reply_markup=main_menu_keyboard)
    return States.MAIN_MENU


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text["main_menu"], reply_markup=main_menu_keyboard)

    return States.MAIN_MENU


async def answer_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text["answer_student"], reply_markup=back_keyboard)
    return States.MAIN_MENU


async def answer_it_tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text["answer_it_tech"], reply_markup=back_keyboard)
    return States.MAIN_MENU


async def answer_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text["answer_contacts"], reply_markup=back_keyboard)
    return States.MAIN_MENU


async def ask_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.chat_data["msg_to_delete"] = query

    await query.edit_message_text(text["answer_chatgpt"], reply_markup=back_keyboard)
    return States.CHATGPT


async def answer_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query: CallbackQuery = context.chat_data.pop("msg_to_delete")
    await query.delete_message()
    await update.message.reply_chat_action(action=constants.ChatAction.TYPING)

    msg = update.message.text

    # chatgpt part
    text_from_chatgpt = "Відповідь від ChatGPT:\n"
    text_from_chatgpt +=  request_chatgpt_reply(msg)
    #/

    await update.message.reply_text(text_from_chatgpt)
    await update.message.reply_text(text["main_menu"], reply_markup=main_menu_keyboard)
    return States.MAIN_MENU


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END


async def echo_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ echo all msgs"""

    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=(
            "Зараз бот на технічному обслуговуванні ⚠\n"
            + "и тимчасово не працює 🧑🏿‍💻\nСкоро повернемось🕔"
        ),
    )

