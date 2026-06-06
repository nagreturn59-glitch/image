import telebot
import requests
import json
from datetime import datetime
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# === CONFIGURATION ===
REQUIRED_CHANNEL = '@mrinxdildos'
OWNER_URL = "https://t.me/M_o_y_zzz"
CHANNEL_URL = "https://t.me/mrinxdildos"
BOT_LIST = "https://t.me/MRiNxDiLDOS/3"
LOG_FILE = 'user_prompts.log'

OWNER_IDS = {2007860433}

# Function to read token from file
def read_token_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Initialize bot with token
BOT_TOKEN = read_token_from_file('token.txt')
bot = telebot.TeleBot(BOT_TOKEN)

BOT_LINK = "@Ai_Gen_BY_MxD_bot"
escaped_bot_link = BOT_LINK.replace('_', '\\_')


# === BANNED WORDS ===
BANNED_KEYWORDS = [
    'nude', 'nsfw', 'porn', 'sex', 'xxx', 'explicit', '18+', 'adult', 'erotic', 'naked', 'uncensored',
    'fetish', 'bdsm', 'ass', 'boobs', 'boob', 'pussy', 'dick', 'penis', 'vagina', 'cum', 'fuck', 'suck',
    'hentai', 'rule34', 'mating', 'anal', 'russian', 'milf', 'bhabhi', 'lund', 'chut', 'gand', 'lgbtq',
    'lesbian', 'gay', 'trans', 'transgender', 'gaysex', 'lesbosex', 'deepthroat', 'blowjob', 'handjob',
    'masturbate', 'masturbation', 'orgasm', 'strip', 'stripping', 'stripper', 'threesome', 'foursome',
    'gangbang', 'creampie', 'cumshot', 'facial', 'pegging', 'pegged', 'bondage', 'spank', 'spanking',
    'slut', 'whore', 'prostitute', 'escort', 'callgirl', 'call boy', 'incest', 'stepmom', 'stepsis',
    'stepson', 'stepbro', 'stepdad', 'pissing', 'piss', 'scat', 'scatology', 'bestiality', 'zoophilia',
    'doggy style', 'doggystyle', '69', '69ing', 'cunnilingus', 'fellatio', 'rimjob', 'rim job', 'fisting',
    'fist', 'orgy', 'orgies', 'cumslut', 'cumdump', 'cum dump', 'cum slut', 'cumshot', 'cum shot',
    'cock', 'cocks', 'jerk', 'jerking', 'jerkoff', 'jerk off', 'handjob', 'hand job', 'tit', 'tits',
    'titjob', 'tit job', 'titfuck', 'tit fuck', 'nipple', 'nipples', 'areola', 'clit', 'clitoris',
    'labia', 'shemale', 'tranny', 'futa', 
]

def is_owner(user_id: int) -> bool:
    return user_id in OWNER_IDS

def is_explicit_prompt(user_id: int, prompt: str) -> bool:
    if is_owner(user_id):
        return False
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in BANNED_KEYWORDS)

def log_prompt(user_id: int, username: str, prompt: str, is_nsfw: bool = False):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        'user_id': user_id,
        'username': username,
        'prompt': prompt,
        'timestamp': timestamp,
        'is_nsfw': is_nsfw,
        'allowed': is_owner(user_id) or not is_nsfw
    }
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n\n')

# === RETRY CONFIGURATION ===
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
session.mount('https://', HTTPAdapter(max_retries=retries))

