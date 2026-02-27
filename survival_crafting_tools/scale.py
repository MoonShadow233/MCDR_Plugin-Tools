from mcdreforged.api.all import *
from .utils import ChatEvent


class Scale:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def scale(self, info: Info):
        if not info.source.is_player or not info.content.startswith('!sc'):
            return
            
        args = info.content.split()
        if len(args) != 2:
            ChatEvent(self.server, info, type="info", msg="§c语法错误：正确语法!sc <数值>", log="sc 语法错误", say=False).guide()
            return
        
        try:
            scale_value = float(args[1])
            if scale_value <= 0:
                ChatEvent(self.server, info, type="info", msg="§c缩放值必须大于0！", log="sc 参数错误", say=False).guide()
                return
        except ValueError:
            ChatEvent(self.server, info, type="info", msg="§c缩放值必须是一个数字！", log="sc 参数非数字", say=False).guide()
            return
            
        try:
            self.server.execute(f'attribute {info.source.player} minecraft:scale base set {scale_value}')
            ChatEvent(self.server, info, type="info", msg=f"§a成功将你的大小设置为 {scale_value}！", log=f"设置缩放: {scale_value}", say=False).guide()
        except Exception as e:
            ChatEvent(self.server, info, type="error", msg=f"§c发生错误: {str(e)}", say=False).guide()
