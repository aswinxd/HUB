from pyrogram import enums, filters, types, CallbackQuery
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import Bot
from ..config import Config
from ..utils.decorators import is_banned

START_TEXT = """Hey {mention} 👋
restart the bot /start 
"""

HELP_TEXT = """
**Available Commands and Explanation**

>> /Pconnect - __To connect a channel / group for further settings.__
>> /chats - __Lists the available connected chats.__
>> /send - __To send messages to connected chats together.__

**Auto-Accept Settings**
1. First, you have to connect the desired channel / group using /connect.
2. Once the chat is connected with your PM, use /chats to view the connected chats.
3. Click on any chat to set up auto-accept and auto-delete.
4. You can set a delay for accepting the requests, which means users will be accepted only after the set delay.
5. You can also set up a welcome message, which will be sent to the user, once he sends a request to join the channel / group.

**Auto-Delete Settings**
1. Connect the chat same as above
2. Use /chats to enter into `Auto-Delete` settings for specific chats.
3. You can turn on / off auto-delete using the status button.
4. You can set delay for deleting the message 
5. You can also set `type` of messages to be deleted [text, media or all]
"""

FORMAT = """
<b>Markdown Formatting</b>
You can format your message using <b>bold</b>, <i>italic</i>, <u>underline</u>, <strike>strike</strike>, and much more. Go ahead and experiment!
<b>Note</b>: It supports telegram user-based formatting as well as html and markdown formattings.

... (remaining content)

<b>Fillings</b>
You can also customize the contents of your message with contextual data. For example, you could mention a user by name in the welcome message or mention them in a filter!
You can use these to mention a user in notes too!
<b>Supported fillings:</b>
- <code>{first}</code>: The user's first name.
- <code>{last}</code>: The user's last name.
- <code>{fullname}</code>: The user's full name.
- <code>{username}</code>: The user's username. If they don't have one, mention the user instead.
- <code>{mention}</code>: Mentions the user with their firstname.
- <code>{id}</code>: The user's ID.
- <code>{chatname}</code>: The chat's name.
"""

@Bot.on_message(filters.command("start") & filters.incoming)
@is_banned
async def start_handler(_: Bot, msg: types.Message):
    await msg.reply(
        START_TEXT.format(mention=msg.from_user.mention),
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("🔖 Help", callback_data="fallen_"),
                    types.InlineKeyboardButton(
                        "🔗 Support", url=Config.SUPPORT_CHAT_URL
                    ),
                ]
            ]
        ),
        disable_web_page_preview=True,
    )

@Bot.on_callback_query(filters.regex("bothelp"))
async def help_handler_query(_: Bot, query: types.CallbackQuery):
    await query.answer()
    await query.edit_message_text(
        HELP_TEXT,
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("◀️ Back", callback_data="fallen_back"),
                    types.InlineKeyboardButton("📘 Advanced Help", callback_data="advHelp"),
                ]
            ]
        ),
    )

@Bot.on_callback_query(filters.regex("advHelp"))
async def adv_handler_query(_: Bot, query: types.CallbackQuery):
    await query.edit_message_text(
        FORMAT,
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("◀️ Back", callback_data="fallen_"),
                ]
            ]
        ),
        parse_mode=enums.ParseMode.HTML,
    )

@Bot.on_callback_query(filters.regex("hennhdlp"))
async def home_handler(_: Bot, query: types.CallbackQuery):
    await query.answer()
    await query.edit_message_text(
        START_TEXT.format(mention=query.from_user.mention),
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("🔖 Help", callback_data="fallen_"),
                    types.InlineKeyboardButton(
                        "🔗 Support", url=Config.SUPPORT_CHAT_URL
                    ),
                ]
            ]
        ),
        disable_web_page_preview=True,
    )

@Bot.on_message(filters.command("help") & filters.incoming)
@is_banned
async def help_handler(_: Bot, msg: types.Message):
    # Create callback buttons with corresponding strings
    callback_buttons = [
        InlineKeyboardButton("Button 1 - Explanation", callback_data="button1"),
        InlineKeyboardButton("Button 2 - Advanced Help", callback_data="button2"),
        InlineKeyboardButton("Button 3 - Other Option", callback_data="button3"),
        InlineKeyboardButton("Button 4 - Settings", callback_data="button4"),
        InlineKeyboardButton("Button 5 - Support", callback_data="button5"),
        InlineKeyboardButton("Button 6 - More Info", callback_data="button6"),
        InlineKeyboardButton("Close", callback_data="close"),
    ]

    # Create InlineKeyboardMarkup with 2 buttons per row
    reply_markup = InlineKeyboardMarkup([callback_buttons[i:i + 2] for i in range(0, len(callback_buttons), 2)])

    # Reply to the message with the help text and callback buttons
    await msg.reply(
        HELP_TEXT,
        reply_markup=reply_markup,
    )

@Bot.on_callback_query()
async def help_callback_handler(bot: Bot, query: CallbackQuery):
    await query.answer()

    if query.data == "close":
        # Close the menu
        await query.message.delete()
    elif query.data.startswith("button"):
        # Handle button clicks
        button_number = query.data[6:]  # Extract the button number from the callback data
        await query.edit_message_text(f"You clicked on {query.data} - Implement your logic here")

# ... (other functions)
