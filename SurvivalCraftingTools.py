from mcdreforged.api.all import *
import time
import random
# Tools.py - MCDReforged 插件，提供多种服务器管理功能
# Copyright (C) 2024 MoonShadow233, Fashiye_xico
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 本文件包含来自 PrimeBackup 的修改代码，
# 原作者 TISUnion，遵循 LGPL-3.0 协议。
# 原项目地址：https://github.com/TISUnion/PrimeBackup


# 如果发现了bug欢迎在git提交issues

PLUGIN_ID = 'tools'
PLUGIN_NAME = 'Tools'
VERSION = '1.2.0'
IS_MCDR_COMMAND_FABRIC = False

def on_load(server: PluginServerInterface, prev_module):
    global IssueUrl, GithubUrl, PLUGIN_ENABLED, settings, music_dict, config
    
    IssueUrl = "https://github.com/MoonShadow233/MCDR_Plugin-Tools/issues"
    GithubUrl = "https://github.com/MoonShadow233/MCDR_Plugin-Tools"
    
    conf(server)
    
    music_dict = {
        'creative': 'minecraft:music.creative',
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
        register_tools_commands(server)
    else:
        ChatEvent(server, None, type="info", msg='====================================================', say=True).guide()
        ChatEvent(server, None, type="info", msg=f'§cTools插件被禁用!版本：{VERSION}', say=True).guide()
        ChatEvent(server, None, type="info", msg=f'§c在{GithubUrl}阅读插件使用说明！', say=True).guide()
        ChatEvent(server, None, type="info", msg='====================================================', say=True).guide()
        return
    server.logger.info(f'{PLUGIN_NAME} 插件 加载成功 版本: {VERSION}')

def on_unload(server: PluginServerInterface):
    ChatEvent(server, None, type="info", msg='插件已卸载', log='插件已卸载', say=False).guide()

def on_info(server: PluginServerInterface, info: Info):
    # 只处理非命令功能
    global settings
    
    if info.content is None or not settings.get('enable_tools', True):
        return
    
    # BetterChat
    if settings.get('enable_betterchat', True):
        BetterChat(server).process_chat(info)

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
        'enable_tools': True,  # 默认改为True
        'enable_position': True,
        'enable_music': True,
        "max_position": 100,
        "position_permission_level": 2
    }
    message: dict = {
        'welcome_message': '§c欢迎 §a{player} §c加入游戏！'

    }
    Position: dict = {
        "name": {
            "location": "0 64 0",
            "dimension": "0",
            "by": "player"
        }
    }

def conf(server: PluginServerInterface):
    global config, settings
    config = server.load_config_simple(
        'config.json',
        target_class=Config
    )
    settings = config.settings

class Here:
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server
        self.info = info
    
    @new_thread("Here")
    def GetPos(self):
        if not self.info.is_player:
            return
            
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
        
        x = round(x)
        y = round(y)
        z = round(z)
        
        message = f"§a§u{self.info.player} §r在 "
        if dim == 0:
            message += f"[§2主世界:§a{x}  {y}  {z}§r]→ [§c下界:§6{round(x/8)}  {y}  {round(z/8)}§r]"
        elif dim == -1:
            message += f"[§c下界:§6{x}  {y}  {z}§r]→ [§2主世界:§a{x*8}  {y}  {z*8}§r]"
        elif dim == 1:
            message += f"[§5末地:§e{x}  {y}  {z}§r]"
        else:
            message += f"[§4未知维度:§c{x}  {y}  {z}§r]"
            
        ChatEvent(self.server, None, type="info", msg=message, log=f"[HerePlugin] {message}", say=True).guide()
        
        tellraw_cmd = f'tellraw @a [{{"text":"[",color:dark_gray}},{{"text":"Tools",color:dark_green}},{{"text":"] ",color:dark_gray}},{{"text":"[旁观TP坐标]",color:gold,click_event:{{action:suggest_command,command:"!tp {x} {y} {z}"}},hover_event:{{action:show_text,value:{{text:"Tools插件的TP功能"}}}}}},{{"text":"   "}},{{"bold":true,"text":"[+H]",click_event:{{action:run_command,command:"/highlight {x} {y} {z}"}},hover_event:{{action:show_text,value:{{text:"使用Carpet Org的高亮功能"}}}},color:yellow}},{{"text":"   "}},{{"text":"[+C]",color:yellow,bold:true,hover_event:{{action:show_text,value:{{text:"复制坐标"}}}},click_event:{{action:copy_to_clipboard,value:"{x} {y} {z}"}}}}]'
        self.server.execute(tellraw_cmd)

class Kill:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def kill(self, info: Info):
        if info.is_player:
            player_name = info.player
            self.server.execute(f'kill {player_name}')
            ChatEvent(self.server, info, type="info", msg=f'欸 {player_name} 你怎么似了啊？！', log=f"玩家 {player_name} 自杀", say=True).guide()

