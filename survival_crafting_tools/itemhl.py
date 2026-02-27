from mcdreforged.api.all import *
from .utils import ChatEvent


class ItemHL:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    @new_thread("ItemHighlight")
    def highlight_item(self, info: Info):
        if not info.source.is_player:
            return
            
        if info.content == '!uitemhl':
            self.server.execute('execute as @e[type=item] run data merge entity @s {Glowing:0b}')
            ChatEvent(self.server, info, type="info", msg='§a所有掉落物高亮已取消，输入!itemhl开启', log='取消物品高亮', say=False).guide()
            return
            
        elif info.content == '!itemhl':
            self.server.execute('execute as @e[type=item] run data merge entity @s {Glowing:1b}')
            ChatEvent(self.server, info, type="info", msg='§a所有掉落物已高亮，输入!uitemhl取消', log='开启物品高亮', say=False).guide()
