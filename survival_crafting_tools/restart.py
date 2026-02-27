from mcdreforged.api.all import *
import time
from .utils import ChatEvent


class Restart:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def restart(self, info: Info):
        if not info.source.is_player:
            return
            
        perm = self.server.get_permission_level(info.source.player)
        if perm >= 3:
            ChatEvent(self.server, info, type="info", msg=f"由{info.source.player}执行的重启！", log=f"重启: {info.source.player}", say=True).guide()
            i = 10
            while i >= 0:
                ChatEvent(self.server, info, type="info", msg=f"服务器将在{i}秒后重启！", log=f"重启倒计时: {i}", say=True).guide()
                i -= 1
                time.sleep(1)

            self.server.restart()
        else:
            ChatEvent(self.server, info, type="error", msg="§c你没有权限重启服务器！", log="没有权限重启", say=False).guide()
