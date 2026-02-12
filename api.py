from mcdreforged.api.all import *
from typing import Callable, Optional, Dict, Any, List
import json
import uuid

_button_registry: Dict[str, dict] = {}
_server_instance: Optional[PluginServerInterface] = None


def init_button_system(server: PluginServerInterface) -> None:
    """
    初始化按钮系统，在 on_load 中调用
    
    :param server: PluginServerInterface 实例
    """
    global _server_instance
    _server_instance = server
    
    server.register_command(
        Literal('button').then(
            Text('id').runs(lambda src, ctx: _on_button_click(src, ctx['id']))
        )
    )
    
    server.register_command(
        Literal('btn').then(
            Text('id').runs(lambda src, ctx: _on_button_click(src, ctx['id']))
        )
    )


def _on_button_click(source: CommandSource, button_id: str) -> None:
    """
    按钮点击处理函数
    
    :param source: 命令来源
    :param button_id: 按钮ID
    """
    if button_id not in _button_registry:
        if source.is_player:
            source.reply('§c按钮已过期或无效')
        return
    
    button_info = _button_registry[button_id]
    callback = button_info['callback']
    data = button_info['data']
    
    try:
        if data is not None:
            callback(source, data)
        else:
            callback(source)
    except Exception as e:
        if source.is_player:
            source.reply(f'§c按钮执行出错: {e}')
        if _server_instance:
            _server_instance.logger.error(f'Button callback error: {e}')


class ButtonManager:
    """
    按钮管理器
    用于创建、注册和管理可点击按钮
    """
    
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.cb = ClickableButton(server)
    
    def create_button(
        self,
        text: str,
        callback: Callable,
        data: Any = None,
        color: str = 'yellow',
        bold: bool = False,
        hover_text: Optional[str] = None,
        button_id: Optional[str] = None
    ) -> dict:
        """
        创建一个带命令回调的按钮
        
        :param text: 按钮显示文本
        :param callback: 点击回调函数 callback(source, data) 或 callback(source)
        :param data: 传递给回调的数据
        :param color: 按钮颜色
        :param bold: 是否加粗
        :param hover_text: 悬停提示
        :param button_id: 自定义按钮ID，不指定则自动生成
        :return: JSON 组件字典
        """
        if button_id is None:
            button_id = uuid.uuid4().hex[:8]
        
        _button_registry[button_id] = {
            'callback': callback,
            'data': data,
            'text': text
        }
        
        command = f'/button {button_id}'
        
        return self.cb.create_button(
            text=text,
            action='run_command',
            value=command,
            color=color,
            bold=bold,
            hover_text=hover_text
        )
    
    def create_button_simple(
        self,
        text: str,
        command: str,
        color: str = 'yellow',
        bold: bool = False,
        hover_text: Optional[str] = None
    ) -> dict:
        """
        创建一个直接执行命令的按钮（不通过回调）
        
        :param text: 按钮显示文本
        :param command: 要执行的命令（如 !tp 100 64 100）
        :param color: 按钮颜色
        :param bold: 是否加粗
        :param hover_text: 悬停提示
        :return: JSON 组件字典
        """
        return self.cb.create_button(
            text=text,
            action='run_command',
            value=command,
            color=color,
            bold=bold,
            hover_text=hover_text
        )
    
    def remove_button(self, button_id: str) -> bool:
        """
        移除注册的按钮
        
        :param button_id: 按钮ID
        :return: 是否成功移除
        """
        if button_id in _button_registry:
            del _button_registry[button_id]
            return True
        return False
    
    def clear_buttons(self) -> None:
        """清除所有注册的按钮"""
        _button_registry.clear()
    
    def get_button_count(self) -> int:
        """获取已注册按钮数量"""
        return len(_button_registry)