def check_user_membership(message):
    try:
        user_status = bot.get_chat_member(REQUIRED_CHANNEL, message.from_user.id).status
        if user_status not in ["member", "administrator", "creator"]:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(
                telebot.types.InlineKeyboardButton("[➖ 𝟭𝗦𝗧 𝗝𝗢𝗜𝗡 𝗛𝗘𝗥𝗘 𝗧𝗢 𝗨𝗦𝗘 𝗠𝗘 ➖]", url=CHANNEL_URL, style="danger")
            )
            markup.add(
                telebot.types.InlineKeyboardButton(text="[➖ | 𝗠 𝘅 𝗗™ 𝗔𝗟𝗟 𝗕𝗢𝗧𝗦 | ➖]", url=BOT_LIST, style="primary")
            )
            user_id = message.from_user.id
            try:
                photos = bot.get_user_profile_photos(user_id)
                has_photo = photos.total_count > 0
            except Exception:
                has_photo = False
            caption = f"🚨𝗛𝗜 👋 *{message.from_user.first_name}* \n\n‼️ 𝗠𝗥𝗶𝗡 𝘅 𝗗𝗶𝗟𝗗𝗢𝗦™ 𝗔𝗶 𝗜𝗠𝗔𝗚𝗘 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥 𝗕𝗢𝗧 𝗔𝗖𝗖𝗘𝗦𝗦 𝗗𝗘𝗡𝗜𝗘𝗗 ! \n\n🔒 *𝗝𝗼𝗶𝗻 𝗼𝘂𝗿 𝗼𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁 !* 🔒"
            if has_photo:
                try:
                    photo_file_id = photos.photos[0][0].file_id
                    bot.send_photo(
                        message.chat.id, 
                        photo_file_id,
                        caption=caption,
                        parse_mode="Markdown",
                        reply_markup=markup
                    )
                except Exception:
                    bot.send_message(
                        message.chat.id,
                        caption,
                        parse_mode="Markdown",
                        reply_markup=markup
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    caption,
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            return False
        return True
    except Exception as e:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("[➖ 𝟭𝗦𝗧 𝗝𝗢𝗜𝗡 𝗛𝗘𝗥𝗘 𝗧𝗢 𝗨𝗦𝗘 𝗠𝗘 ➖]", url=CHANNEL_URL)
        )
        bot.send_message(
            message.chat.id,
            f"Error checking membership: {str(e)}",
            reply_markup=markup
        )
        return False

# === START COMMAND ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_user_membership(message):
        return

    user_id = message.from_user.id

    user_id = message.from_user.id
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text="[➖ 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 ➖]", url=OWNER_URL, style="primary")
    button2 = telebot.types.InlineKeyboardButton(text="[➖ 𝗠𝗔𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 ➖]", url=CHANNEL_URL, style="danger")
    button3 = telebot.types.InlineKeyboardButton(text="[➖ | 𝗠 𝘅 𝗗™ 𝗔𝗟𝗟 𝗕𝗢𝗧𝗦 | ➖]", url=BOT_LIST, style="success")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)

    welcome_text = (
        "𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗠𝗥𝗶𝗡 𝘅 𝗗𝗶𝗟𝗗𝗢𝗦™ 𝗔𝗶 𝗜𝗠𝗔𝗚𝗘 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥 𝗕𝗢𝗧\n\n"
        "🖼️ 𝗦𝗲𝗻𝗱 𝗮 𝘁𝗲𝘅𝘁 𝗽𝗿𝗼𝗺𝗽𝘁 𝗮𝗻𝗱 𝗜'𝗹𝗹 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗮𝗻 𝗶𝗺𝗮𝗴𝗲 𝗳𝗼𝗿 𝘆𝗼𝘂 !\n\n"
        "𝗘𝘅𝗮𝗺𝗽𝗹𝗲  :    `Cow eating carrot on rainy day`"
    )

    try:
        photos = bot.get_user_profile_photos(user_id)
        has_photo = photos.total_count > 0
    except Exception:
        has_photo = False

    if has_photo:
        try:
            photo_file_id = photos.photos[0][0].file_id
            bot.send_photo(
                message.chat.id, photo_file_id,
                caption=welcome_text,
                parse_mode="Markdown",
                reply_markup=markup
            )
        except Exception:
            bot.send_message(
                message.chat.id, welcome_text,
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=markup
            )
    else:
        bot.send_message(
            message.chat.id, welcome_text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=markup
        )

# Notify owner(s) about new user
    user_name = (message.from_user.username and f"@{message.from_user.username}") or message.from_user.first_name or str(message.from_user.id)
    notify_text = f"👤 𝗡𝗘𝗪 𝗨𝗦𝗘𝗥 𝗛𝗔𝗦 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 𝗢𝗨𝗥 𝗕𝗢𝗧\n\n 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘: {user_name}\n 𝗨𝗦𝗘𝗥 𝗜𝗗: {message.from_user.id}"

    for owner_id in OWNER_IDS:
        if owner_id != message.from_user.id:  # Don't notify if owner starts the bot
            try:
                bot.send_message(owner_id, notify_text)
            except Exception as e:
                print(f"Failed to notify owner {owner_id}: {e}")

