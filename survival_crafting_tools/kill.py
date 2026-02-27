from mcdreforged.api.all import *
from .utils import ChatEvent


class Kill:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def kill(self, info: Info):
        if info.source.is_player:
            player_name = info.source.player
            self.server.execute(f'kill {player_name}')
            ChatEvent(self.server, info, type="info", msg=f'欸 {player_name} 你怎么似了啊？！', log=f"玩家 {player_name} 自杀", say=True).guide()
