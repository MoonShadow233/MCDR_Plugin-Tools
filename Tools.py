from mcdreforged.api.all import * 
import time
import random
#这些东西并没有什么参考价值
#一堆石山罢了
#如果发现了bug也欢迎在git提交issus
# GPL-3.0 License - Copyright (c) 2024 MoonShadow233


PLUGIN_ID = 'tools'
PLUGIN_NAME = 'Tools'
VERSION = '1.1.3'

def on_load(server: PluginServerInterface, prev_module):
    global IssueUrl
    IssueUrl = "https://github.com/MoonShadow233/MCDR_Plugin-Tools/issues"
    global GithubUrl
    GithubUrl = "https://github.com/MoonShadow233/MCDR_Plugin-Tools"
    global PLUGIN_ENABLED
    conf(server)
    global music_dict
    music_dict = {
        'ceative': 'minecraft:music.creative',
        'credits': 'minecraft:music.credits',
        'end': 'minecraft:music.end',
        'game': 'minecraft:music.game',
        'dragon': 'minecraft:music.dragon',
        'menu': 'minecraft:music.menu',
        'nether': 'minecraft:music.nether',
        '11': 'minecraft:music_disc.11',
        '13': 'minecraft:music_disc.13',
        '5': 'minecraft:music_disc.5',
        'blocks': 'minecraft:music_disc.blocks',
        'cat': 'minecraft:music_disc.cat',
        'chirp': 'minecraft:music_disc.chirp',
        'far': 'minecraft:music_disc.far',
        'mall': 'minecraft:music_disc.mall',
        'creator': 'minecraft:music_disc.creator',
        'creator_music_box': 'minecraft:music_disc.creator_music_box',
        'lava_chicken': 'minecraft:music_disc.lava_chicken',
        'mellohi': 'minecraft:music_disc.mellohi',
        'otherside': 'minecraft:music_disc.otherside',
        'pigstep': 'minecraft:music_disc.pigstep',
        'precipice': 'minecraft:music_disc.precipice',
        'relic': 'minecraft:music_disc.relic',
        'stal': 'minecraft:music_disc.stal',
        'strad': 'minecraft:music_disc.strad',
        'tears': 'minecraft:music_disc.tears',
        'wait': 'minecraft:music_disc.wait',
        'ward': 'minecraft:music_disc.ward'
    }
    
    PLUGIN_ENABLED = settings.get('enable_tools', False)
    if PLUGIN_ENABLED:
        ChatEvent(server, None, type="info", msg=f'§aTools插件{VERSION} by MoonShadow233 加载成功', say=True).guide()
    else:
        ChatEvent(server, None, type="info", msg='====================================================', say=True).guide()
        ChatEvent(server, None, type="info", msg=f'§cTools插件被禁用!版本：{VERSION}', say=True).guide()
        ChatEvent(server, None, type="info", msg=f'§c在{GithubUrl}阅读插件使用说明！', say=True).guide()
        ChatEvent(server, None, type="info", msg='====================================================', say=True).guide()
        return
    server.logger.info(f'{PLUGIN_NAME} 插件 加载成功 版本: {VERSION}')

def conf(server: PluginServerInterface):
    DefauleConf = {
        'settings': {
            'enable_here': True,
            'enable_kill': True,
            'enable_tp': True,
            'enable_restart': True,
            'enable_random': True,
            'enable_fakeplayer': True,
            'enable_manyplayer': True,
            'enable_betterchat': True,
            'enable_scale': True,
            'enable_itemhighlight': True,
            'enable_tools': True,
            'enable_music': True
        },
        'message': {
            'welcome_message': '§c欢迎 §a{player} §c加入游戏！'
        }
    }
    conf.config = server.load_config_simple(
        'config.json',
        DefauleConf
    )
    global settings
    settings = conf.config.get('settings', DefauleConf['settings'])

def on_unload(server: PluginServerInterface):
    ChatEvent(server, None, type="info", msg='插件已卸载', log='插件已卸载', say=False).guide()

def on_info(server: PluginServerInterface, info: Info):
    command(server, info)

