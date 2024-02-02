from pyrogram import enums, filters, types

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
1. First you have to connect the desired channel / group using /connect.
2. Once chat is connected with your PM, use /chats to view the connected chats.
3. Click on any chat to set-up auto-accept and auto-delete.
4. You can set a delay for accepting the requests, which means users will be accepted only after the set delay.
5. You can also set-up a welcome message, which will be sent to the user, once he send request to join the channel / group.

**Auto-Delete Settings**
1. Connect the chat same as above
2. Use /chats to enter into `Auto-Delete` settings for specific chats.
3. You can turn on / off auto delete using the status button.
4. You can set delay for deleting the message 
5. You can also set `type` of messages to be deleted [text, media or all]
"""

FORMAT = """
<b>Markdown Formatting</b>
You can format your message using <b>bold</b>, <i>italic</i>, <u>underline</u>, <strike>strike</strike> and much more. Go ahead and experiment!
<b>Note</b>: It supports telegram user based formatting as well as html and markdown formattings.

<b>Supported markdown</b>:
- <code>`code words`</code>: Backticks are used for monospace fonts. Shows as: <code>code words</code>.
- <code>__italic__</code>: Underscores are used for italic fonts. Shows as: <i>italic words</i>.
- <code>**bold**</code>: Asterisks are used for bold fonts. Shows as: <b>bold words</b>.
- <code>```pre```</code>: To make the formatter ignore other formatting characters inside the text formatted with '```', like: <code>**bold** | *bold*</code>.
- <code>--underline--</code>: To make text <u>underline</u>.
- <code>~~strike~~</code>: Tildes are used for strikethrough. Shows as: <strike>strike</strike>.
- <code>||spoiler||</code>: Double vertical bars are used for spoilers. Shows as: <spoiler>Spoiler</spoiler>.
- <code>[hyperlink](example.com)</code>: This is the formatting used for hyperlinks. Shows as: <a href="https://example.com/">hyperlink</a>.
- <code>[My Button](buttonurl://example.com)</code>: This is the formatting used for creating buttons. This example will create a button named "My button" which opens <code>example.com</code> when clicked.
If you would like to send buttons on the same row, use the <code>:same</code> formatting.
<b>Example:</b>
<code>[button 1](buttonurl:example.com)</code>
<code>[button 2](buttonurl://example.com:same)</code>
<code>[button 3](buttonurl://example.com)</code>
This will show button 1 and 2 on the same line, while 3 will be underneath.


<b>Fillings</b>
You can also customise the contents of your message with contextual data. For example, you could mention a user by name in the welcome message, or mention them in a filter!
You can use these to mention a user in notes too!
<b>Supported fillings:</b>
- <code>{first}</code>: The user's first name.
- <code>{last}</code>: The user's last name.
- <code>{fullname}</code>: The user's full name.
- <code>{username}</code>: The user's username. If they don't have one, mentions the user instead.
- <code>{mention}</code>: Mentions the user with their firstname.
- <code>{id}</code>: The user's ID.
- <code>{chatname}</code>: The chat's name.
"""


@Bot.on_message(filters.command("ssstart") & filters.incoming)  # type: ignore
@is_banned
async def start_handler(_: Bot, msg: types.Message):
    await msg.reply(
        START_TEXT.format(mention=msg.from_user.mention),
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("🔖 Help", callback_data=f"fallen_"),
                    types.InlineKeyboardButton(
                        "🔗 Support", url=Config.SUPPORT_CHAT_URL
                    ),
                ]
            ]
        ),
        disable_web_page_preview=True,
    )


@Bot.on_callback_query(filters.regex("bothelp"))  # type: ignore
async def help_handler_query(_: Bot, query: types.CallbackQuery):
    await query.answer()
    await query.edit_message_text(
        HELP_TEXT,
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("◀️ Back", callback_data="fallen_back"),
                    types.InlineKeyboardButton("📘 Advanced Help", "advHelp"),
                ]
            ]
        ),
    )


@Bot.on_callback_query(filters.regex("advHelp"))  # type: ignore
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


@Bot.on_callback_query(filters.regex("hennhdlp"))  # type: ignore
async def home_handler(_: Bot, query: types.CallbackQuery):
    await query.answer()
    await query.edit_message_text(
        START_TEXT.format(mention=query.from_user.mention),
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("🔖 Help", callback_data=f"fallen_"),
                    types.InlineKeyboardButton(
                        "🔗 Support", url=Config.SUPPORT_CHAT_URL
                    ),
                ]
            ]
        ),
        disable_web_page_preview=True,
    )


HELP_MENU = [
    [
        InlineKeyboardButton("Quiz", callback_data='help_button_1'),
        InlineKeyboardButton("AutoQuiz", callback_data='help_button_2'),
    ],
    [
        InlineKeyboardButton("Ranking", callback_data='help_button_3'),
        InlineKeyboardButton("Points", callback_data='help_button_4'),
    ],
    [
        InlineKeyboardButton("Language", callback_data='help_button_5'),
        InlineKeyboardButton("Support", callback_data='help_button_6'),
    ],
    [
        InlineKeyboardButton("Close", callback_data='help_button_close'),
    ],
]

@Bot.on_message(filters.command("help") & filters.incoming)
@is_banned
async def help_handler(_: Bot, msg: types.Message):
    reply_markup = InlineKeyboardMarkup(HELP_MENU)
    
    await msg.reply_text(
        "This is the help menu of the quiz game bot. If you have any doubts, head to the support chat.",
        reply_markup=reply_markup,
    )


@Bot.on_callback_query(filters.regex("^help_button_"))
async def handle_help_callback(_: Bot, query: types.CallbackQuery):
    query.answer()

    button_data = query.data

    if button_data == 'help_button_close':
        await query.delete_message()
    else:
        help_text = get_help_text_for_button(button_data)

        await query.edit_message_text(
            text=help_text,
            parse_mode='Markdown',
        )

def get_help_text_for_button(button_data: str) -> str:
    help_text = "This is the help menu:\n"
    
    if button_data == 'help_button_1':
        help_text += "/quiz - sends quiz to the group/user. The command can be used in groups and inbox of the bot"
    elif button_data == 'help_button_2':
        help_text += "/autoquiz - enables periodic quiz that sends 1 in 10 minutes and deletes old quiz poll\n/stopquiz - stops the function on the group or inbox of the bot"
    elif button_data == 'help_button_3':
        help_text += "/topusers - shows the global top 10 users who have high points."
    elif button_data == 'help_button_4':
        help_text += "/points - shows your total points on the bot based on your answers on polls. You can receive negative or positive points."
    elif button_data == 'help_button_5':
        help_text += "Language:\nComing soon! Adding Russian, Arabic, Hindi, French, etc. Other languages will be added as per user request."
    elif button_data == 'help_button_6':
        help_text += "Support:\nHead to @XenonSupportChat for more help and to report bugs, and provide ideas about adding new features to the bot."

    return help_text
