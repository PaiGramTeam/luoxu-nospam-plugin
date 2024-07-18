import contextlib

from telethon import TelegramClient
from telethon.tl.custom import Message
from telethon.tl.types import PeerChannel


class NoSpamPlugin:
    def __init__(self, indexer, client: TelegramClient):
        self.client = client
        self.groups = [int(i) for i in indexer.config['plugin']['nospam']['groups'] if i]
        self.keywords = indexer.config['plugin']['nospam']['keywords']
        self.notice = indexer.config['plugin']['nospam']['notice']

    async def on_message(self, msg: Message, text: str):
        # 检查 cid
        if not (isinstance(msg.peer_id, PeerChannel) and msg.peer_id.channel_id in self.groups):
            return
        # 检查关键词
        need_run = next((True for key in self.keywords if key in text), False)
        if not need_run:
            return
        msg2: Message = await msg.reply(self.notice)
        if msg2:
            with contextlib.suppress(Exception):
                await msg.delete()
            with contextlib.suppress(Exception):
                await msg2.delete()


def register(indexer, client):
    plugin = NoSpamPlugin(indexer, client)
    indexer.dbstore.add_msg_ocr_handler(plugin.on_message)