# === HISTORY COMMAND FOR OWNERS ===
@bot.message_handler(commands=['history'])
def handle_history(message):
    if message.from_user.id not in OWNER_IDS:
        return  # Ignore for non-owners

    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()
        if not logs:
            bot.reply_to(message, ".\n📜 𝗡𝗼 𝗹𝗼𝗴𝘀 𝗙𝗼𝘂𝗻𝗱 !")
            return
        with open(LOG_FILE, 'rb') as f:
            bot.send_document(
                message.chat.id,
                f,
                caption=".\n📄 𝗙𝘂𝗹𝗹 𝗣𝗿𝗼𝗺𝗽𝘁 𝗟𝗼𝗴𝘀"
            )
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error accessing logs: {str(e)}")

# === IMAGE GENERATION HANDLER ===
@bot.message_handler(func=lambda message: True, content_types=['text'])
def generate_image(message):
    # If owner sends /history, do not generate image (handled above)
    if message.text.strip().lower() == '/history':
        return

    if not check_user_membership(message):
        return

    user_id = message.from_user.id
    username = message.from_user.username or str(user_id)
    prompt = message.text.strip()
    
    # Log all prompts immediately
    log_prompt(user_id, username, prompt)
    
    if not prompt:
        bot.reply_to(message, "𝗣𝗟𝗘𝗔𝗦𝗘 𝗣𝗥𝗢𝗩𝗜𝗗𝗘 𝗠𝗘 𝗔 𝗧𝗘𝗫𝗧 𝗣𝗥𝗢𝗠𝗣𝗧 ✌️")
        return

    # NSFW content check (owners exempt)
    if is_explicit_prompt(user_id, prompt):
        warning_msg = (
            "🚫 𝗘𝘅𝗽𝗹𝗶𝗰𝗶𝘁 𝗖𝗼𝗻𝘁𝗲𝗻𝘁 𝗪𝗮𝗿𝗻𝗶𝗻𝗴 😡‼️\n\n"
            "𝗪𝗲 𝗱𝗼 𝗻𝗼𝘁 𝗮𝗹𝗹𝗼𝘄 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗼𝗻 𝗼𝗳 𝗲𝘅𝗽𝗹𝗶𝗰𝗶𝘁 𝗼𝗿 𝗮𝗱𝘂𝗹𝘁 𝗰𝗼𝗻𝘁𝗲𝗻𝘁. 𝗬𝗼𝘂𝗿 𝗿𝗲𝗾𝘂𝗲𝘀𝘁 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗹𝗼𝗴𝗴𝗲𝗱.\n\n"
            "𝗥𝗲𝗽𝗲𝗮𝘁𝗲𝗱 𝘃𝗶𝗼𝗹𝗮𝘁𝗶𝗼𝗻𝘀 𝗺𝗮𝘆 𝗿𝗲𝘀𝘂𝗹𝘁 𝗶𝗻 𝗮 𝗯𝗮𝗻."
        )
        bot.reply_to(message, warning_msg, parse_mode="Markdown")
        log_prompt(user_id, username, prompt, is_nsfw=True)
        return

    bot.send_chat_action(message.chat.id, 'upload_photo')

    try:
        response = session.get(
            "https://img-gen.hazex.workers.dev/",
            params={'prompt': prompt},
            timeout=60
        )
        # Parse the JSON response
        data = response.json()
        image_url = data.get("image_url")
        if image_url:
            bot.send_photo(
                message.chat.id,
                image_url,
                caption=f"🖼️ 𝗬𝗢𝗨𝗥 𝗥𝗘𝗤𝗨𝗘𝗦𝗧𝗘𝗗 𝗣𝗛𝗢𝗧𝗢  >  `{prompt}`\n\n         ©️  {escaped_bot_link}",
                parse_mode="Markdown"
            )
        else:
            bot.reply_to(
                message,
                "⚠️ 𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗶𝗺𝗮𝗴𝗲. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿."
            )
    except Exception as e:
        bot.reply_to(message, f"⚠️ {str(e)}")


if __name__ == '__main__':
    print("Image Generator Bot is running...")
    bot.infinity_polling()
