from mcdreforged.api.all import * 
import time
import os
import random
import json
#这些东西并没有什么参考价值
#我也看不懂:)
#如果发现了bug也欢迎在git提交issuse
# GPL-3.0 License - Copyright (c) 2024 MoonShadow233


# These notes might not be very helpful
# Honestly, Im not sure about this part :)
# Bug? Feel free to create an issue on Git

# To prevent people from using the plugin without reading the instructions, 
# some obfuscation has been applied to the plugin activation check
# GPL-3.0 License - Copyright (c) 2024 MoonShadow233


PLUGIN_ID = 'tools'
PLUGIN_NAME = 'Tools'
VERSION = '1.0.2'

def on_load(server: PluginServerInterface, prev_module):
    loaded = server.load_config_simple(
        'config.json',
        {
            'settings': Config.settings,
            'message': Config.message,
        }
    )
    config = Config()
    try:
        if isinstance(loaded, dict):
            config.settings = loaded.get('settings', Config.settings)
    except Exception as e:
        server.logger.error(f"加载配置时出错: {e}")
    server.logger.info('插件已加载')
    if not config.settings.get('enable_tools', True):
        global PLUGIN_ENABLED
        PLUGIN_ENABLED = False
        server.say('§cTools插件已被禁用！请查看插件github中启用插件的方法')
        return
    PLUGIN_ENABLED = True
    server.execute('carpet commandPlayer 0')
    server.execute('carpet setDefault commandPlayer 0')
    server.execute('difficulty hard')
    server.say('====================================================')
    server.say(f'§aTools插件 by MoonShadow233 加载成功！版本：{VERSION}')
    server.say('====================================================')


def on_unload(server: PluginServerInterface):
    server.logger.info('插件已卸载')

def on_info(server: PluginServerInterface, info: Info):
    command(server, info)

def command(server: PluginServerInterface, info: Info):
    if info.content is None or PLUGIN_ENABLED == False:
        return
    if Config.settings.get('enable_betterchat', True):
        BetterChat(server).Chat(info)
    if not '!' in info.content:
        return
    if Config.settings.get('enable_kill', True):
        Kill(server).kill(info)
    if Config.settings.get('enable_here', True):
        Here(server, info).userinfo(info)
    if Config.settings.get('enable_tp', True):
        GamemodeTp(server).get_player_info(info)
    if Config.settings.get('enable_restart', True):
        Restart(server, info).restart(info)
    if Config.settings.get('enable_random', True):
        Random(server).ListNumber(info)
    if Config.settings.get('enable_fakeplayer', True):
        FakePlayer(server, info).FakePlayer(info)
    if Config.settings.get('enable_manyplayer', True):
        ManyPlayer(server, info).ManyPlayer(info)
    if Config.settings.get('enable_scale', True):
        Scale(server).scale(info)
    # console(server, info)


class Config(Serializable):
    settings: dict = {
        'enable_here': True,
        'enable_kill': True,
        'enable_tp': True,
        'enable_restart': True,
        'enable_random': True,
        'enable_fakeplayer': True,
        'enable_manyplayer': True,
        'enable_betterchat': True,
        'enable_scale': True,
        'enable_tools': False
    }
    message: dict = {
        'welcome_message': '§c欢迎 §a{player} §c加入游戏！'

    }



# def console(server: PluginServerInterface, info: Info):
#     if info.is_player or info.content is None or not "moved" in info.content:
#         return
#     ops_path = os.path.join('server', 'ops.json')
#     op_names = []
#     op_additon = []
#     try:
#         with open(ops_path, 'r', encoding='utf-8') as ops_file:
#             ops_data = json.load(ops_file)
#         for op in ops_data:
#             if isinstance(op, dict) and 'name' in op:
#                 op_names.append(op['name'])
#     except Exception as e:
#         server.logger.error(f"读取 ops.json 时出错: {e}")
#         server.say("§c无法读取服务器管理员列表，请检查服务器日志以获取详细信息。")
#         return
#     local_time = time.localtime()
#     hh_mm_ss = f"{local_time.tm_hour:02d}:{local_time.tm_min:02d}:{local_time.tm_sec:02d}"
#     if "moved" in info.content:
#         for op in op_names:
#             server.tell(op, f'§a原版反作弊警告§c[Server][{hh_mm_ss}] {info.content}')
#         for op in op_additon:
#             server.tell(op, f'§a原版反作弊警告§c[Server][{hh_mm_ss}] {info.content}')