def command(server: PluginServerInterface, info: Info):
    global settings
    
    if info.content is None or not settings.get('enable_tools', True):
        return
    
    if settings.get('enable_betterchat', True):
        BetterChat(server).Chat(info)
    
    if not '!' in info.content:
        return
    
    if settings.get('enable_kill', True):
        Kill(server).kill(info)
    
    if settings.get('enable_here', True):
        Here(server, info).HereMain()
    
    if settings.get('enable_tp', True):
        GamemodeTp(server).get_player_info(info)
    
    if settings.get('enable_restart', True):
        Restart(server, info).restart(info)
    
    if settings.get('enable_random', True):
        Random(server).ListNumber(info)
    
    if settings.get('enable_fakeplayer', True):
        FakePlayer(server, info).FakePlayer(info)
    
    if settings.get('enable_manyplayer', True):
        ManyPlayer(server, info).ManyPlayer(info)
    
    if settings.get('enable_scale', True):
        Scale(server).scale(info)
    
    if settings.get('enable_itemhighlight', True):
        ItemHL(server).highlight_item(info)

    if settings.get('enable_music', True):
        Music(server, info).PlayMusic()
    
    ChatEvent(server, info).help()

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
        'enable_itemhighlight': True,
        'enable_tools': False
    }
    message: dict = {
        'welcome_message': '§c欢迎 §a{player} §c加入游戏！'

    }

class Here:
    def __init__(self, server: PluginServerInterface, info:Info):
        self.server = server
        self.info = info
    
    def HereMain(self):
        if self.info.content != '!here' and self.info.content != '!h':
            return
        if not self.info.is_player:
            return
        self.GetPos()
        
    @new_thread("Here")
    def GetPos(self):
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            ChatEvent(self.server, self.info, type="error", msg='§cMinecraft Data API未启用，无法使用此功能！请联系管理员#106', log='Minecraft Data API 未启用', say=False).guide()
            return
        try:
            pos = api.get_player_coordinate(self.info.player)
            dim = api.get_player_dimension(self.info.player)
            x, y, z = pos.x, pos.y, pos.z
        except Exception as e:
            ChatEvent(self.server, self.info, type="error", msg=f'§c获取坐标时发生错误: {str(e)}', log=f'获取坐标错误: {e}', say=False).guide()
            return
        x_n = round(x/8)
        y_n = round(y)
        z_n = round(z/8)
        
        x = round(x)
        y = round(y)
        z = round(z)
        message = f"§a§u{self.info.player} §r在 "
        if dim == 0:
            message += f"[§2主世界:§a{x}  {y}  {z}§r]→ [§c下界:§6{x_n}  {y_n}  {z_n}§r]"
        elif dim == -1:
            message += f"[§c下界:§6{x}  {y}  {z}§r]→ [§2主世界:§a{x_n}  {y_n}  {z_n}§r]"
        elif dim == 1:
            message += f"[§5末地:§e{x}  {y}  {z}§r]"
        else:
            message += f"[§4未知维度:§c{x}  {y}  {z}§r]"
        x_n = x/8
        ChatEvent(self.server, None, type="info", msg=message, log=f"[HerePlugin] {message}", say=True).guide()
        self.server.execute(f'tellraw @a [{{text:"[",color:dark_gray}},{{text:"Tools",color:dark_green}},{{text:"] ",color:dark_gray}},{{text:"[旁观TP坐标]",color:gold,click_event:{{action:suggest_command,command:"!tp {x} {y} {z}"}},hover_event:{{action:show_text,value:{{text:"Tools插件的TP功能"}}}}}},{{text:"   "}},{{bold:true,text:"[+H]",click_event:{{action:run_command,command:"/highlight {x} {y} {z}"}},hover_event:{{action:show_text,value:{{text:"使用Carpet Org的高亮功能"}}}},color:yellow}},{{text:"   "}},{{text:"[+C]",color:yellow,bold:true,hover_event:{{action:show_text,value:{{text:"复制坐标"}}}},click_event:{{action:copy_to_clipboard,value:"{x} {y} {z}"}}}}]')

