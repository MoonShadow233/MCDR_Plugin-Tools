from mcdreforged.api.all import *
from .utils import ChatEvent


class GamemodeTp:
    """
    旁观模式传送类
    允许玩家在旁观模式下进行传送操作
    """
    
    def __init__(self, server: PluginServerInterface):
        self.server = server
    
    @new_thread("GetPlayerInfo")
    def get_player_info(self, info):
        """
        主入口函数，处理!tp命令
        根据参数数量和类型分发到不同的处理函数
        """
        if not info.source.is_player or not info.content.startswith('!tp'):
            return
        
        if not self.check_gamemode(info):
            return
        
        args = info.content.split()
        
        if len(args) > 4:
            self.tpdebug(info)
            return
        elif len(args) == 4:
            self.handle_full_coordinates(info, args)
        elif len(args) == 3:
            self.handle_partial_coordinates(info, args)
        elif len(args) == 2:
            self.handle_two_arguments(info, args)
        else:
            self.tpdebug(info)
            return
    
    def check_gamemode(self, info):
        """
        检查玩家游戏模式
        只有旁观模式（游戏模式3）才能使用传送功能
        :param info: 服务器信息对象
        :return: 是旁观模式，op返回True，否则返回False
        """
        if self.Authentication(info):
            return True
            
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            return False
            
        try:
            gamemode = str(api.get_player_info(info.source.player, 'playerGameType'))
            if gamemode != '3':
                self.server.tell(info.source.player, '§c你不是旁观模式，无法使用此指令！请切换到旁观模式后再试。')
                self.tpdebug(info)
                return False
        except:
            return False
        return True
    
    def parse_coordinates(self, x_str, y_str, z_str, player):
        """
        解析坐标字符串为浮点数
        :param x_str: X坐标字符串
        :param y_str: Y坐标字符串
        :param z_str: Z坐标字符串
        :param player: 玩家名称（用于错误提示）
        :return: 解析成功返回(x, y, z)元组，失败返回None
        """
        try:
            x = float(x_str)
            y = float(y_str)
            z = float(z_str)
            return x, y, z
        except ValueError:
            self.server.tell(player, '§c你确定你输入的是数字吗？（必须是双浮点double）')
            return None
    
    def execute_teleport(self, player, x, y, z):
        """
        执行传送命令
        根据玩家当前维度执行对应的传送命令
        :param player: 玩家名称
        :param x: 目标X坐标
        :param y: 目标Y坐标
        :param z: 目标Z坐标
        """
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            self.server.tell(player, '§cMinecraft Data API未启用')
            return
            
        try:
            player_dim = api.get_player_dimension(player)
            
            dimension_map = {
                0: 'minecraft:overworld',
                -1: 'minecraft:the_nether',
                1: 'minecraft:the_end'
            }
            
            if player_dim in dimension_map:
                dimension = dimension_map[player_dim]
                self.server.execute(f'execute in {dimension} run tp {player} {x} {y} {z}')
            else:
                self.server.tell(player, '§c无法识别的维度，请联系管理员#101')
        except Exception as e:
            self.server.tell(player, f'§c传送失败: {str(e)}')
    
    def handle_full_coordinates(self, info, args):
        """
        处理完整坐标传送
        格式: !tp x y z
        :param info: 服务器信息对象
        :param args: 命令参数列表
        """
        x, y, z = args[1], args[2], args[3]
        coords = self.parse_coordinates(x, y, z, info.source.player)
        
        if coords is None:
            self.tpdebug(info)
            return
        
        self.execute_teleport(info.source.player, *coords)
    
    def handle_partial_coordinates(self, info, args):
        """
        处理部分坐标传送
        格式: !tp x z（Y坐标使用玩家当前坐标）
        :param info: 服务器信息对象
        :param args: 命令参数列表
        """
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            return
            
        try:
            player_pos = api.get_player_coordinate(info.source.player)
            
            x = args[1]
            y = player_pos.y
            z = args[2]
            
            coords = self.parse_coordinates(x, y, z, info.source.player)
            
            if coords is None:
                self.tpdebug(info)
                return
            
            self.execute_teleport(info.source.player, *coords)
        except Exception as e:
            self.server.tell(info.source.player, f'§c获取坐标失败: {str(e)}')
    
    def handle_two_arguments(self, info, args):
        """
        处理两个参数的传送
        格式: !tp <维度> 或 !tp <玩家>
        :param info: 服务器信息对象
        :param args: 命令参数列表
        """
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
            self.server.execute(f'execute in {dimension} run tp {info.source.player} {x} {y} {z}')
        else:
            self.server.execute(f'tp {info.source.player} {target}')
    
    def tpdebug(self, info: Info):
        """
        显示传送命令的帮助信息
        :param info: 服务器信息对象
        """
        ChatEvent(self.server, info, type="info", msg=(
            '§c语法错误！正确语法：!tp <x> [<y>] <z>|!tp [<玩家>|<维度>]|!tp help\n'
            '§c如果你想传送到某个坐标，请使用!tp <x> [<y>] <z>，其中y是可选的，默认为64。\n'
            '§c如果你想传送到某个玩家，请使用!tp <玩家>。\n'
            '§c如果你想传送到某个维度，请使用!tp <维度> 注意：维度只能有 主世界 下界/地狱/下届 末地 三种选择\n'
            '§c注意：!tp <维度>是单独的指令，不能和其他参数一起使用！'
        ), log=None, say=False).guide()

    def Authentication(self, info: Info):
        """
        鉴权,如果为op则跳过模式检查
        :param info: 服务器信息对象
        :return: True/False
        """
        if not info.source.is_player:
            return False
        try:
            perm = self.server.get_permission_level(info.source.player)
            return perm >= 3
        except:
            return False