class Here:
    def __init__(self, server: PluginServerInterface, info:Info):
        self.server = server
    def get_player_location(self, player):
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            self.debug_log("Minecraft Data API:off")
            return None, None
    
        try:
            self.debug_log(f"Try: 获取 {player} 的位置...")
            @new_thread('HereQuery')
            def query_location():
                try:
                    pos = api.get_player_coordinate(player)
                    dim = api.get_player_dimension(player)
                    self.debug_log(f"Pos: {pos} Dim: {dim}")
                
                    if pos is None or dim is None:
                        self.server.tell(player, '§r[ERROR] 获取维度或位置失败，请联系管理员#100')
                        return
                        
                    x, y, z = int(round(pos.x, 1)), int(round(pos.y, 1)), int(round(pos.z, 1))
                    z = z - 1
                    message = f"§a§l{player}§r 在"

                    if dim == 0:  # 主世界
                        message += f"§r[§2主世界§r"
                    elif dim == -1:  # 下界
                        message += f"§r[§c下界§r"
                    elif dim == 1:  # 末地
                        message += f"§r[§2末地§r"




                    if dim == 0:  # 主世界
                        message += f"§a§n§l {x} {y} {z} §r]"
                    elif dim == -1:  # 下界
                        message += f"§6§n§l {x} {y} {z} §r]"
                    elif dim == 1:  # 末地
                        message += f"§e§n§l {x} {y} {z} §r]"

                
                    if dim == 0:  # 主世界
                        message += f" ==> [§c下界§r §6§n§l{int(round(x/8, 1))} {y} {int(round(z/8, 1))}§r]"
                    elif dim == -1:  # 下界
                        message += f" ==> [§2主世界§a §6§n§l{round(x*8, 1)} {y} {round(z*8, 1)}§r]"
                # elif dim == 1:  # 末地
                #     message += "==> [] Not A Number."
                
                    self.server.say(message)
                    self.server.execute(f'tellraw @a [{{"hoverEvent":{{"action":"show_text","contents":{{"text":"!tp"}}}},"text": "[旁观TP坐标]§r","color":"gold","clickEvent": {{"action": "suggest_command","value": "!tp {x} {y} {z}"}}}},{{"text":"   [显示路径点]","color":"yellow","clickEvent":{{"action":"run_command","value":"/highlight {x} {y} {z}"}},"hoverEvent":{{"action":"show_text","contents":{{"text":"/highlight"}}}}}}]')
                except Exception as e:
                    self.debug_log(f"[ERROR] {str(e)} 请联系管理员#102")
                    self.server.say(f"[ERROR]: {str(e)} 请联系管理员#102")
        
            query_location() 
    
        except Exception as e:
            self.debug_log(f"[ERROR]: {str(e)} 请联系管理员#103")
            return None, None

    def debug_log(self, message: str):
        self.server.logger.info(f"[HerePlugin] {message}")
    
    def userinfo(self, info: Info):
        if not info.is_player or (info.content != '!here' and info.content != '!h'):
            return
        else:
            self.get_player_location(info.player)

class Kill:
    def __init__(self, server:PluginServerInterface):
        self.server = server
        pass
    def kill(self, info: Info):
        if info.is_player and info.content.strip().lower() == '!kill': 
            player_name = info.player  
            self.server.execute(f'kill {player_name}')
            self.server.say(f'欸 {player_name} 你怎么似了啊？！')