class Kill:
    def __init__(self, server:PluginServerInterface):
        self.server = server
        pass
    def kill(self, info: Info):
        if info.is_player and info.content.strip().lower() == '!kill': 
            player_name = info.player  
            self.server.execute(f'kill {player_name}')
            ChatEvent(self.server, info, type="info", msg=f'欸 {player_name} 你怎么似了啊？！', log=f"玩家 {player_name} 自杀", say=True).guide()

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
        if not info.is_player or not info.content.startswith('!tp'):
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
        ChatEvent(self.server, info, type="info", msg=(
            '§c语法错误！正确语法：!tp <x> [<y>] <z>|!tp [<玩家>|<维度>]|!tp help\n'
            '§c如果你想传送到某个坐标，请使用!tp <x> [<y>] <z>，其中y是可选的，默认为64。\n'
            '§c如果你想传送到某个玩家，请使用!tp <玩家>。\n'
            '§c如果你想传送到某个维度，请使用!tp <维度> 注意：维度只能有 主世界 下界/地狱/下届 末地 三种选择\n'
            '§c注意：!tp <维度>是单独的指令，不能和其他参数一起使用！'
        ), log=None, say=False).guide()

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
            ChatEvent(self.server, info, type="info", msg=f"由{info.player}执行的重启！", log=f"重启: {info.player}", say=True).guide()
            i = 10
            while i >= 0:
                ChatEvent(self.server, info, type="info", msg=f"服务器将在{i}秒后重启！", log=f"重启倒计时: {i}", say=True).guide()
                i -= 1
                time.sleep(1)

            self.server.restart()
        else:
            ChatEvent(self.server, info, type="error", msg="§c你没有权限重启服务器！", log="没有权限重启", say=False).guide()

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
                ChatEvent(self.server, info, type="info", msg=f'§a[骰子] §r- §b生成的数为: §e{num}', log=f"骰子: {num}", say=True).guide()

                return
            range_str = parts[1] 
            # self.server.say(range_str)
            range1 = int(range_str.split('-')[0])
            range2 = int(range_str.split('-')[1])
            if range1 > range2:
                ChatEvent(self.server, info, type="error", msg='§c[骰子] §r- §c范围错误：前一个数必须小于后一个数！', log='骰子 范围错误', say=False).guide()
                return
            elif range1 == range2:
                ChatEvent(self.server, info, type="error", msg='§c[骰子] §r- §c范围错误：两个数不能相等！', log='骰子 范围错误', say=False).guide()
                return
            
            num = random.randint(range1,range2)
            ChatEvent(self.server, info, type="info", msg=f'§a[骰子] §r- §b生成的数为: §e{num}', log=f"骰子: {num}", say=True).guide()
        except Exception as e:
            ChatEvent(self.server, info, type="error", msg=f'§c[骰子] §r- §c发生错误: {str(e)}', log=f"骰子错误: {e}", say=False).guide()