class ClickableButton:
    """
    Tellraw 可点击按钮工具类
    用于创建自定义颜色、动作的可点击按钮
    """
    
    ACTION_RUN_COMMAND = 'run_command'
    ACTION_SUGGEST_COMMAND = 'suggest_command'
    ACTION_COPY_TO_CLIPBOARD = 'copy_to_clipboard'
    ACTION_OPEN_URL = 'open_url'
    
    def __init__(self, server: PluginServerInterface):
        self.server = server
    
    def create_button(
        self,
        text: str,
        action: str,
        value: str,
        color: str = 'yellow',
        bold: bool = False,
        italic: bool = False,
        underlined: bool = False,
        strikethrough: bool = False,
        obfuscated: bool = False,
        hover_text: Optional[str] = None
    ) -> dict:
        """
        创建单个可点击按钮的 JSON 组件
        
        :param text: 按钮显示的文本
        :param action: 点击动作类型 (run_command/suggest_command/copy_to_clipboard/open_url)
        :param value: 点击后执行的值（命令/URL/复制内容）
        :param color: 按钮颜色
        :param bold: 是否加粗
        :param italic: 是否斜体
        :param underlined: 是否下划线
        :param strikethrough: 是否删除线
        :param obfuscated: 是否混淆
        :param hover_text: 悬停提示文本
        :return: JSON 组件字典
        """
        component = {
            'text': text,
            'color': color,
            'bold': bold,
            'italic': italic,
            'underlined': underlined,
            'strikethrough': strikethrough,
            'obfuscated': obfuscated,
            'click_event': {
                'action': action,
                'value': value
            }
        }
        
        if hover_text:
            component['hover_event'] = {
                'action': 'show_text',
                'value': {'text': hover_text}
            }
        
        return component
    
    def create_text(
        self,
        text: str,
        color: str = 'white',
        bold: bool = False,
        italic: bool = False,
        underlined: bool = False
    ) -> dict:
        """
        创建普通文本组件
        
        :param text: 文本内容
        :param color: 文本颜色
        :param bold: 是否加粗
        :param italic: 是否斜体
        :param underlined: 是否下划线
        :return: JSON 组件字典
        """
        return {
            'text': text,
            'color': color,
            'bold': bold,
            'italic': italic,
            'underlined': underlined
        }
    
    def send_to_player(
        self,
        player: str,
        components: List[dict],
        prefix: Optional[str] = None
    ) -> None:
        """
        发送按钮消息给指定玩家
        
        :param player: 玩家名称
        :param components: JSON 组件列表
        :param prefix: 消息前缀文本
        """
        if prefix:
            components = [self.create_text(prefix)] + components
        
        self.server.execute(f'tellraw {player} {self._build_json(components)}')
    
    def send_to_all(
        self,
        components: List[dict],
        prefix: Optional[str] = None
    ) -> None:
        """
        发送按钮消息给所有玩家
        
        :param components: JSON 组件列表
        :param prefix: 消息前缀文本
        """
        if prefix:
            components = [self.create_text(prefix)] + components
        
        self.server.execute(f'tellraw @a {self._build_json(components)}')
    
    def _build_json(self, components: List[dict]) -> str:
        """
        构建 tellraw JSON 字符串
        
        :param components: JSON 组件列表
        :return: JSON 字符串
        """
        return json.dumps(components, ensure_ascii=False)


