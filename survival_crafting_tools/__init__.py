from mcdreforged.api.all import *
from typing import Any
from .here import Here
from .kill import Kill
from .position import Position
from .gamemodetp import GamemodeTp
from .restart import Restart
from .random import Random
from .manyplayer import ManyPlayer
from .betterchat import BetterChat
from .scale import Scale
from .itemhl import ItemHL
from .music import Music
from .utils import ChatEvent, music_dict

PLUGIN_NAME = 'survival_crafting_tools'
VERSION = '1.2.0'
IS_MCDR_COMMAND_FABRIC = False

settings = {}
config = {}
IssueUrl = ""
GithubUrl = ""

def on_load(server: PluginServerInterface, prev_module):
    global IssueUrl, GithubUrl, PLUGIN_ENABLED, settings, config
    
    IssueUrl = "https://github.com/MoonShadow233/MCDR_Plugin-Tools/issues"
    GithubUrl = "https://github.com/MoonShadow233/MCDR_Plugin-Tools"
    
    conf(server)
    
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
        'enable_tools': True,
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

def register_tools_commands(server: PluginServerInterface):
    global settings
    
    # !h / !here - 发送当前位置
    if settings.get('enable_here', True):
        def on_here_command(context: CommandContext):
            Here(context.source.get_server(), context).GetPos()
        server.register_command(Literal('!!h').runs(on_here_command))
        server.register_command(Literal('!!here').runs(on_here_command))
    
    # !kill - 自杀
    if settings.get('enable_kill', True):
        def on_kill_command(context: CommandContext):
            Kill(context.source.get_server()).kill(context)
        server.register_command(Literal('!!kill').runs(on_kill_command))
    
    # !d - 位置管理
    if settings.get('enable_position', True):
        def on_position_command(context: CommandContext):
            Position(context.source.get_server()).set_position(context)
        server.register_command(Literal('!!d').runs(on_position_command))
    
    # !tp - 旁观模式传送
    if settings.get('enable_tp', True):
        def on_tp_command(context: CommandContext):
            GamemodeTp(context.source.get_server()).get_player_info(context)
        server.register_command(Literal('!!tp').runs(on_tp_command))
    
    # !restart - 重启服务器
    if settings.get('enable_restart', True):
        def on_restart_command(context: CommandContext):
            Restart(context.source.get_server()).restart(context)
        server.register_command(Literal('!!restart').runs(on_restart_command))
    
    # !l - 随机数
    if settings.get('enable_random', True):
        def on_random_command(context: CommandContext):
            Random(context.source.get_server()).ListNumber(context)
        server.register_command(Literal('!!l').runs(on_random_command))
    
    # !mp - 假人管理
    if settings.get('enable_manyplayer', True):
        def on_manyplayer_command(context: CommandContext):
            ManyPlayer(context.source.get_server()).ManyPlayer(context)
        server.register_command(Literal('!!mp').runs(on_manyplayer_command))
    
    # !sc - 玩家缩放
    if settings.get('enable_scale', True):
        def on_scale_command(context: CommandContext):
            Scale(context.source.get_server()).scale(context)
        server.register_command(Literal('!!sc').runs(on_scale_command))
    
    # !itemhl / !uitemhl - 物品高亮
    if settings.get('enable_itemhighlight', True):
        def on_itemhl_command(context: CommandContext):
            ItemHL(context.source.get_server()).highlight_item(context)
        server.register_command(Literal('!!itemhl').runs(on_itemhl_command))
        server.register_command(Literal('!!uitemhl').runs(on_itemhl_command))
    
    # !music - 音乐播放
    if settings.get('enable_music', True):
        def on_music_command(context: CommandContext):
            Music(context.source.get_server(), context).PlayMusic()
        server.register_command(Literal('!!music').runs(on_music_command))