class FakePlayer():
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server
        self.info = info

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
                    ChatEvent(self.server, info, type="error", msg='§c语法错误！正确语法：!p !move <玩家>', log='!p 语法错误', say=False).guide()
                    return
                Splayer = args[2]
                self.MovePlayer(info, Splayer) 
                
            elif target_player == '!b':
                if len(args) < 3:
                    ChatEvent(self.server, info, type="error", msg='§c语法错误！正确语法：!p !b <玩家>', log='!p 语法错误', say=False).guide()
                    return
                Splayer = args[2]
                self.PlayerInventory(info, Splayer) 
            elif target_player == '!t':
                if len(args) < 3:
                    ChatEvent(self.server, info, type="error", msg='§c语法错误！正确语法：!p !t <玩家>', log='!p 语法错误', say=False).guide()
                    return
                Splayer = args[2]
                self.TurnPlayer(info, Splayer) 
            else:
                
                self.server.execute(f'tellraw {info.player} [{{"text":"§b玩家控制 - §a{target_player}"}}]') 
                self.FPlayerC(info, target_player) 


            return
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            ChatEvent(self.server, info, type="error", msg='§cMinecraft Data API未启用，无法使用此功能！请联系管理员#106', log='Minecraft Data API 未启用', say=False).guide()
            return
        try:
            playerlist = api.get_server_player_list()
            
            if playerlist.amount > 0:
                player_names_list = playerlist.players
                ChatEvent(self.server, info, type="info", msg=f"§a在线: §6{playerlist.amount}§a/§6{playerlist.limit}§a", log="玩家列表", say=True).guide()
                try:
                    i = 0
                    while i+1 < len(player_names_list):
                        self.server.execute(f'tellraw {info.player} [{{"text":"|-  §b{player_names_list[i]}", "extra":[{{"text":" §a[选中]", "clickEvent":{{"action":"suggest_command","value":"!p {player_names_list[i]}"}},"hoverEvent":{{"action":"show_text","value":"点击选择玩家 {player_names_list[i]}"}}}}]}}]')
                        i += 1
                    self.server.execute(f'tellraw {info.player} [{{"text":"∟-  §b{player_names_list[i]}", "extra":[{{"text":" §a[选中]", "clickEvent":{{"action":"suggest_command","value":"!p {player_names_list[i]}"}},"hoverEvent":{{"action":"show_text","value":"点击选择玩家 {player_names_list[i]}"}}}}]}}]') 
                except Exception as e:
                    ChatEvent(self.server, None, type="error", msg=f"§c错误: {e}", log=f"获取玩家列表错误: {e}", say=False).guide()
                    return
                # server.say(player_names_list)




            else:
                ChatEvent(self.server, None, type="info", msg="§c当前没有玩家在线", log="玩家列表 空", say=True).guide()
                
        except Exception as e:
            ChatEvent(self.server, None, type="error", msg=f"§c错误: {e}", log=f"获取玩家列表异常: {e}", say=False).guide()

class ManyPlayer():
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server
        self.info = info

    @new_thread("SpawnPlayer")
    #/player 1 spawn at ~ ~ ~ facing ~ ~ in minecraft:overworld
    #!mp spawn 10 x y z a b dim
    def SpawnPlayer(self, info: Info, player_num: int, sleep: int = 0, x: str = '~', y: str = '~', z: str = '~', a='~', b='~', dim=None):
        i = 1
        try:
            if dim == "o":
                dim1 = "minecraft:overworld"
            elif dim == "n":
                dim1 = "minecraft:the_nether"
            elif dim == "e":
                dim1 = "minecraft:the_end"
            if sleep <= 0:
                if x == "~" and y == "~" and z == "~":
                    for i in range(player_num):
                        self.server.execute(f'execute as {info.player} run execute at @s run player FakePlayer{i} spawn at {x} {y} {z} facing {a} {b}')
                    time.sleep(1)
                elif x != "~" and y != "~" and z != "~" and dim is not None:
                    for i in range(player_num):
                        self.server.execute(f'execute as {info.player} run execute at @s run player FakePlayer{i} spawn at {x} {y} {z} facing {a} {b} in {dim1}')
                        time.sleep(1)
            elif sleep > 0:
                if x == "~" and y == "~" and z == "~":
                    for i in range(player_num):
                        self.server.execute(f'execute as {info.player} run execute at @s run player FakePlayer{i} spawn at {x} {y} {z} facing {a} {b}')
                    time.sleep(sleep)
                elif x != "~" and y != "~" and z != "~" and not dim is None:
                    for i in range(player_num):
                        self.server.execute(f'execute as {info.player} run execute at @s run player FakePlayer{i} spawn at {x} {y} {z} facing {a} {b} in {dim1}')
                        time.sleep(sleep)
        except Exception as e:
            ChatEvent(self.server, info, type="error", msg=f'§c生成假人时发生错误: {str(e)}', log=f'生成假人错误: {e}', say=False).guide()
            return

            

    @new_thread("ManyPlayer")
    def ManyPlayer(self, info: Info):
        if not info.is_player or not info.content.startswith('!mp'): 
            return
        args = info.content.split() 
        x = '~'
        y = '~'
        z = '~'
        a = '~'
        b = '~'
        dim = None
        if len(args) < 2:
            ChatEvent(self.server, info, type="error", msg='§c语法错误：正确语法输入!tools', log='!mp 语法错误', say=False).guide()
            return
        
        elif len(args) >= 8:
            x = args[3]
            y = args[4]
            z = args[5]
            a = args[6]
            b = args[7]
            dim = args[8]
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
                ChatEvent(self.server, info, type="error", msg='§c玩家数量必须是一个整数！', log='!mp 参数错误', say=False).guide()
                return
            except IndexError:
                ChatEvent(self.server, info, type="error", msg='§c语法错误：正确语法查看!tools', log='!mp 参数不足', say=False).guide()
                return
            try:
                permission_level = self.server.get_permission_level(info.player)
            except Exception as e:
                ChatEvent(self.server, None, type="error", msg=f'§c发生错误: {str(e)}', log=f'权限检查错误: {e}', say=False).guide()
                return
            if permission_level < 1:
                ChatEvent(self.server, info, type="error", msg='§c你没有权限使用此指令！', log='权限不足', say=False).guide()
            else:
                self.SpawnPlayer(info, player_num, sleep=1) #type: ignore
            return
        elif args[1] == 'spawn':
            try:
                player_num = int(args[2])
            except ValueError:
                ChatEvent(self.server, info, type="error", msg='§c玩家数量必须是一个整数！', log='!mp 参数错误', say=False).guide()
                return
            except IndexError:
                ChatEvent(self.server, info, type="error", msg='§c语法错误：正确语法：!mp slow <number_of_players>', log='!mp 参数不足', say=False).guide()
                return
            try:
                permission_level = self.server.get_permission_level(info.player)
            except Exception as e:
                ChatEvent(self.server, None, type="error", msg=f'§c发生错误: {str(e)}', log=f'权限检查错误: {e}', say=False).guide()
                return
            if permission_level < 1 and player_num > 20:
                ChatEvent(self.server, info, type="error", msg='§c你没有足够的权限创建超过10个假人！', log='权限不足', say=False).guide()
            elif permission_level < 2 and player_num > 50:
                ChatEvent(self.server, info, type="error", msg='§c你没有足够的权限创建超过50个假人！', log='权限不足', say=False).guide()
            elif player_num <= 256:
                self.SpawnPlayer(info, player_num, x=x,y=y,z=z, dim=dim,a=a,b=b,sleep=0.1) #type: ignore
                
