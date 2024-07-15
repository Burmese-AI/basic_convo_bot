from typing import Final

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

TOKEN: Final = ''
BOT_USERNAME: Final = '@TTT3st_bot'

GENDER, PHOTO, AGE, BIO = range(4)

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Use command to start the conversation with the bot.")


async def start_conversation_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Male", "Female", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Zixxe Bot. Let's talk.\nAnd, don't worry, i do not store your data "
        "Send /cancel to stop the conversation.\n\n"
        "May i know your gender?",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Gender?"
        ),
    )

    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Can i see your photo? "
        "or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "You looks amazing. May I know yout age , or send /skip if you don't want to."
    )

    return AGE

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "I am sure you looks great.May I know your age., or send /skip."
    )

    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        processedAge = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Sorry, that is not a number.")
        return AGE

    if processedAge < 18:
        await update.message.reply_text("You are Young.")
    elif processedAge < 30:
        await update.message.reply_text("You are Adult.")
    else:
        await update.message.reply_text("You are Old.")
    await update.message.reply_text("Tell me something about yourself.")
    return BIO

async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Wow, Thanks for sharing.")

    return ConversationHandler.END

async def rate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
            [
                InlineKeyboardButton("1", callback_data="1"),
                InlineKeyboardButton("2", callback_data="2"),
                InlineKeyboardButton("3", callback_data="3"),
                InlineKeyboardButton("4", callback_data="4"),
                InlineKeyboardButton("5", callback_data="5"),
            ]
        ]

    await update.message.reply_text(
            "Please rate the bot from 1 to 5:",
            reply_markup=InlineKeyboardMarkup(reply_keyboard),
    )

    return ConversationHandler.END

async def rate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    rating = int(query.data)
    await query.message.reply_text(f"You rated the bot: {rating} out of 5")
    if rating < 3:
        await query.message.reply_text(
            "Sorry to hear that! Please let me know how I can improve."
        )
    else:
        await query.message.reply_text(
            "Thank you! I'm glad you liked it."
        )



async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    first_name = update.message.from_user.first_name
    await update.message.reply_text(f"Goodbye, {first_name}! I hope we can talk again some day.")
    await rate_command(update, context)
    return ConversationHandler.END

async def surprise_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I love you!")
    await update.message.reply_sticker("CAACAgUAAxkBAAIgt2aEslOB4WKomj4z2OkaXll3LudZAAL-AQAC-ClJVtvbqyuA_khaNAQ")


# handlers
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Nice photo!')

async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'You said: {update.message.text}')





if __name__ == '__main__':
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()

    # commands

    app.add_handler(CommandHandler('rate', rate_command))
    app.add_handler(CommandHandler('cancel', cancel_command))
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('surprise', surprise_command))
    # conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("convo", start_conversation_command)],
        states={
            GENDER: [MessageHandler(filters.Regex("^(Male|Female|Other)$"), gender)],
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            AGE: [MessageHandler(filters.TEXT, age)],
            BIO: [MessageHandler(filters.TEXT, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )


    # handlers
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(~filters.COMMAND, echo_handler))
    app.add_handler(CallbackQueryHandler(rate_callback))

    print('polling... ')
    app.run_polling(poll_interval=3)



