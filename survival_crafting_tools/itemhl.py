from mcdreforged.api.all import *
from .utils import ChatEvent
from .tools import get_command_source, get_content


class ItemHL:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    @new_thread("ItemHighlight")
    def highlight_item(self, source):
        cs = get_command_source(source)
        if cs is None or not cs.is_player:
            return
            
        content = get_content(source)
            
        if 'uitemhl' in content:
            self.server.execute('execute as @e[type=item] run data merge entity @s {Glowing:0b}')
            ChatEvent(self.server, source, type="info", msg='§a所有掉落物高亮已取消，输入!itemhl开启', log='取消物品高亮', say=False).guide()
            return
            
        else:
            self.server.execute('execute as @e[type=item] run data merge entity @s {Glowing:1b}')
            ChatEvent(self.server, source, type="info", msg='§a所有掉落物已高亮，输入!uitemhl取消', log='开启物品高亮', say=False).guide()


def register(server: PluginServerInterface):
    def on_itemhl_command(source):
        ItemHL(server).highlight_item(source)
    server.register_command(Literal('!itemhl').runs(on_itemhl_command))
    server.register_command(Literal('!uitemhl').runs(on_itemhl_command))