class BetterChat():
    def __init__(self, server: PluginServerInterface):
        self.server = server
    @new_thread("BetterChat")
    def Chat(self, info: Info):
        if not info.is_player:
            return
        if '@' not in info.content or info.player == 'Server':
            return
        elif '@ ' in info.content:
            try:
                words = info.content.split()
                for i, word in enumerate(words):
                    if word == '@' and i + 1 < len(words):
                        target_name = words[i + 1]
                        if target_name.lower() == 'a':
                            ChatEvent(self.server, info, type="info", msg=f'- §a玩家 §e{info.player} §a@了所有人', log=f"@a by {info.player}", say=False).guide()
                            self.server.execute('title @a title ""')
                            self.server.execute(f'title @a subtitle [{{"text":"{info.player}","color":"aqua"}},{{"text":"@了你","color":"blue"}}]')
                            self.server.execute('execute at @a run playsound minecraft:entity.player.levelup master @a')
                            return
                        online_players = self.server.get_plugin_instance('minecraft_data_api').get_server_player_list()
                        if target_name not in online_players.players:
                            ChatEvent(self.server, info, type="error", msg=f'§c玩家 §e{target_name} §c不在线', log=f"玩家不在线: {target_name}", say=False).guide()
                            return
                        ChatEvent(self.server, info, type="info", msg=f'- §a玩家 §e{info.player} §a@了{target_name}', log=f"@ {target_name} by {info.player}", say=False).guide()
                        self.server.execute('title @a title ""')
                        self.server.execute(f'title {target_name} subtitle [{{"text":"{info.player}","color":"aqua"}},{{"text":"@了你","color":"blue"}}]')
                        self.server.execute(f'execute at {target_name} run playsound minecraft:entity.player.levelup master @a')
            except Exception as e:
                ChatEvent(self.server, info, type="error", msg=f"§c发生错误: {str(e)}", say=False).guide()
            return
       