class ButtonBuilder:
    """
    链式构建按钮消息的构建器
    """
    
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.cb = ClickableButton(server)
        self.bm: Optional[ButtonManager] = None
        self.components: List[dict] = []
    
    def text(self, text: str, color: str = 'white', bold: bool = False) -> 'ButtonBuilder':
        """添加普通文本"""
        self.components.append(self.cb.create_text(text, color, bold))
        return self
    
    def button(
        self,
        text: str,
        action: str,
        value: str,
        color: str = 'yellow',
        bold: bool = False,
        hover_text: Optional[str] = None
    ) -> 'ButtonBuilder':
        """添加可点击按钮（直接执行命令）"""
        self.components.append(self.cb.create_button(
            text=text,
            action=action,
            value=value,
            color=color,
            bold=bold,
            hover_text=hover_text
        ))
        return self
    
    def callback_button(
        self,
        text: str,
        callback: Callable,
        data: Any = None,
        color: str = 'yellow',
        bold: bool = False,
        hover_text: Optional[str] = None
    ) -> 'ButtonBuilder':
        """
        添加带回调的按钮
        
        :param text: 按钮文本
        :param callback: 回调函数 callback(source, data)
        :param data: 回调数据
        :param color: 颜色
        :param bold: 是否加粗
        :param hover_text: 悬停提示
        """
        if self.bm is None:
            self.bm = ButtonManager(self.server)
        
        self.components.append(self.bm.create_button(
            text=text,
            callback=callback,
            data=data,
            color=color,
            bold=bold,
            hover_text=hover_text
        ))
        return self
    
    def space(self, count: int = 1) -> 'ButtonBuilder':
        """添加空格"""
        self.components.append(self.cb.create_text(' ' * count))
        return self
    
    def newline(self) -> 'ButtonBuilder':
        """添加换行"""
        self.components.append(self.cb.create_text('\n'))
        return self
    
    def send_to(self, target: str) -> None:
        """发送给指定目标"""
        self.server.execute(f'tellraw {target} {self.cb._build_json(self.components)}')
    
    def send_all(self) -> None:
        """发送给所有玩家"""
        self.send_to('@a')
    
    def build(self) -> List[dict]:
        """构建组件列表"""
        return self.components.copy()


def create_callback_button(
    server: PluginServerInterface,
    text: str,
    callback: Callable,
    data: Any = None,
    color: str = 'yellow',
    bold: bool = False,
    hover_text: Optional[str] = None
) -> dict:
    """
    快捷函数：创建带回调的按钮
    
    :param server: PluginServerInterface 实例
    :param text: 按钮文本
    :param callback: 回调函数
    :param data: 回调数据
    :param color: 颜色
    :param bold: 是否加粗
    :param hover_text: 悬停提示
    :return: JSON 组件字典
    """
    return ButtonManager(server).create_button(
        text=text,
        callback=callback,
        data=data,
        color=color,
        bold=bold,
        hover_text=hover_text
    )


def create_button(
    server: PluginServerInterface,
    text: str,
    action: str,
    value: str,
    color: str = 'yellow',
    bold: bool = False,
    hover_text: Optional[str] = None
) -> dict:
    """
    快捷函数：创建单个可点击按钮
    
    :param server: PluginServerInterface 实例
    :param text: 按钮显示文本
    :param action: 点击动作类型
    :param value: 点击后执行的值
    :param color: 按钮颜色
    :param bold: 是否加粗
    :param hover_text: 悬停提示
    :return: JSON 组件字典
    """
    return ClickableButton(server).create_button(
        text=text,
        action=action,
        value=value,
        color=color,
        bold=bold,
        hover_text=hover_text
    )


def send_buttons(
    server: PluginServerInterface,
    target: str,
    buttons: List[dict],
    separator: str = ' ',
    prefix: Optional[str] = None
) -> None:
    """
    快捷函数：发送多个按钮给目标
    
    :param server: PluginServerInterface 实例
    :param target: 目标玩家或 @a
    :param buttons: 按钮组件列表
    :param separator: 按钮之间的分隔符
    :param prefix: 消息前缀
    """
    cb = ClickableButton(server)
    components = []
    
    if prefix:
        components.append(cb.create_text(prefix))
    
    for i, button in enumerate(buttons):
        components.append(button)
        if i < len(buttons) - 1:
            components.append(cb.create_text(separator))
    
    server.execute(f'tellraw {target} {cb._build_json(components)}')