class Position:
    """
    传送位置管理类
    提供保存、传送、删除和查看传送点的功能
    """
    
    def __init__(self, server: PluginServerInterface):
        """
        初始化 Position 类
        
        :param server: PluginServerInterface 实例
        """
        self.server = server
    
    def _load_config(self):
        """
        加载配置文件
        
        :return: 配置数据字典
        """
        return self.server.load_config_simple('config.json')
    
    def _save_config(self, config_data):
        """
        保存配置文件
        
        :param config_data: 要保存的配置数据
        """
        self.server.save_config_simple(config_data, 'config.json')
    
    def getpositionlist(self, info: Info, page: int = 1, per_page: int = 5):
        """
        获取所有保存的位置列表
        支持点击翻页和操作按钮
        
        :param info: Info 对象
        :param page: 当前页码
        :param per_page: 每页显示数量
        """
        config_data = self._load_config()
        positions = config_data.get('Position', {})
        
        if not positions:
            ChatEvent(self.server, info, type="info", 
                     msg='§c没有保存的传送位置！', 
                     log='没有保存的传送位置', 
                     say=True).guide()
            return
        
        items = list(positions.items())
        total_count = len(items)
        max_page = max(1, (total_count - 1) // per_page + 1)
        
        if not (1 <= page <= max_page):
            out_of_range_msg = RText(f'页码 {page} 超出范围 (1-{max_page})', RColor.gray).set_styles(RStyle.italic)
            self.server.tell(info.player, out_of_range_msg)
            page = max(1, min(page, max_page))
        
        title = RTextList(
            RText('========== ', RColor.gray),
            RText('传送位置列表', RColor.gold),
            RText(' ==========', RColor.gray)
        )
        self.server.tell(info.player, title)
        
        count_text = RTextList(
            RText('共有 ', RColor.gray),
            RText(str(total_count), RColor.yellow),
            RText(' 个位置', RColor.gray)
        )
        self.server.tell(info.player, count_text)
        
        start = (page - 1) * per_page
        end = start + per_page
        page_items = items[start:end]
        
        for name, data in page_items:
            location = data.get('location', '?')
            dimension = data.get('dimension', '?')
            by = data.get('by', '?')
            dim_text = self._dimension_to_text(dimension)
            
            name_text = RText(name, RColor.gold).h(f'位置名称: {name}')
            
            tp_button = RText('[传送]', RColor.green)
            tp_button.h(f'点击传送到 {name}')
            tp_button.c(RAction.run_command, f'!d tp "{name}"')
            
            del_button = RText('[删除]', RColor.red)
            del_button.h(f'点击删除 {name}')
            del_button.c(RAction.suggest_command, f'!d del "{name}"')
            
            item_line = RTextList(
                name_text,
                RText(' - ', RColor.gray),
                RText(f'[{location}]', RColor.aqua),
                RText(' - ', RColor.gray),
                RText(dim_text, RColor.light_purple),
                RText(' - ', RColor.gray),
                RText(f'by {by}', RColor.yellow),
                RText(' ', RColor.gray),
                tp_button,
                RText(' ', RColor.gray),
                del_button
            )
            self.server.tell(info.player, item_line)
        
        prev_btn = RText('<-')
        if 1 <= page - 1 <= max_page:
            prev_btn.h('上一页').c(RAction.run_command, self.__make_pos_list_command(page - 1, per_page))
        else:
            prev_btn.set_color(RColor.dark_gray)
        
        next_btn = RText('->')
        if 1 <= page + 1 <= max_page:
            next_btn.h('下一页').c(RAction.run_command, self.__make_pos_list_command(page + 1, per_page))
        else:
            next_btn.set_color(RColor.dark_gray)
        
        nav_line = RTextList(
            RText('---- ', RColor.gray),
            prev_btn,
            RText(' [', RColor.gray),
            RText(str(page), RColor.yellow),
            RText('/', RColor.gray),
            RText(str(max_page), RColor.yellow),
            RText('] ', RColor.gray),
            next_btn,
            RText(' ----', RColor.gray)
        )
        self.server.tell(info.player, nav_line)
    
    def __make_pos_list_command(self, page: int, per_page: int) -> str:
        """
        生成翻页命令字符串
        
        :param page: 目标页码
        :param per_page: 每页数量
        :return: 完整的命令字符串
        """
        return f'!d list {page}'
    
    def posdebug(self, info: Info):
        """
        显示帮助信息
        当用户输入命令格式错误时调用
        
        :param info: Info 对象
        """
        ChatEvent(self.server, info, type="info", msg=(
            '§c语法错误！正确语法：!d tp <位置名称> | !d set <位置名称> | !d list\n'
            '§c- !d set <名称> : 保存当前位置\n'
            '§c- !d tp <名称> : 传送到保存的位置\n'
            '§c- !d list : 查看所有保存的位置\n'
            '§c- !d del <名称> : 删除保存的位置'
        ), log=None, say=False).guide()
    
    def set_position(self, info: Info):
        """
        设置/传送位置主方法
        根据命令参数分发到不同的子方法
        
        :param info: Info 对象
        """
        if not info.is_player or not info.content.startswith('!d'):
            return
        
        args = info.content.split()
        if len(args) < 2:
            self.posdebug(info)
            return
        
        mode = args[1]
        
        if mode == 'tp':
            self._teleport_to_position(info, args)
        elif mode == 'set':
            self.set_location(info)
        elif mode == 'list':
            page = 1
            if len(args) >= 3:
                try:
                    page = int(args[2])
                except ValueError:
                    pass
            self.getpositionlist(info, page)
        elif mode == 'del':
            if len(args) >= 3:
                self.delete_position(info, args[2])
            else:
                self.posdebug(info)
        else:
            self.posdebug(info)
    
    def _teleport_to_position(self, info: Info, args: list):
        """
        传送到保存的位置
        
        :param info: Info 对象
        :param args: 命令参数列表
        """
        if len(args) < 3:
            self.posdebug(info)
            return
        
        location_name = args[2]
        
        try:
            config_data = self._load_config()
            position_data = config_data.get('Position', {}).get(location_name, {})
            
            if not position_data:
                ChatEvent(self.server, info, type="error", 
                         msg=f'§c未找到位置 "{location_name}"！', 
                         log=f'未找到传送位置: {location_name}', 
                         say=True).guide()
                return
            
            pos_str = position_data.get('location')
            dimension_id = position_data.get('dimension')
            
            if not pos_str or dimension_id is None:
                ChatEvent(self.server, info, type="error", 
                         msg='§c位置数据损坏！', 
                         log='位置数据损坏', 
                         say=True).guide()
                return
            
            # 维度转换
            dimension = self._dimension_to_command(dimension_id)
            
            # 执行传送
            self.server.execute(f'execute in {dimension} run tp {info.player} {pos_str}')
            
            dim_text = self._dimension_to_text(dimension_id)
            ChatEvent(self.server, info, type="info", 
                     msg=f'§a已将你传送到 §6{location_name} §a({dim_text})', 
                     log=f"玩家 {info.player} 传送到 {location_name}", 
                     say=True).guide()
            
        except Exception as e:
            ChatEvent(self.server, info, type="error", 
                     msg=f'§c传送时发生错误: {str(e)}', 
                     log=f'传送错误: {e}', 
                     say=True).guide()
    
    @new_thread("SetPosition")
    def set_location(self, info: Info):
        """
        保存当前位置
        获取玩家当前坐标和维度，保存到配置文件
        
        :param info: Info 对象
        """
        args = info.content.split()
        if len(args) < 3:
            self.posdebug(info)
            return
        
        name = args[2]
        
        # 检查名称是否已存在
        config_data = self._load_config()
        if name in config_data.get('Position', {}):
            ChatEvent(self.server, info, type="error", 
                     msg=f'§c位置 "{name}" 已存在！请使用其他名称', 
                     log=f'位置名称已存在: {name}', 
                     say=True).guide()
            return
        
        # 获取坐标
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            ChatEvent(self.server, info, type="error", 
                     msg='§cMinecraft Data API未启用！', 
                     log='Minecraft Data API 未启用', 
                     say=False).guide()
            return
        
        try:
            # 获取玩家维度和坐标
            dimension = api.get_player_dimension(info.player)
            location = api.get_player_coordinate(info.player)
            
            # 四舍五入坐标
            x = round(location.x)
            y = round(location.y)
            z = round(location.z)
            pos_str = f"{x} {y} {z}"
            
            # 保存到配置
            config_data.setdefault('Position', {})
            config_data['Position'][name] = {
                'location': pos_str,
                'dimension': dimension,
                'by': info.player,
                'time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self._save_config(config_data)
            
            dim_text = self._dimension_to_text(dimension)
            ChatEvent(self.server, info, type="info", 
                     msg=f'§a已保存位置 §6{name} §a: §e{x} {y} {z} §a在 §d{dim_text}', 
                     log=f"玩家 {info.player} 保存位置 {name} [{x} {y} {z}]", 
                     say=True).guide()
            
        except Exception as e:
            ChatEvent(self.server, info, type="error", 
                     msg=f'§c保存位置时发生错误: {str(e)}', 
                     log=f'保存位置错误: {e}', 
                     say=False).guide()
    
    def _dimension_to_text(self, dimension_id):
        """
        维度ID转显示文本
        
        :param dimension_id: 维度ID (0=主世界, -1=下界, 1=末地)
        :return: 维度中文名称
        """
        dimension_map = {
            0: '主世界',
            -1: '下界',
            1: '末地',
            '0': '主世界',
            '-1': '下界',
            '1': '末地'
        }
        return dimension_map.get(dimension_id, f'未知({dimension_id})')
    
    def _dimension_to_command(self, dimension_id):
        """
        维度ID转命令维度名
        用于 execute in <dimension> 命令
        
        :param dimension_id: 维度ID
        :return: Minecraft 命令使用的维度名称
        """
        dimension_map = {
            0: 'minecraft:overworld',
            -1: 'minecraft:the_nether',
            1: 'minecraft:the_end',
            '0': 'minecraft:overworld',
            '-1': 'minecraft:the_nether',
            '1': 'minecraft:the_end'
        }
        return dimension_map.get(dimension_id, 'minecraft:overworld')
    
    def delete_position(self, info: Info, name: str):
        """
        删除保存的位置
        需要权限等级 >= 3
        
        :param info: Info 对象
        :param name: 要删除的位置名称
        """
        perm = self.server.get_permission_level(info.player)
        if perm < 3:
            ChatEvent(self.server, info, type="error", 
                     msg='§c你没有权限删除位置！', 
                     log='权限不足', 
                     say=False).guide()
            return
        
        config_data = self._load_config()
        if name in config_data.get('Position', {}):
            del config_data['Position'][name]
            self._save_config(config_data)
            ChatEvent(self.server, info, type="info", 
                     msg=f'§a已删除位置 §6{name}', 
                     log=f"玩家 {info.player} 删除位置 {name}", 
                     say=True).guide()
        else:
            ChatEvent(self.server, info, type="error", 
                     msg=f'§c未找到位置 "{name}"！', 
                     log=f'删除失败，位置不存在: {name}', 
                     say=True).guide()

class GamemodeTp():
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
        if self.Authentication(info):
            return True
            
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            return False
            
        try:
            gamemode = str(api.get_player_info(info.player, 'playerGameType'))
            if gamemode != '3':
                self.server.tell(info.player, '§c你不是旁观模式，无法使用此指令！请切换到旁观模式后再试。')
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
        coords = self.parse_coordinates(x, y, z, info.player)
        
        if coords is None:
            self.tpdebug(info)
            return
        
        self.execute_teleport(info.player, *coords)
    
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
            player_pos = api.get_player_coordinate(info.player)
            
            x = args[1]
            y = player_pos.y
            z = args[2]
            
            coords = self.parse_coordinates(x, y, z, info.player)
            
            if coords is None:
                self.tpdebug(info)
                return
            
            self.execute_teleport(info.player, *coords)
        except Exception as e:
            self.server.tell(info.player, f'§c获取坐标失败: {str(e)}')
    
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

    def Authentication(self, info: Info):
        """
        鉴权,如果为op则跳过模式检查
        :param info: 服务器信息对象
        :return: True/False
        """
        if not info.is_player:
            return False
        try:
            perm = self.server.get_permission_level(info.player)
            return perm >= 3
        except:
            return False
        
class Restart():
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def restart(self, info: Info):
        if not info.is_player:
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
        if not info.is_player or not info.content.split()[0] == '!l':
            return
        try:
            parts = info.content.split()
            if len(parts) < 2:
                num = random.randint(1, 10)
                ChatEvent(self.server, info, type="info", msg=f'§a[骰子] §r- §b生成的数为: §e{num}', log=f"骰子: {num}", say=True).guide()
                return
            
            range_str = parts[1]
            if '-' not in range_str:
                ChatEvent(self.server, info, type="error", msg='§c[骰子] §r- §c格式错误！正确格式：!l 1-10', log='骰子 格式错误', say=False).guide()
                return
                
            range1 = int(range_str.split('-')[0])
            range2 = int(range_str.split('-')[1])
            
            if range1 > range2:
                ChatEvent(self.server, info, type="error", msg='§c[骰子] §r- §c范围错误：前一个数必须小于后一个数！', log='骰子 范围错误', say=False).guide()
                return
            elif range1 == range2:
                ChatEvent(self.server, info, type="error", msg='§c[骰子] §r- §c范围错误：两个数不能相等！', log='骰子 范围错误', say=False).guide()
                return
            
            num = random.randint(range1, range2)
            ChatEvent(self.server, info, type="info", msg=f'§a[骰子] §r- §b生成的数为: §e{num}', log=f"骰子: {num}", say=True).guide()
        except Exception as e:
            ChatEvent(self.server, info, type="error", msg=f'§c[骰子] §r- §c发生错误: {str(e)}', log=f"骰子错误: {e}", say=False).guide()

class ManyPlayer():
    def __init__(self, server: PluginServerInterface):
        self.server = server

    @new_thread("SpawnPlayer")
    def SpawnPlayer(self, info: Info, player_num: int, sleep: float = 0):
        """
        在玩家位置生成假人
        :param info: Info 对象
        :param player_num: 要生成的假人数量
        :param sleep: 生成间隔时间（秒）
        """
        try:
            for i in range(player_num):
                # 直接在玩家位置生成假人
                self.server.execute(f'execute at {info.player} run player FakePlayer{i} spawn')
                
                if sleep > 0:
                    time.sleep(sleep)
                    
            ChatEvent(self.server, info, type="info", msg=f'§a成功在当前位置生成{player_num}个假人', log=f'生成假人: {player_num}个', say=True).guide()
        except Exception as e:
            ChatEvent(self.server, info, type="error", msg=f'§c生成假人时发生错误: {str(e)}', log=f'生成假人错误: {e}', say=False).guide()

    @new_thread("ManyPlayer")
    def ManyPlayer(self, info: Info):
        """
        处理假人命令
        :param info: Info 对象
        """
        if not info.is_player or not info.content.startswith('!mp'):
            return
        
        args = info.content.split()
        
        if len(args) < 2:
            ChatEvent(self.server, info, type="error", msg='§c语法错误：正确语法!mp <kill|cmd|spawn> <数量>', log='!mp 语法错误', say=False).guide()
            return
        
        # 处理 kill 命令
        if args[1] == 'kill':
            for i in range(256):
                self.server.execute(f'kill FakePlayer{i}')
            ChatEvent(self.server, info, type="info", msg='§a已清除所有假人', log='清除假人', say=True).guide()
            return
            
        # 处理 cmd 命令
        elif args[1] == 'cmd':
            if len(args) < 3:
                ChatEvent(self.server, info, type="error", msg='§c语法错误：!mp cmd <命令>', log='!mp cmd 语法错误', say=False).guide()
                return
            cmd = ' '.join(args[2:])
            for i in range(256):
                self.server.execute(f'player FakePlayer{i} {cmd}')
            ChatEvent(self.server, info, type="info", msg=f'§a已对所有假人执行命令: {cmd}', log=f'假人批量命令: {cmd}', say=True).guide()
            return
            
        # 处理 spawn 命令
        elif args[1] == 'spawn':
            if len(args) < 3:
                ChatEvent(self.server, info, type="error", msg='§c语法错误：!mp spawn <数量>', log='!mp spawn 参数不足', say=False).guide()
                return
                
            try:
                player_num = int(args[2])
            except ValueError:
                ChatEvent(self.server, info, type="error", msg='§c玩家数量必须是一个整数！', log='!mp 参数错误', say=False).guide()
                return
            
            # 权限检查
            try:
                permission_level = self.server.get_permission_level(info.player)
            except:
                permission_level = 0
                
            if permission_level < 1 and player_num > 20:
                ChatEvent(self.server, info, type="error", msg='§c你没有足够的权限创建超过20个假人！', log='权限不足', say=False).guide()
                return
            elif permission_level < 2 and player_num > 50:
                ChatEvent(self.server, info, type="error", msg='§c你没有足够的权限创建超过50个假人！', log='权限不足', say=False).guide()
                return
            elif player_num > 256:
                ChatEvent(self.server, info, type="error", msg='§c最多只能创建256个假人！', log='假人数量超限', say=False).guide()
                return
                
            # 直接生成，没有延迟
            self.SpawnPlayer(info, player_num, sleep=0)
            
        # 兼容旧的 slow 命令
        elif args[1] == 'slow':
            if len(args) < 3:
                ChatEvent(self.server, info, type="error", msg='§c语法错误：!mp slow <数量>', log='!mp slow 参数不足', say=False).guide()
                return
                
            try:
                player_num = int(args[2])
            except ValueError:
                ChatEvent(self.server, info, type="error", msg='§c玩家数量必须是一个整数！', log='!mp 参数错误', say=False).guide()
                return
            
            # 权限检查
            try:
                permission_level = self.server.get_permission_level(info.player)
            except:
                permission_level = 0
                
            if permission_level < 1 and player_num > 20:
                ChatEvent(self.server, info, type="error", msg='§c你没有足够的权限创建超过20个假人！', log='权限不足', say=False).guide()
                return
            elif permission_level < 2 and player_num > 50:
                ChatEvent(self.server, info, type="error", msg='§c你没有足够的权限创建超过50个假人！', log='权限不足', say=False).guide()
                return
            elif player_num > 256:
                ChatEvent(self.server, info, type="error", msg='§c最多只能创建256个假人！', log='假人数量超限', say=False).guide()
                return
                
            # slow 模式有1秒延迟
            self.SpawnPlayer(info, player_num, sleep=1)
            
        else:
            ChatEvent(self.server, info, type="error", msg='§c未知的子命令！可用: kill, cmd, spawn', log='!mp 未知子命令', say=False).guide()

class BetterChat:
    def __init__(self, server: PluginServerInterface):
        self.server = server
    
    @new_thread("BetterChat")
    def process_chat(self, info: Info):
        """处理聊天消息中的@功能"""
        if not info.is_player or '@' not in info.content:
            return
        if 'Command' in info.content:
            return  # 如果包含Server，直接返回不处理
        if info.player == "Server":
            return
        content = info.content
        player = info.player
        words = content.split()
        
        # 在线列表
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            ChatEvent(self.server, info, type="error", 
                     msg='§cMinecraft Data API未启用，无法使用@功能', 
                     log='Minecraft Data API 未启用', 
                     say=False).guide()
            return
            
        try:
            online_players = api.get_server_player_list().players
        except Exception as e:
            ChatEvent(self.server, info, type="error", 
                     msg=f'§c获取玩家列表失败: {str(e)}', 
                     log=f'获取玩家列表失败: {e}', 
                     say=False).guide()
            return
        
        # 处理每个词
        for i, word in enumerate(words):
            if not word.startswith('@'):
                continue
            
            # 处理@后面带空格
            if word == '@' and i + 1 < len(words):
                target = words[i + 1]
                self._process_target(player, target, online_players)
            # 处理直接@
            elif len(word) > 1:
                target = word[1:]
                self._process_target(player, target, online_players)
    
    def _process_target(self, sender: str, target: str, online_players: list):
        """处理@目标"""
        # 处理@a
        if target == 'a':
            self._at_all(sender, online_players)
            return
            
        # 处理@玩家
        if target in online_players:
            self._at_player(sender, target)
        else:
            ChatEvent(self.server, None, type="error", 
                     msg=f'§c玩家 §e{target} §c不在线', 
                     log=f"玩家不在线: {target}", 
                     say=True).guide()
    
    def _at_all(self, sender: str, players: list):
        """@所有人"""
        if not players:
            return
            
        # 通知
        ChatEvent(self.server, None, type="info", 
                 msg=f'§6{sender} §a@了所有人', 
                 log=f"{sender} @a", 
                 say=True).guide()
        
        # 音效、标题
        self.server.execute('title @a title ""')
        self.server.execute(f'title @a subtitle [{{"text":"{sender}","color":"aqua"}},{{"text":"@了所有人","color":"blue"}}]')
        self.server.execute('playsound minecraft:entity.player.levelup master @a')
    
    def _at_player(self, sender: str, target: str):
        """@指定玩家"""
        # 通知
        ChatEvent(self.server, None, type="info", 
                 msg=f'§6{sender} §a@了 §b{target}', 
                 log=f"{sender} @{target}", 
                 say=True).guide()
        
        # 音效、标题
        self.server.execute('title @a title ""')
        self.server.execute(f'title {target} subtitle [{{"text":"{sender}","color":"aqua"}},{{"text":"@了你","color":"blue"}}]')
        self.server.execute(f'playsound minecraft:entity.player.levelup master {target}')
       
class Scale():
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    def scale(self, info: Info):
        if not info.is_player or not info.content.startswith('!sc'):
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
            self.server.execute(f'attribute {info.player} minecraft:scale base set {scale_value}')
            ChatEvent(self.server, info, type="info", msg=f"§a成功将你的大小设置为 {scale_value}！", log=f"设置缩放: {scale_value}", say=False).guide()
        except Exception as e:
            ChatEvent(self.server, info, type="error", msg=f"§c发生错误: {str(e)}", say=False).guide()

class ItemHL():
    def __init__(self, server: PluginServerInterface):
        self.server = server
        
    @new_thread("ItemHighlight")
    def highlight_item(self, info: Info):
        if not info.is_player:
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
        helpmsg += "├┬─ §c!music p id <音乐ID> §r- 为所有玩家播放指定ID的音乐\n"
        helpmsg += "│├─ §c!music p name <音乐名称> §r- 为所有玩家播放指定名称的音乐\n"
        helpmsg += "│└─ §c!music p stop §r- 停止所有玩家播放的音乐\n"
        helpmsg += "├─ §c!music stop §r- 停止当前播放的音乐\n"
        helpmsg += "└─ §c!music §r- 显示帮助信息"
        ChatEvent(self.server, self.info, type="info", msg=helpmsg, log=None, say=False).guide()

    def PlayMusic(self):
        if not self.info.is_player or not self.info.content.startswith('!music'):
            return
            
        args = self.info.content.split()
        if len(args) < 2:
            self.help()
            return
            
        if args[1] == 'stop':
            self.server.execute(f'stopsound {self.info.player}')
            ChatEvent(self.server, self.info, type="info", msg='§a已停止播放音乐', log=f'停止音乐: {self.info.player}', say=False).guide()
            return
            
        if args[1] == 'p':
            if len(args) < 3:
                self.help()
                return
                
            if args[2] == 'stop':
                self.server.execute('stopsound @a')
                ChatEvent(self.server, self.info, type="info", msg='§a已停止所有玩家播放的音乐', log='停止所有音乐', say=False).guide()
                return
                
            if len(args) < 4:
                self.help()
                return
                
            if args[2] == 'name':
                music_name = args[3]
                if music_name not in music_dict:
                    ChatEvent(self.server, self.info, type="warn", msg=f"§c未找到名为 {music_name} 的音乐！可用音乐：{music_dict.keys()}...", log=f"未找到音乐: {music_name}", say=False).guide()
                    return
                music_id = music_dict[music_name]
                self.server.execute(f'execute at @a run playsound {music_id} player @a')
                ChatEvent(self.server, self.info, type="info", msg=f'§a正在为所有玩家播放: {music_name}', log=f'播放音乐: {music_name}', say=False).guide()
                
            elif args[2] == 'id':
                music_id = args[3]
                self.server.execute(f'execute at @a run playsound {music_id} player @a')
                ChatEvent(self.server, self.info, type="info", msg=f'§a正在为所有玩家播放音乐ID: {music_id}', log=f'播放音乐ID: {music_id}', say=False).guide()
            else:
                self.help()
                return
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
        """
        - type: <info|error|warn|help>
        - log: 需要发送到服务器控制台的日志信息
        - msg: 需要发送给玩家的消息
        - say: 是否使用say命令发送消息而不是tell命令
        """
        self.server = server
        self.info = info

        self.SendMsg = "§8[§2Tools§8] §r"
        self.SendLog = "§8[§2Tools§8] §r"

        self.log = log
        self.msg = msg
        self.say = say
        self.type = type

    def pack(self):
        if self.msg is not None:
            self.SendMsg += self.msg
        else:
            self.SendMsg = None
            
        if self.log is not None:
            self.SendLog += self.log
        else:
            self.SendLog = None
            
        self.send(send_msg=self.SendMsg, send_log=self.SendLog, say=self.say)

    def guide(self):
        if self.msg is None and self.log is None:
            return
            
        if self.type == "error":
            self.SendMsg += "§c§l[ERROR] §r"
            self.SendLog += "§c§l[ERROR] §r"
            self.pack()
        elif self.type == "warn":
            self.SendMsg += "§6§l[WARN] §r"
            self.SendLog += "§6§l[WARN]§r "
            self.pack()
        elif self.type == "info":
            self.pack()
        else:
            self.SendMsg = "§c[ERROR] §r在尝试处理消息文本时出错-->没有找到匹配的消息类型"
            self.pack()

    def send(self, send_msg: str, send_log: str, say: bool = False):
        """经过guide、pack导航并处理完成SendMsg后的消息处理"""
        if send_msg is not None:
            if say:
                self.server.say(send_msg)
            else:
                if self.info and self.info.is_player:
                    self.server.tell(self.info.player, send_msg)
                    
        if send_log is not None:
            self.server.logger.info(send_log)

    def help(self):
        if not self.info or not getattr(self.info, "is_player", False) or self.info.content != '!tools':
            return
            
        self.SendLog += f"§r[info] - 向{self.info.player}显示帮助信息"

        help_msg = "§e[Help] §r- "
        help_msg += "§bToolsPlugin 帮助信息§r\n"
        help_msg += "├─ §c!here | !h §r- 获取你当前所在位置的坐标和维度\n"
        help_msg += "├─ §c!kill §r- 自杀指令\n"
        help_msg += "├─ §c!tp <x> [<y>] <z> | !tp [<玩家>|<维度>] §r- 旁观模式传送指令\n"
        help_msg += "├─ §c!!restart §r- 重启服务器指令（需要权限）\n"
        help_msg += "├─ §c!l <范围1-范围2> §r- 在指定范围内生成一个随机数\n"
        help_msg += "├─┬§c!mp <kill|cmd|slow|spawn> <数量> [x y z] [朝向x 朝向y] [维度] §r- 假人管理指令\n"
        help_msg += "│    └─ §c维度: o(主世界) n(下界) e(末地)\n"
        help_msg += "├─ §c!p <玩家>|!p !move <玩家>|!p !b <玩家>|!p !t <玩家> §r- 假人控制指令\n"
        help_msg += "├─ §c!sc <数值> §r- 设置玩家大小指令\n"
        help_msg += "├─ §c!itemhl / !uitemhl §r- 高亮/取消高亮所有掉落物\n"
        help_msg += "├─ §c@a|@玩家名 §r- @玩家\n"
        help_msg += "├┬─ §c!music p id <音乐ID> §r- 为所有玩家播放指定ID的音乐\n"
        help_msg += "│├─ §c!music p name <音乐名称> §r- 为所有玩家播放指定名称的音乐\n"
        help_msg += "│├─ §c!music p stop §r- 停止所有玩家播放的音乐\n"
        help_msg += "│└─ §c!music stop §r- 停止当前播放的音乐\n"
        help_msg += "└─ §c!d <set|tp|list|del> [参数] §r- 位置传送管理"
        
        self.SendMsg += help_msg
        self.send(send_msg=self.SendMsg, send_log=self.SendLog, say=False)

def register_tools_commands(server: PluginServerInterface):
    """
    注册所有 Tools 插件命令到 MCDR 命令树
    支持 Tab 补全和 CommandSuggest 插件
    """
    from mcdreforged.api.command import Literal, Text, Integer, Float, Number, QuotableText
    from mcdreforged.api.rtext import RText, RColor, RStyle, RAction
    
    global settings
    
    if not settings.get('enable_tools', True):
        return
    
    server.logger.info("Registering Tools commands...")
    
    # ============ !tools 帮助命令 ============
    def tools_help_callback(source: CommandSource, context: CommandContext):
        if source.is_player:
            fake_info = type('Info', (), {
                'is_player': True,
                'player': source.player,
                'content': '!tools'
            })()
            ChatEvent(server, fake_info).help()
    
    tools_cmd = Literal('!tools').runs(tools_help_callback)
    server.register_command(tools_cmd)
    
    # ============ !kill 自杀命令 ============
    if settings.get('enable_kill', True):
        def kill_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': '!kill'
                })()
                Kill(server).kill(fake_info)
        
        kill_cmd = Literal('!kill').runs(kill_callback)
        server.register_command(kill_cmd)
    
    # ============ !here / !h 坐标命令 ============
    if settings.get('enable_here', True):
        def here_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': '!here'
                })()
                Here(server, fake_info).GetPos()
        
        here_cmd = Literal('!here').runs(here_callback)
        server.register_command(here_cmd)
        
        h_cmd = Literal('!h').runs(here_callback)
        server.register_command(h_cmd)
    
    # ============ !!restart 重启命令 ============
    if settings.get('enable_restart', True):
        def restart_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': '!!restart'
                })()
                Restart(server).restart(fake_info)
        
        restart_cmd = Literal('!!restart').runs(restart_callback)
        server.register_command(restart_cmd)
    
    # ============ !l 随机数命令 ============
    if settings.get('enable_random', True):
        def random_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                range_str = context.get('range', '')
                if range_str:
                    content = f'!l {range_str}'
                else:
                    content = '!l'
                
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': content
                })()
                Random(server).ListNumber(fake_info)
        
        random_root = Literal('!l')
        random_root.then(Text('range').runs(random_callback))
        random_root.runs(random_callback)
        server.register_command(random_root)
    
    # ============ !itemhl / !uitemhl 物品高亮命令 ============
    if settings.get('enable_itemhighlight', True):
        def itemhl_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': '!itemhl'
                })()
                ItemHL(server).highlight_item(fake_info)
        
        def uitemhl_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': '!uitemhl'
                })()
                ItemHL(server).highlight_item(fake_info)
        
        itemhl_cmd = Literal('!itemhl').runs(itemhl_callback)
        server.register_command(itemhl_cmd)
        
        uitemhl_cmd = Literal('!uitemhl').runs(uitemhl_callback)
        server.register_command(uitemhl_cmd)
    
    # ============ !d 位置传送命令 ============
    if settings.get('enable_position', True):
        pos_manager = Position(server)
        
        def pos_list_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                page = context.get('page', 1)
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!d list {page}'
                })()
                pos_manager.getpositionlist(fake_info, page)
        
        def pos_tp_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                name = context.get('name', '')
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!d tp {name}'
                })()
                # 创建 args 列表供 _teleport_to_position 使用
                args = ['!d', 'tp', name]
                pos_manager._teleport_to_position(fake_info, args)
        
        def pos_set_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                name = context.get('name', '')
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!d set {name}'
                })()
                pos_manager.set_location(fake_info)
        
        def pos_del_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                name = context.get('name', '')
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!d del {name}'
                })()
                pos_manager.delete_position(fake_info, name)
        
        pos_root = Literal('!d')
        
        # !d list [page]
        list_node = Literal('list').then(Integer('page').at_min(1).runs(pos_list_callback))
        list_node.runs(lambda s, c: pos_list_callback(s, {**c, 'page': 1}))
        pos_root.then(list_node)
        
        # !d tp <name>
        pos_root.then(Literal('tp').then(QuotableText('name').runs(pos_tp_callback)))
        
        # !d set <name>
        pos_root.then(Literal('set').then(QuotableText('name').runs(pos_set_callback)))
        
        # !d del <name>
        pos_root.then(Literal('del').then(QuotableText('name').runs(pos_del_callback)))
        
        server.register_command(pos_root)
    
    # ============ !tp 旁观传送命令 ============
    if settings.get('enable_tp', True):
        tp_manager = GamemodeTp(server)
        
        def tp_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                # 构建原始命令字符串
                parts = ['!tp']
                
                if 'x' in context and 'y' in context and 'z' in context:
                    parts.extend([str(context['x']), str(context['y']), str(context['z'])])
                elif 'x' in context and 'z' in context:
                    parts.extend([str(context['x']), str(context['z'])])
                elif 'player_or_dim' in context:
                    parts.append(context['player_or_dim'])
                
                raw_command = ' '.join(parts)
                
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': raw_command
                })()
                tp_manager.get_player_info(fake_info)
        
        tp_root = Literal('!tp')
        
        # !tp x y z
        tp_root.then(Float('x').then(Float('y').then(Float('z').runs(tp_callback))))
        
        # !tp x z
        tp_root.then(Float('x').then(Float('z').runs(tp_callback)))
        
        # !tp <player_or_dim>
        tp_root.then(Text('player_or_dim').runs(tp_callback))
        
        # !tp (默认)
        tp_root.runs(tp_callback)
        
        server.register_command(tp_root)
    
    # ============ !sc 缩放命令 ============
    if settings.get('enable_scale', True):
        scale_manager = Scale(server)
        
        def scale_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                scale = context.get('scale', 1.0)
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!sc {scale}'
                })()
                scale_manager.scale(fake_info)
        
        scale_root = Literal('!sc')
        scale_root.then(Number('scale').at_min(0.01).at_max(100).runs(scale_callback))
        scale_root.runs(lambda s, c: scale_callback(s, {**c, 'scale': 1.0}))
        
        server.register_command(scale_root)
    
    # ============ !music 音乐命令 ============
    if settings.get('enable_music', True):
        def music_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                raw_command = '!music'
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': raw_command
                })()
                Music(server, fake_info).PlayMusic()
        
        def music_p_name_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                music_name = context.get('music_name', '')
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!music p name {music_name}'
                })()
                Music(server, fake_info).PlayMusic()
        
        def music_p_id_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                music_id = context.get('music_id', '')
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!music p id {music_id}'
                })()
                Music(server, fake_info).PlayMusic()
        
        def music_p_stop_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': '!music p stop'
                })()
                Music(server, fake_info).PlayMusic()
        
        def music_stop_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': '!music stop'
                })()
                Music(server, fake_info).PlayMusic()
        
        music_root = Literal('!music')
        
        # !music stop
        music_root.then(Literal('stop').runs(music_stop_callback))
        
        # !music p ...
        p_node = Literal('p')
        
        # !music p stop
        p_node.then(Literal('stop').runs(music_p_stop_callback))
        
        # !music p name <music_name>
        p_node.then(Literal('name').then(Text('music_name').runs(music_p_name_callback)))
        
        # !music p id <music_id>
        p_node.then(Literal('id').then(Text('music_id').runs(music_p_id_callback)))
        
        music_root.then(p_node)
        
        # !music (help)
        music_root.runs(music_callback)
        
        server.register_command(music_root)
    
    # ============ !mp 假人管理命令（简化版） ============
    if settings.get('enable_manyplayer', True):
        manyplayer_manager = ManyPlayer(server)
        
        def mp_kill_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': '!mp kill'
                })()
                manyplayer_manager.ManyPlayer(fake_info)
        
        def mp_cmd_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                command = context.get('command', '')
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!mp cmd {command}'
                })()
                manyplayer_manager.ManyPlayer(fake_info)
        
        def mp_spawn_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                count = context.get('count', 1)
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!mp spawn {count}'
                })()
                manyplayer_manager.ManyPlayer(fake_info)
        
        def mp_slow_callback(source: CommandSource, context: CommandContext):
            if source.is_player:
                count = context.get('count', 1)
                fake_info = type('Info', (), {
                    'is_player': True,
                    'player': source.player,
                    'content': f'!mp slow {count}'
                })()
                manyplayer_manager.ManyPlayer(fake_info)
        
        mp_root = Literal('!mp')
        
        # !mp kill
        mp_root.then(Literal('kill').runs(mp_kill_callback))
        
        # !mp cmd <command>
        mp_root.then(Literal('cmd').then(Text('command').runs(mp_cmd_callback)))
        
        # !mp spawn <count>
        mp_root.then(Literal('spawn').then(Integer('count').at_min(1).at_max(256).runs(mp_spawn_callback)))
        
        # !mp slow <count>
        mp_root.then(Literal('slow').then(Integer('count').at_min(1).at_max(256).runs(mp_slow_callback)))
        
        server.register_command(mp_root)
    
    server.logger.info("Tools commands registered successfully!")


    