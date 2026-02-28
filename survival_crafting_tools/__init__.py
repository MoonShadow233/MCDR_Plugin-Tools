from mcdreforged.api.all import *
from .utils import ChatEvent

PLUGIN_NAME = 'survival_crafting_tools'
VERSION = '1.2.0'

settings = {}
config = {}

def on_load(server: PluginServerInterface):
    global settings, config
    
    conf(server)
    
    PLUGIN_ENABLED = settings.get('enable_tools', False)
    if PLUGIN_ENABLED:
        ChatEvent(server, None, type="info", msg=f'§aTools插件{VERSION} by MoonShadow233 加载成功', say=True).guide()
        register_commands(server)
    else:
        ChatEvent(server, None, type="info", msg='====================================================', say=True).guide()
        ChatEvent(server, None, type="info", msg=f'§cTools插件被禁用!版本：{VERSION}', say=True).guide()
        ChatEvent(server, None, type="info", msg='§c在 https://github.com/MoonShadow233/MCDR_Plugin-Tools 阅读插件使用说明！', say=True).guide()
        ChatEvent(server, None, type="info", msg='====================================================', say=True).guide()
        return
    server.logger.info(f'{PLUGIN_NAME} 插件 加载成功 版本: {VERSION}')

def on_unload(server: PluginServerInterface):
    ChatEvent(server, None, type="info", msg='插件已卸载', log='插件已卸载', say=False).guide()

def on_info(server: PluginServerInterface, info: Info):
    global settings
    
    if info.content is None or not settings.get('enable_tools', True):
        return
    
    if settings.get('enable_betterchat', True):
        from .betterchat import BetterChat
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
    Position: dict = {}

def conf(server: PluginServerInterface):
    global config, settings
    config = server.load_config_simple(
        'config.json',
        target_class=Config
    )
    settings = config.settings

def register_commands(server: PluginServerInterface):
    global settings
    
    if settings.get('enable_here', True):
        from .here import register as register_here
        register_here(server)
    
    if settings.get('enable_kill', True):
        from .kill import register as register_kill
        register_kill(server)
    
    if settings.get('enable_position', True):
        from .position import register as register_position
        register_position(server)
    
    if settings.get('enable_tp', True):
        from .gamemodetp import register as register_tp
        register_tp(server)
    
    if settings.get('enable_restart', True):
        from .restart import register as register_restart
        register_restart(server)
    
    if settings.get('enable_random', True):
        from .random import register as register_random
        register_random(server)
    
    if settings.get('enable_manyplayer', True):
        from .manyplayer import register as register_manyplayer
        register_manyplayer(server)
    
    if settings.get('enable_scale', True):
        from .scale import register as register_scale
        register_scale(server)
    
    if settings.get('enable_itemhighlight', True):
        from .itemhl import register as register_itemhl
        register_itemhl(server)
    
    if settings.get('enable_music', True):
        from .music import register as register_music
        register_music(server)
