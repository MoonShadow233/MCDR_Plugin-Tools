from mcdreforged.api.all import *
from .utils import ChatEvent
from .tools import get_player_name


class Kill:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def kill(self, source):
        player_name = get_player_name(source)
        if player_name:
            self.server.execute(f'kill {player_name}')
            ChatEvent(self.server, source, type="info", msg=f'欸 {player_name} 你怎么似了啊？！', log=f"玩家 {player_name} 自杀", say=True).guide()


def register(server: PluginServerInterface):
    def on_kill_command(source):
        Kill(server).kill(source)
    server.register_command(Literal('!kill').runs(on_kill_command))
