from mcdreforged.api.all import *
from .utils import ChatEvent
from .tools import get_command_source, get_player_name


class Scale:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def check_version(self):
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            return None
        try:
            version = api.get_server_version()
            return version
        except:
            return None
    
    def parse_version(self, version_str):
        if not version_str:
            return None
        import re
        match = re.search(r'(\d+)\.(\d+)(?:\.(\d+))?', version_str)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3)) if match.group(3) else 0
            return (major, minor, patch)
        return None
        
    def scale(self, source, scale_value: float):
        cs = get_command_source(source)
        if cs is None or not cs.is_player:
            return
            
        player_name = get_player_name(source)
        
        version_str = self.check_version()
        if version_str:
            version = self.parse_version(version_str)
            if version and version < (1, 20, 0):
                ChatEvent(self.server, source, type="info", msg="§c游戏版本不支持！scale属性需要 Minecraft 1.20 或更高版本。", log="版本不支持", say=False).guide()
                return
        
        if scale_value <= 0:
            ChatEvent(self.server, source, type="info", msg="§c缩放值必须大于0！", log="sc 参数错误", say=False).guide()
            return
            
        try:
            self.server.execute(f'attribute {player_name} minecraft:scale base set {scale_value}')
            ChatEvent(self.server, source, type="info", msg=f"§a成功将你的大小设置为 {scale_value}！", log=f"设置缩放: {scale_value}", say=False).guide()
        except Exception as e:
            ChatEvent(self.server, source, type="error", msg=f"§c发生错误: {str(e)}", say=False).guide()


def register(server: PluginServerInterface):
    def on_scale_command(source, ctx):
        scale_value = ctx['scale']
        Scale(server).scale(source, scale_value)
    server.register_command(
        Literal('!sc').then(
            Float('scale').at_min(0.1).at_max(10).runs(on_scale_command)
        )
    )
