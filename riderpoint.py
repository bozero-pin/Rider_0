#!/usr/bin/python3

import asyncio
from typing import NamedTuple
import logging

from aiogram import Bot, Dispatcher, types, loggers
from aiogram import exceptions
from aiogram.filters.command import Command

logger = logging.getLogger(__name__)

class NameId(NamedTuple):
    name: str
    id: int | str

    def __str__(self):
        return self.name

class BanChannelBot:
    def __init__(self, token):

        bot = Bot(token=token)
        dp = Dispatcher()
        dp.message(Command('banch'))(self.ban_channel)

        self.dp = dp
        self.bot = bot

    async def ban_from_a_group(self, u: types.User, group: NameId, to_ban: NameId) -> str:
        bot = self.bot
        try:
            admins = await bot.get_chat_administrators(group.id)
        except exceptions.TelegramNotFound:
            return f'Error: chat {group} not found.'

        admin_ids = [cm.user.id for cm in admins]
        if u.id not in admin_ids:
            return f'Error: you are not an admin of {group}.'

        if bot.id not in admin_ids:
            return f"Error: I'm not an admin of {group}."

        if await bot.ban_chat_sender_chat(chat_id=group.id, sender_chat_id=to_ban.id):
            return f"Banned {to_ban} from {group}."
        else:
            return f"Failed to ban {to_ban} from {group}."

    async def ban_channel(self, msg: types.Message) -> None:
        logger.info('Received %s', msg.text)
        bot = self.bot
        _, *parts = msg.text.split()

        if not parts:
            return

        ch, *group_names = parts

        if not group_names:
            groups = [NameId(msg.chat.username, msg.chat.id)]
        else:
            groups = [NameId(x, x) for x in group_names]

        try:
            if ch.startswith('-') and ch[1:].isdigit():
                to_ban = NameId(ch, int(ch))
            elif ch.isdigit():
                to_ban = NameId(ch, int('-100' + ch))
            else:
                chat = await bot.get_chat(chat_id=ch)
                to_ban = NameId(ch, chat.id)

        except exceptions.TelegramNotFound:
            await bot.send_message(
                chat_id=msg.chat.id,
                text=f'Error: chat {ch} not found',
                reply_to_message_id=msg.message_id,
            )
            return

        reply = []

        for g in groups:
            reply.append(await self.ban_from_a_group(msg.from_user, g, to_ban))

        await bot.send_message(
            chat_id=msg.chat.id,
            text='\n'.join(reply),
            reply_to_message_id=msg.message_id,
        )

    async def run(self) -> None:
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)

async def main(bot_token):
    bcbot = BanChannelBot(bot_token)
    await bcbot.run()

if __name__ == '__main__':
    import os
    import sys

    token = os.environ.pop('TOKEN', None)

    if not token:
        sys.exit('Please pass bot token in environment variable TOKEN.')

    loggers.event.setLevel(logging.WARNING)

    try:
        asyncio.run(main(token))
    except KeyboardInterrupt:
        pass
