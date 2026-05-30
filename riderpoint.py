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
    # ⚠️ NOTE: real Telegram ban needs admin rights
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

    # simple conversion
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
        admin_ids = [a.user.id for a in admins]

        if u.id not in admin_ids:
            return f"Error: you are not an admin of {group}."

        me = await bot.get_me()

        if me.id not in admin_ids:
            return f"Error: I'm not an admin of {group}."

        try:
            await bot.ban_chat_sender_chat(
                chat_id=group.id,
                sender_chat_id=to_ban.id
            )
            return f"Banned {to_ban} from {group}."
        except Exception as e:
            return f"Failed to ban {to_ban} from {group}. ({e})"

    async def ban_channel(self, msg: types.Message):
        logger.info("Received: %s", msg.text)

        parts = msg.text.split()[1:]
        if not parts:
            return

        ch, *group_names = parts

        if not group_names:
            groups = [NameId(msg.chat.username or "group", msg.chat.id)]
        else:
            groups = [NameId(x, x) for x in group_names]

        try:
            if ch.startswith("-") and ch[1:].isdigit():
                to_ban = NameId(ch, int(ch))
            elif ch.isdigit():
                to_ban = NameId(ch, int("-100" + ch))
            else:
                chat = await self.bot.get_chat(ch)
                to_ban = NameId(ch, chat.id)

        except Exception:
            await msg.answer(f"Error: chat {ch} not found")
            return

        results = []
        for g in groups:
            results.append(await self.ban_from_a_group(msg.from_user, g, to_ban))

        await msg.answer("\n".join(results))

    async def run(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)


async def main():
    token = os.getenv("TOKEN")

    if not token:
        raise RuntimeError("TOKEN not set in environment variables")

    bot = BanChannelBot(token)
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
        try:
            admins = await bot.get_chat_administrators(group.id)
        except Exception:
            return f"Error: chat {group} not found."

        admin_ids = [a.user.id for a in admins]

        if u.id not in admin_ids:
            return f"Error: you are not an admin of {group}."

        me = await bot.get_me()

        if me.id not in admin_ids:
            return f"Error: I'm not an admin of {group}."

        try:
            await bot.ban_chat_sender_chat(
                chat_id=group.id,
                sender_chat_id=to_ban.id
            )
            return f"Banned {to_ban} from {group}."
        except Exception as e:
            return f"Failed to ban {to_ban} from {group}. ({e})"

    async def ban_channel(self, msg: types.Message):
        logger.info("Received: %s", msg.text)

        parts = msg.text.split()[1:]
        if not parts:
            return

        ch, *group_names = parts

        if not group_names:
            groups = [NameId(msg.chat.username or "group", msg.chat.id)]
        else:
            groups = [NameId(x, x) for x in group_names]

        try:
            if ch.startswith("-") and ch[1:].isdigit():
                to_ban = NameId(ch, int(ch))
            elif ch.isdigit():
                to_ban = NameId(ch, int("-100" + ch))
            else:
                chat = await self.bot.get_chat(ch)
                to_ban = NameId(ch, chat.id)

        except Exception:
            await msg.answer(f"Error: chat {ch} not found")
            return

        results = []
        for g in groups:
            res = await self.ban_from_a_group(msg.from_user, g, to_ban)
            results.append(res)

        await msg.answer("\n".join(results))

    async def run(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)


async def main(token: str):
    bot = BanChannelBot(token)
    await bot.run()


if __name__ == "__main__":
    import os
    import sys

    token = os.getenv("TOKEN")

    if not token:
        sys.exit("Please set TOKEN environment variable")

    asyncio.run(main(token))
