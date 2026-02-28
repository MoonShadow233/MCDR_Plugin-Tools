from mcdreforged.api.all import *
from .utils import ChatEvent
from .tools import get_command_source, get_player_name, get_content, dimension_to_command


class GamemodeTp:
    def __init__(self, server: PluginServerInterface):
        self.server = server
    
    @new_thread("GetPlayerInfo")
    def get_player_info(self, source):
        cs = get_command_source(source)
        if cs is None or not cs.is_player:
            return
        
        if not self.check_gamemode(source):
            return
        
        args = get_content(source).split()
        
        if len(args) > 4:
            self.tpdebug(source)
            return
        elif len(args) == 4:
            self.handle_full_coordinates(source, args)
        elif len(args) == 3:
            self.handle_partial_coordinates(source, args)
        elif len(args) == 2:
            self.handle_two_arguments(source, args)
        else:
            self.tpdebug(source)
            return
    
    def check_gamemode(self, source):
        if self.Authentication(source):
            return True
            
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            return False
            
        player_name = get_player_name(source)
        try:
            gamemode = str(api.get_player_info(player_name, 'playerGameType'))
            if gamemode != '3':
                self.server.tell(player_name, '§c你不是旁观模式，无法使用此指令！请切换到旁观模式后再试。')
                self.tpdebug(source)
                return False
        except:
            return False
        return True
    
    def parse_coordinates(self, x_str, y_str, z_str, player):
        try:
            x = float(x_str)
            y = float(y_str)
            z = float(z_str)
            return x, y, z
        except ValueError:
            self.server.tell(player, '§c你确定你输入的是数字吗？（必须是双浮点double）')
            return None
    
    def execute_teleport(self, player, x, y, z):
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            self.server.tell(player, '§cMinecraft Data API未启用')
            return
            
        try:
            player_dim = api.get_player_dimension(player)
            dimension = dimension_to_command(player_dim)
            self.server.execute(f'execute in {dimension} run tp {player} {x} {y} {z}')
        except Exception as e:
            self.server.tell(player, f'§c传送失败: {str(e)}')
    
    def handle_full_coordinates(self, source, args):
        player_name = get_player_name(source)
        x, y, z = args[1], args[2], args[3]
        coords = self.parse_coordinates(x, y, z, player_name)
        
        if coords is None:
            self.tpdebug(source)
            return
        
        self.execute_teleport(player_name, *coords)
    
    def handle_partial_coordinates(self, source, args):
        player_name = get_player_name(source)
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            return
            
        try:
            player_pos = api.get_player_coordinate(player_name)
            
            x = args[1]
            y = player_pos.y
            z = args[2]
            
            coords = self.parse_coordinates(x, y, z, player_name)
            
            if coords is None:
                self.tpdebug(source)
                return
            
            self.execute_teleport(player_name, *coords)
        except Exception as e:
            self.server.tell(player_name, f'§c获取坐标失败: {str(e)}')
    
    def handle_two_arguments(self, source, args):
        player_name = get_player_name(source)
        target = args[1]
        
        dimension_map = {
            '主世界': ('minecraft:overworld', 0, 64, 0),
            '地狱': ('minecraft:the_nether', 0, 120, 0),
            '下界': ('minecraft:the_nether', 0, 120, 0),
            '下届': ('minecraft:the_nether', 0, 120, 0),
            '末地': ('minecraft:the_end', 0, 64, 0)
        }
        
        if target in dimension_map:
            dimension, x, y, z = dimension_map[target]
            self.server.execute(f'execute in {dimension} run tp {player_name} {x} {y} {z}')
        else:
            self.server.execute(f'tp {player_name} {target}')
    
    def tpdebug(self, source):
        ChatEvent(self.server, source, type="info", msg=(
            '§c语法错误！正确语法：!tp <x> [<y>] <z>|!tp [<玩家>|<维度>]|!tp help\n'
            '§c如果你想传送到某个坐标，请使用!tp <x> [<y>] <z>，其中y是可选的，默认为64。\n'
            '§c如果你想传送到某个玩家，请使用!tp <玩家>。\n'
            '§c如果你想传送到某个维度，请使用!tp <维度> 注意：维度只能有 主世界 下界/地狱/下届 末地 三种选择\n'
            '§c注意：!tp <维度>是单独的指令，不能和其他参数一起使用！'
        ), log=None, say=False).guide()

    def Authentication(self, source):
        player_name = get_player_name(source)
        if not player_name:
            return False
        try:
            perm = self.server.get_permission_level(player_name)
            return perm >= 3
        except:
            return False


def register(server: PluginServerInterface):
    def on_tp_command(source):
        GamemodeTp(server).get_player_info(source)
    server.register_command(Literal('!tp').runs(on_tp_command))