class GamemodeTp():
    """
    旁观模式传送类
    允许玩家在旁观模式下进行传送操作
    """
    
    def __init__(self, server: PluginServerInterface):
        self.server = server
        pass
    
    @new_thread("GetPlayerInfo")
    def get_player_info(self, info):
        """
        主入口函数，处理!tp命令
        根据参数数量和类型分发到不同的处理函数
        """
        if not self.validate_command(info):
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
    
    def validate_command(self, info):
        """
        验证命令有效性
        检查是否为玩家发送的!tp命令
        :param info: 服务器信息对象
        :return: 命令有效返回True，否则返回False
        """
        if not info.is_player or not info.content.startswith('!tp'):
            return False
        return True
    
    def check_gamemode(self, info):
        """
        检查玩家游戏模式
        只有旁观模式（游戏模式3）才能使用传送功能
        :param info: 服务器信息对象
        :return: 是旁观模式，op返回True，否则返回False
        """
        api = self.server.get_plugin_instance('minecraft_data_api')
        gamemode = str(api.get_player_info(info.player, 'playerGameType'))
        if not self.Authentication(info):
            if gamemode != '3':
                self.server.tell(info.player, '§c你不是旁观模式，无法使用此指令！请切换到旁观模式后再试。')
                self.tpdebug(info)
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
    
    def handle_full_coordinates(self, info, args):
        """
        处理完整坐标传送
        格式: !tp x y z
        :param info: 服务器信息对象
        :param args: 命令参数列表
        """
        x, y, z = args[1], args[2], args[3]
        coords = self.parse_coordinates(x, y, z, info.player)
        
        if coords is None:
            self.tpdebug(info)
            return
        
        self.server.tell(info.player, f"§c你正在尝试传送到 {x} {y} {z}##2")
        self.execute_teleport(info.player, *coords)
    
    def handle_partial_coordinates(self, info, args):
        """
        处理部分坐标传送
        格式: !tp x z（Y坐标使用玩家当前坐标）
        :param info: 服务器信息对象
        :param args: 命令参数列表
        """
        api = self.server.get_plugin_instance('minecraft_data_api')
        player_pos = api.get_player_coordinate(info.player)
        
        x = args[1]
        y = player_pos.y
        z = args[2]
        
        coords = self.parse_coordinates(x, y, z, info.player)
        
        if coords is None:
            self.tpdebug(info)
            return
        
        self.server.tell(info.player, f"§c你正在尝试传送到 {x} {y} {z}##3")
        self.execute_teleport(info.player, *coords)
    
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
            self.server.execute(f'execute in {dimension} run tp {info.player} {x} {y} {z}')
        else:
            self.server.tell(info.player, f"§c你正在尝试传送到玩家 {target}##4")
            self.server.execute(f'tp {info.player} {target}')
    
    def tpdebug(self, info: Info):
        """
        显示传送命令的帮助信息
        :param info: 服务器信息对象
        """
        self.server.tell(info.player, '§c语法错误！正确语法：!tp <x> [<y>] <z>|!tp [<玩家>|<维度>]|!tp help') 
        self.server.tell(info.player, '§c如果你想传送到某个坐标，请使用!tp <x> [<y>] <z>，其中y是可选的，默认为64。') 
        self.server.tell(info.player, '§c如果你想传送到某个玩家，请使用!tp <玩家>。') 
        self.server.tell(info.player, '§c如果你想传送到某个维度，请使用!tp <维度> 注意：维度只能有 主世界 下界/地狱/下届 末地 三种选择') 
        self.server.tell(info.player, '§c注意：!tp <维度>是单独的指令，不能和其他参数一起使用！') 

    def Authentication(self,info: Info):
        """
        鉴权,如果为op则跳过模式检查
        :param info: 服务器信息对象
        :return: True/False
        """
        if not info.is_player :
            return False
        perm = self.server.get_permission_level(info.player) 
        if perm >= 3:
            return True
        else:           
            return False