class Scale():
    def __init__(self, server: PluginServerInterface):
        self.server = server
    def scale(self, info: Info):
        if not info.is_player or not info.content.startswith('!sc'): 
            return
        args = info.content.split() 
        if len(args) != 2:
            ChatEvent(self.server, info, type="info", msg="§c语法错误：正确语法查看!tools", log="sc 语法错误", say=False).guide()
            return
        
        try:
            scale_value = float(args[1])
        except ValueError:
            ChatEvent(self.server, info, type="info", msg="§c缩放值必须是一个数字！", log="sc 参数非数字", say=False).guide()
            return
        try:
            self.server.execute(f'attribute {info.player} minecraft:scale base set {scale_value}')
            ChatEvent(self.server, info, type="info", msg=f"§a成功将你的大小设置为 {scale_value}！", log=f"设置缩放: {scale_value}", say=False).guide()
        except Exception as e:
            ChatEvent(self.server, info, type="error", msg=f"§c发生错误: {str(e)}", say=False).guide()

class ItemHL():
    def __init__(self, server: PluginServerInterface):
        self.server = server
    @new_thread("ItemHighlight")
    def highlight_item(self, info: Info):
        if not info.is_player or (not info.content == '!itemhl' and not info.content == '!uitemhl'): 
            return
        if info.content == '!uitemhl':
            self.server.execute('execute as @e[type=item] run data merge entity @s {Glowing:0b}')
            ChatEvent(self.server, info, type="info", msg='§a所有掉落物高亮已取消，输入!itemhl开启', log='取消物品高亮', say=False).guide()
            return
        elif info.content == '!itemhl':
            self.server.execute('execute as @e[type=item] run data merge entity @s {Glowing:1b}')
            ChatEvent(self.server, info, type="info", msg='§a所有掉落物已高亮，输入!uitemhl取消', log='开启物品高亮', say=False).guide()

class Music():
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server
        self.info = info
    def help(self):
        helpmsg = "§e[Help] §r- "
        helpmsg += "§bMusic Plugin 帮助信息§r\n"
        helpmsg += "├┬─ §c!music p id <music_id> §r- 为所有玩家播放指定id的声音\n"
        helpmsg += "│├─ §c!music p name <music_name> §r- 为所有玩家播放指定唱片名称的音乐\n"
        helpmsg += "│└─ §c!music p stop §r- 停止所有玩家播放的音乐\n"
        helpmsg += "├─ §c!music §r- 显示帮助信息\n"
        helpmsg += "└─ §c!music stop §r- 停止当前播放的音乐"
        ChatEvent(self.server, self.info, type="info", msg=helpmsg, log=None, say=False).guide()
        ChatEvent(self.server, self.info, type="help", msg=None, log=None, say=False).guide()


    def PlayMusic(self):
        if not self.info.is_player or not self.info.content.startswith('!music'):
            return
        args = self.info.content.split()
        if len(args) < 2:
            self.help()
            return
        mode = args[1]
        if mode == 'p':
            if len(args) < 3:
                self.help()
                return
            if args[2] == 'name':
                music_name = args[3]
                try:
                    music_name_id = music_dict[music_name]
                except KeyError:
                    ChatEvent(self.server, self.info, type="error", msg=f"§c未找到名为 {music_name} 的音乐！音乐列表：{list(music_dict.keys())}", log=f"未找到名为 {music_name} 的音乐", say=False).guide()
                    return
                self.server.execute(f'execute at @a run playsound {music_name_id} player @a')
            elif args[2] == 'id':
                music_id = args[3]
                self.server.execute(f'execute at @a run playsound {music_id} player @a')
            elif args[2] == 'stop':
                self.server.execute('stopsound @a')
            else:
                self.help()
                return
        elif args[1] == 'stop':
            self.server.execute(f'stopsound {self.info.player}')
        else:
            self.help()
            return


class ChatEvent():
    def __init__(self, server: PluginServerInterface, 
                 info: Info = None, 
                 type: str = None, 
                 log: str = None, 
                 msg: str = None, 
                 say: bool = False):


