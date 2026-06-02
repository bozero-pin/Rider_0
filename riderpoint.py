import telebot
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("TOKEN not set")

bot = telebot.TeleBot(TOKEN)


class NameId:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return self.name


def ban_from_group(user_id, group, to_ban):
    return f"Checked ban request: {to_ban} from {group}"


@bot.message_handler(commands=['banch'])
def ban_channel(message):
    parts = message.text.split()[1:]

    if not parts:
        bot.reply_to(message, "Usage: /banch <channel> <group1> <group2>")
        return

    ch = parts[0]
    group_names = parts[1:]

    if not group_names:
        groups = [NameId(message.chat.title or "group", message.chat.id)]
    else:
        groups = [NameId(x, x) for x in group_names]

    if ch.startswith("-") and ch[1:].isdigit():
        to_ban = NameId(ch, int(ch))
    elif ch.isdigit():
        to_ban = NameId(ch, int("-100" + ch))
    else:
        to_ban = NameId(ch, ch)

    results = []

    for g in groups:
        results.append(ban_from_group(message.from_user.id, g, to_ban))

    bot.reply_to(message, "\n".join(results))


print("Bot running...")
bot.infinity_polling()