class Restart():
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server
    def restart(self, info: Info):
        if not info.is_player or info.content != '!!restart': 
            return
        perm = self.server.get_permission_level(info.player) 
        if perm >= 3:
            self.server.say(f"由{info.player}执行的重启！")
            i = 10
            while i >= 0:
                self.server.say(f"服务器将在{i}秒后重启！")
                i -= 1
                time.sleep(1)

            self.server.restart()
        else:
            self.server.tell(info.player, "§c你没有权限重启服务器！") 

class Random():
    def __init__(self, server: PluginServerInterface):
        self.server = server

    def ListNumber(self, info: Info):
        if not info.is_player or not info.content.split( )[0] == '!l':
            return
        try:
            parts = info.content.split()
            if len(parts) < 2:
                num = random.randint(1, 10)
                self.server.say(f'§a[骰子] §r- §b生成的数为: §e{num}')

                return
            range_str = parts[1] 
            # self.server.say(range_str)
            range1 = int(range_str.split('-')[0])
            range2 = int(range_str.split('-')[1])
            if range1 > range2:
                self.server.tell(info.player, '§c[骰子] §r- §c范围错误：前一个数必须小于后一个数！') 
                return
            elif range1 == range2:
                self.server.tell(info.player, '§c[骰子] §r- §c范围错误：两个数不能相等！') 
                return
            
            num = random.randint(range1,range2)
            self.server.say(f'§a[骰子] §r- §b生成的数为: §e{num}') 
        except Exception as e:
            self.server.tell(info.player, f'§c[骰子] §r- §c发生错误: {str(e)}') 