# - type: <info|error|warn|help>
# - log: 需要发送到服务器控制台的日志信息
# - msg: 需要发送给玩家的消息
# - say: 是否使用say命令发送消息而不是tell命令

        self.server = server
        self.info = info

        self.SendMsg = "§8[§2Tools§8] §r"
        self.SendLog = "§8[§2Tools§8] §r"

        self.log = log
        self.msg = msg
        self.say = say
        self.type = type

    def pack(self):
        if not self.msg is None:
            self.SendMsg += self.msg
        else:
            self.SendMsg = None
        if not self.log is None:
            self.SendLog += self.log
        else:
            self.SendLog = None
        self.send(send_msg=self.SendMsg, send_log=self.SendLog, say=self.say)

    def guide(self):
        if self.help == "help":
            self.help()
            return
        if self.msg is None and self.log is None:
            return
        if self.type == "error":
            self.SendMsg += "§c§l[ERROR] §r"
            self.SendLog += "§c§l[ERROR]§r"
            self.pack()
        elif self.type == "warn":
            self.SendMsg += "§6§l[WARN] §r"
            self.SendLog += "§6§l[WARN] §r"
            self.pack()
        elif self.type == "info":
            self.pack()
        else:
            self.SendMsg = "§a[Tools] §c[ERROR] §r在尝试处理消息文本时出错-->没有找到匹配的消息类型\n位置：Tools.py\n->ChatEvent\n->guide->\nif self.type……else:"

    def send(self, send_msg: str, send_log: str, say: bool = False):
    # 经过guide、pack导航并处理完成SendMsg后的消息处理
        if not self.SendMsg is None:
            if say:
                self.server.say(send_msg)
                return
            else:
                self.server.tell(self.info.player, send_msg)
                return
        if not self.SendLog is None:
            self.server.logger(send_log)

        

        

    def help(self):
        if not self.info or not getattr(self.info, "is_player", False) or self.info.content != '!tools':
            return
        self.SendLog += f"§r[info] - 向{self.info.player}显示帮助信息"

        self.SendMsg += "§e[Help] §r- "
        self.SendMsg += "§bToolsPlugin 帮助信息§r\n"
        self.SendMsg += "├─ §c!here | !h §r- 获取你当前所在位置的坐标和维度\n"
        self.SendMsg += "├─ §c!kill §r- 自杀指令\n"
        self.SendMsg += "├─ §c!tp <x> [<y>] <z> | !tp [<玩家>|<维度>] §r- 旁观模式传送指令\n"
        self.SendMsg += "├─ §c!!restart §r- 重启服务器指令（需要权限）\n"
        self.SendMsg += "├─ §c!l <range1>-<range2> §r- 在指定范围内生成一个随机数，大小无限制;r1 < r2\n"
        self.SendMsg += "├─┬§c!mp <kill|cmd|slow|spawn> <count> [<pos>] [<dim:o|n|e>] §r- 假人管理指令\n"
        self.SendMsg += "│    └─ §c![mp <spawn> <count> <x> <y> <z> <facing:x'> <facing:y'> <dim:o|n|e>] §r- 在指定维度、位置生成指定朝向假人,绝对坐标 \n"
        self.SendMsg += "├─ §c!p <玩家>|!p !move <玩家>|!p !b <玩家>|!p !t <玩家> §r- 假人控制指令(已弃用)\n"
        self.SendMsg += "├─ §c!sc <scale_value> §r- 设置玩家大小指令\n"
        self.SendMsg += "├─ §c!itemhl §r- 高亮所有掉落物指令，!uitemhl 取消高亮\n"
        self.SendMsg += "├─ §c@a|@{PLAYERNAME} §r- @玩家\n"
        self.SendMsg += "├┬─ §c!music p id <music_id> §r- 为所有玩家播放指定id的声音\n"
        self.SendMsg += "│├─ §c!music p name <music_name> §r- 为所有玩家播放指定唱片名称的音乐\n"
        self.SendMsg += "│└─ §c!music p stop §r- 停止所有玩家播放的音乐\n"
        self.SendMsg += "├─ §c!music §r- 显示帮助信息\n"
        self.SendMsg += "└─ §c!music stop §r- 停止当前播放的音乐"
        self.send(send_msg=self.SendMsg, send_log=self.SendLog, say=False)