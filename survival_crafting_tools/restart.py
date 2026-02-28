from mcdreforged.api.all import *
import time
from .utils import ChatEvent
from .tools import get_player_name


class Restart:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def restart(self, source):
        player_name = get_player_name(source)
        if not player_name:
            return
            
        perm = self.server.get_permission_level(player_name)
        if perm >= 3:
            ChatEvent(self.server, source, type="info", msg=f"由{player_name}执行的重启！", log=f"重启: {player_name}", say=True).guide()
            i = 10
            while i >= 0:
                ChatEvent(self.server, source, type="info", msg=f"服务器将在{i}秒后重启！", log=f"重启倒计时: {i}", say=True).guide()
                i -= 1
                time.sleep(1)

            self.server.restart()
        else:
            ChatEvent(self.server, source, type="error", msg="§c你没有权限重启服务器！", log="没有权限重启", say=False).guide()


def register(server: PluginServerInterface):
    def on_restart_command(source):
        Restart(server).restart(source)
    server.register_command(Literal('!restart').runs(on_restart_command))
