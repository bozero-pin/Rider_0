#!/usr/bin/python3

import asyncio
import logging
from typing import NamedTuple

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NameId(NamedTuple):
    name: str
    id: int | str

    def __str__(self):
        return self.name


class BanChannelBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()

        # register command
        self.dp.message.register(self.ban_channel, Command("banch"))

    async def ban_from_a_group(
        self,
        u: types.User,
        group: NameId,
        to_ban: NameId
    ) -> str:
        bot = self.bot

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
