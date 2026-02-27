from mcdreforged.api.all import *
from mcdreforged.api.rtext import RText, RTextList, RColor, RAction
import time
from .utils import ChatEvent


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
    
    def getpositionlist(self, info: Info, page: int = 1, per_page: int = 12):
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
            self.server.tell(info.source.player, out_of_range_msg)
            page = max(1, min(page, max_page))
        
        title = RTextList(
            RText('========== ', RColor.gray),
            RText('传送位置列表', RColor.gold),
            RText(' ==========', RColor.gray)
        )
        self.server.tell(info.source.player, title)
        
        count_text = RTextList(
            RText('共有 ', RColor.gray),
            RText(str(total_count), RColor.yellow),
            RText(' 个位置', RColor.gray)
        )
        self.server.tell(info.source.player, count_text)
        
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
            self.server.tell(info.source.player, item_line)
        
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
        self.server.tell(info.source.player, nav_line)
    
    def __make_pos_list_command(self, page: int) -> str:
        """
        生成翻页命令字符串
        
        :param page: 目标页码
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
            '§c语法错误!正确语法：!d tp <位置名称> | !d set <位置名称> | !d list\n'
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
        if not info.source.is_player or not info.content.startswith('!d'):
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
            
            dimension = self._dimension_to_command(dimension_id)
            
            self.server.execute(f'execute in {dimension} run tp {info.source.player} {pos_str}')
            
            dim_text = self._dimension_to_text(dimension_id)
            ChatEvent(self.server, info, type="info", 
                     msg=f'§a已将 {info.source.player} 传送到 §6{location_name} §a({dim_text})', 
                     log=f"玩家 {info.source.player} 传送到 {location_name}", 
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
        
        config_data = self._load_config()
        if name in config_data.get('Position', {}):
            ChatEvent(self.server, info, type="error", 
                     msg=f'§c位置 "{name}" 已存在！请使用其他名称', 
                     log=f'位置名称已存在: {name}', 
                     say=True).guide()
            return
        
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            ChatEvent(self.server, info, type="error", 
                     msg='§cMinecraft Data API未启用!', 
                     log='Minecraft Data API 未启用', 
                     say=False).guide()
            return
        
        try:
            dimension = api.get_player_dimension(info.source.player)
            location = api.get_player_coordinate(info.source.player)
            
            x = round(location.x)
            y = round(location.y)
            z = round(location.z)
            pos_str = f"{x} {y} {z}"
            
            config_data.setdefault('Position', {})
            config_data['Position'][name] = {
                'location': pos_str,
                'dimension': dimension,
                'by': info.source.player,
                'time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self._save_config(config_data)
            
            dim_text = self._dimension_to_text(dimension)
            ChatEvent(self.server, info, type="info", 
                     msg=f'§a已保存位置 §6{name} §a: §e{x} {y} {z} §a在 §d{dim_text}', 
                     log=f"玩家 {info.source.player} 保存位置 {name} [{x} {y} {z}]", 
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
        perm = self.server.get_permission_level(info.source.player)
        if perm < 3:
            ChatEvent(self.server, info, type="error", 
                     msg='§c你没有权限删除位置!', 
                     log='权限不足', 
                     say=False).guide()
            return
        
        config_data = self._load_config()
        if name in config_data.get('Position', {}):
            del config_data['Position'][name]
            self._save_config(config_data)
            ChatEvent(self.server, info, type="info", 
                     msg=f'§a已删除位置 §6{name}', 
                     log=f"玩家 {info.source.player} 删除位置 {name}", 
                     say=True).guide()
        else:
            ChatEvent(self.server, info, type="error", 
                     msg=f'§c未找到位置 "{name}"！', 
                     log=f'删除失败，位置不存在: {name}', 
                     say=True).guide()