class FakePlayer():
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server

    def TurnPlayer(self, info: Info, target_player: str): 
        self.server.execute(f'tellraw {info.player} [{{"text":"§b玩家控制 -§a{target_player}   -   §d旋转选项"}}]')
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b向后看"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !t"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} turn back"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b向右看"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !t"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} turn right"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b向左看"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !t"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} turn left"}}}}]') 

    
    def MovePlayer(self, info: Info, target_player: str):
        self.server.execute(f'tellraw {info.player} [{{"text":"§b玩家控制 -§a{target_player}   -   §d移动选项"}}]')
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b向前"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !move"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} move forward"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b向后"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !move"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} move backward"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b向右"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !move"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} move right"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b向左"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !move"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} move left"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b疾跑"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !move"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} sprint"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b潜行"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !move"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} sneak"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b跳跃"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"!p !move"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} jump"}}}}]') 

    def PlayerInventory(self, info: Info, target_player: str):
        self.server.execute(f'tellraw {info.player} [{{"text":"§b玩家控制 -§a{target_player}   -   §d背包选项"}}]')
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b扔出一次"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"/player name drop"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} drop"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b全扔"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"/player name dropStack all"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} dropStack all"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b扔出一组"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"/player name dropStack"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} dropStack"}}}}]') 






    def FPlayerC(self, info: Info, target_player: str):
        self.server.execute(f'tellraw {info.player} [{{"text":"Tools/假人控制插件","color":"aqua"}}]')
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b下线玩家"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"/player {target_player} kill"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} kill"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b右键"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"/player {target_player} use"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} use"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b左键"}},{{"text":"  §c[点击执行]","hoverEvent":{{"action":"show_text","value":"/player {target_player} attack"}},"clickEvent":{{"action":"run_command","value":"/player {target_player} attack"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b移动"}},{{"text":"  §c[点击选择]","hoverEvent":{{"action":"show_text","value":"!p !move"}},"clickEvent":{{"action":"suggest_command","value":"!p !move {target_player}"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b背包"}},{{"text":"  §c[点击选择]","hoverEvent":{{"action":"show_text","value":"!p !b"}},"clickEvent":{{"action":"suggest_command","value":"!p !b {target_player}"}}}}]') 
        self.server.execute(f'tellraw {info.player} [{{"text":"- §b旋转"}},{{"text":"  §c[点击选择]","hoverEvent":{{"action":"show_text","value":"!p !t"}},"clickEvent":{{"action":"suggest_command","value":"!p !t {target_player}"}}}}]') 


    @new_thread("FakePlayer")
    def FakePlayer(self, info: Info):
        if not info.is_player or not info.content.startswith('!p'): 
            return
        
        args = info.content.split() 
        
        if len(args) >= 2:
            target_player = args[1]
            if target_player == '!move':
                if len(args) < 3:
                    self.server.tell(info.player, '§c语法错误！正确语法：!p !move <玩家>') 
                    return
                Splayer = args[2]
                self.MovePlayer(info, Splayer) 
                
            elif target_player == '!b':
                if len(args) < 3:
                    self.server.tell(info.player, '§c语法错误！正确语法：!p !b <玩家>') 
                    return
                Splayer = args[2]
                self.PlayerInventory(info, Splayer) 
            elif target_player == '!t':
                if len(args) < 3:
                    self.server.tell(info.player, '§c语法错误！正确语法：!p !t <玩家>') 
                    return
                Splayer = args[2]
                self.TurnPlayer(info, Splayer) 
            else:
                
                self.server.execute(f'tellraw {info.player} [{{"text":"§b玩家控制 - §a{target_player}"}}]') 
                self.FPlayerC(info, target_player) 


            return
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            self.server.tell(info.player, '§cMinecraft Data API未启用，无法使用此功能！请联系管理员#106') 
            return
        try:
            playerlist = api.get_server_player_list()
            
            if playerlist.amount > 0:
                player_names_list = playerlist.players
                self.server.say(f"§a在线: §6{playerlist.amount}§a/§6{playerlist.limit}§a")
                try:
                    i = 0
                    while i+1 < len(player_names_list):
                        self.server.execute(f'tellraw {info.player} [{{"text":"|-  §b{player_names_list[i]}", "extra":[{{"text":" §a[选中]", "clickEvent":{{"action":"suggest_command","value":"!p {player_names_list[i]}"}},"hoverEvent":{{"action":"show_text","value":"点击选择玩家 {player_names_list[i]}"}}}}]}}]') 
                        i += 1
                    self.server.execute(f'tellraw {info.player} [{{"text":"∟-  §b{player_names_list[i]}", "extra":[{{"text":" §a[选中]", "clickEvent":{{"action":"suggest_command","value":"!p {player_names_list[i]}"}},"hoverEvent":{{"action":"show_text","value":"点击选择玩家 {player_names_list[i]}"}}}}]}}]') 
                except Exception as e:
                    self.server.say(f"§c错误: {e}")
                    return
                # server.say(player_names_list)




            else:
                self.server.say("§c当前没有玩家在线")
                
        except Exception as e:
            self.server.say(f"§c错误: {e}")


class ManyPlayer():
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server

    @new_thread("SpawnPlayer")
    def SpawnPlayer(self, info: Info, player_num: int, sleep: int = 0):
        self.server.say('§a正在创建假人，请耐心等待...')
        i = 1
        if sleep <= 0:
            for i in range(player_num):
                self.server.execute(f'execute as {info.player} run execute at @s run player FakePlayer{i} spawn')
                self.server.execute(f'tp FakePlayer{i} {info.player}')
                time.sleep(1)
        elif sleep > 0:
            for i in range(player_num):
                self.server.execute(f'execute as {info.player} run execute at @s run player FakePlayer{i} spawn')
                self.server.execute(f'tp FakePlayer{i} {info.player}')
                time.sleep(sleep)

    @new_thread("ManyPlayer")
    def ManyPlayer(self, info: Info):
        if not info.is_player or not info.content.startswith('!mp'): 
            return
        self.server.execute('carpet commandPlayer 0')
        self.server.execute('carpet setDefault commandPlayer 0')
        args = info.content.split() 
        if len(args) < 2:
            self.server.say('§c语法错误：正确语法：!mp <kill|cmd|slow|spawn>') 
            return
        if args[1] == 'kill':
            i = 0
            for i in range(256):
                self.server.execute(f'kill FakePlayer{i}')
            return
        elif args[1] == 'cmd':
            i = 0
            if args[2] == 'spawn':
                return
            for i in range(256):
                self.server.execute(f'player FakePlayer{i} {' '.join(args[2:])}')
        elif args[1] == 'slow':
            try:
                player_num = int(args[2])
            except ValueError:
                self.server.say('§c玩家数量必须是一个整数！') 
                return
            except IndexError:
                self.server.tell(info.player, '§c语法错误：正确语法：!mp slow <number_of_players>')
                return
            try:
                permission_level = self.server.get_permission_level(info.player)
            except Exception as e:
                self.server.say(f'§c发生错误: {str(e)}')
                return
            if permission_level < 1:
                self.server.tell(info.player, '§c你没有权限使用此指令！') 
            else:
                self.SpawnPlayer(info, player_num, sleep=1) #type: ignore
            return
        elif args[1] == 'spawn':
            try:
                player_num = int(args[2])
            except ValueError:
                self.server.say('§c玩家数量必须是一个整数！') 
                return
            except IndexError:
                self.server.tell(info.player, '§c语法错误：正确语法：!mp slow <number_of_players>')
                return
            try:
                permission_level = self.server.get_permission_level(info.player)
            except Exception as e:
                self.server.say(f'§c发生错误: {str(e)}')
                return
            if permission_level < 1 and player_num > 20:
                self.server.tell(info.player, '§c你没有足够的权限创建超过10个假人！')
            elif permission_level < 2 and player_num > 50:
                self.server.tell(info.player, '§c你没有足够的权限创建超过50个假人！')
            elif player_num <= 256:
                self.SpawnPlayer(info, player_num, sleep=0.1) #type: ignore
                

class BetterChat():
    def __init__(self, server: PluginServerInterface):
        self.server = server
    @new_thread("BetterChat")
    def Chat(self, info: Info):
        if not info.is_player:
            return
        if '@' not in info.content or info.player == 'Server':
            return
        if '@a' in info.content:
            self.server.say(f'- §a玩家 §e{info.player} §a@了所有人')
            self.server.execute('title @a title ""')
            self.server.execute(f'title @a subtitle [{{"text":"{info.player}","color":"aqua"}},{{"text":"@了你","color":"blue"}}]')
            self.server.execute('execute at @a run playsound minecraft:entity.player.levelup master @a')
            return
        elif '@ ' in info.content:
            try:
                words = info.content.split()
                for i, word in enumerate(words):
                    if word == '@' and i + 1 < len(words):
                        target_name = words[i + 1]
                        online_players = self.server.get_plugin_instance('minecraft_data_api').get_server_player_list()
                        if target_name not in online_players.players:
                            self.server.tell(info.player, f'§c玩家 §e{target_name} §c不在线')
                            return
                        self.server.say(f'- §a玩家 §e{info.player} §a@了{target_name}')
                        self.server.execute('title @a title ""')
                        self.server.execute(f'title {target_name} subtitle [{{"text":"{info.player}","color":"aqua"}},{{"text":"@了你","color":"blue"}}]')
                        self.server.execute(f'execute at {target_name} run playsound minecraft:entity.player.levelup master @a')
            except Exception as e:
                self.server.logger.error(f"处理@格式时出错: {e}")
            return


       
class Scale():
    def __init__(self, server: PluginServerInterface):
        self.server = server
    def scale(self, info: Info):
        if not info.is_player or not info.content.startswith('!sc'): 
            return
        args = info.content.split() 
        if len(args) != 2:
            self.server.tell(info.player, '§c语法错误：正确语法：!sc <scale_value>') 
            return
        
        try:
            scale_value = float(args[1])
        except ValueError:
            self.server.tell(info.player, '§c缩放值必须是一个整数！') 
            return
        try:
            self.server.execute(f'attribute {info.player} minecraft:scale base set {scale_value}')
            self.server.tell(info.player, f'§a成功将你的大小设置为 {scale_value}！')
        except Exception as e:
            self.server.tell(info.player, f'§c发生错误: {str(e)}')
#                    :)