"""
================================================================================
                                    使用示例
================================================================================

# 在你的插件主文件中（如 Tools.py）：

from mcdreforged.api.all import *
from api import init_button_system, ButtonManager, ButtonBuilder, create_callback_button

# 1. 在 on_load 中初始化按钮系统
def on_load(server: PluginServerInterface, prev_module):
    init_button_system(server)
    # 注册一个测试命令
    server.register_command(
        Literal('!!testbtn').runs(lambda src: show_test_menu(server, src))
    )

# 2. 示例：显示一个带回调按钮的菜单
def show_test_menu(server: PluginServerInterface, source: CommandSource):
    if not source.is_player:
        source.reply('§c此命令只能由玩家执行')
        return
    
    player = source.player
    
    def on_confirm(src, data):
        src.reply(f'§a你确认了操作！选项: {data["option"]}')
        server.execute(f'gamemode creative {src.player}')
    
    def on_cancel(src):
        src.reply('§c你取消了操作')
    
    def on_tp(src, coords):
        x, y, z = coords['x'], coords['y'], coords['z']
        server.execute(f'tp {src.player} {x} {y} {z}')
        src.reply(f'§a已传送到 {x} {y} {z}')
    
    ButtonBuilder(server) \
        .text('========== 测试菜单 ==========', 'gold', bold=True) \
        .newline() \
        .text('请选择操作：', 'white') \
        .newline() \
        .callback_button('[确认]', on_confirm, data={'option': 'A'}, color='green', bold=True, hover_text='确认操作') \
        .space(2) \
        .callback_button('[取消]', on_cancel, color='red', bold=True, hover_text='取消操作') \
        .newline() \
        .text('快捷传送：', 'yellow') \
        .callback_button('[主城]', on_tp, data={'x': 0, 'y': 64, 'z': 0}, color='aqua', hover_text='传送到主城') \
        .space() \
        .callback_button('[资源区]', on_tp, data={'x': 1000, 'y': 64, 'z': 1000}, color='aqua', hover_text='传送到资源区') \
        .newline() \
        .text('==============================', 'gold', bold=True) \
        .send_to(player)

# 3. 示例：使用 ButtonManager 创建单独的按钮
def show_single_button(server: PluginServerInterface, player: str):
    bm = ButtonManager(server)
    
    def on_click(src, data):
        src.reply(f'§e按钮被点击了！数据: {data}')
    
    btn = bm.create_button(
        text='[点击我]',
        callback=on_click,
        data={'info': 'test'},
        color='gold',
        bold=True,
        hover_text='这是一个测试按钮'
    )
    
    bm.cb.send_to_player(player, [btn], prefix='§b测试按钮：')

# 4. 示例：直接执行命令的按钮（不使用回调）
def show_command_buttons(server: PluginServerInterface, player: str):
    ButtonBuilder(server) \
        .text('快捷操作：', 'white') \
        .button('[自杀]', 'run_command', '!kill', 'red', hover_text='执行自杀命令') \
        .space() \
        .button('[查看坐标]', 'run_command', '!here', 'green', hover_text='显示当前坐标') \
        .space() \
        .button('[复制服务器IP]', 'copy_to_clipboard', 'play.example.com:25565', 'aqua', hover_text='复制到剪贴板') \
        .send_to(player)

# 5. 示例：确认对话框
def show_confirm_dialog(server: PluginServerInterface, player: str, message: str, on_yes: Callable, on_no: Callable = None):
    if on_no is None:
        on_no = lambda src: src.reply('§c操作已取消')
    
    ButtonBuilder(server) \
        .text(message, 'yellow') \
        .newline() \
        .callback_button('[是]', on_yes, color='green', bold=True) \
        .space(3) \
        .callback_button('[否]', on_no, color='red', bold=True) \
        .send_to(player)

# 使用确认对话框
def restart_server_dialog(server: PluginServerInterface, source: CommandSource):
    if not source.is_player:
        return
    
    def do_restart(src):
        src.reply('§a服务器将在 5 秒后重启...')
        server.restart()
    
    show_confirm_dialog(server, source.player, '§c确定要重启服务器吗？', do_restart)

================================================================================
"""
