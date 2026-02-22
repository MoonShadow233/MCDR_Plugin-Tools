from mcdreforged.api.all import *
import time
import random

PLUGIN_ID = 'tools'
PLUGIN_NAME = 'Tools'
VERSION = '1.1.3'
IS_MCDR_COMMAND_FABRIC = True

server_instance: PluginServerInterface = None
config = None
settings = {}
music_dict = {}
IssueUrl = "https://github.com/MoonShadow233/MCDR_Plugin-Tools/issues"
GithubUrl = "https://github.com/MoonShadow233/MCDR_Plugin-Tools"

def on_load(server: PluginServerInterface, prev_module):
    global server_instance, config, settings, music_dict
    server_instance = server
    conf(server)

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
        register_commands(server)
    else:
        ChatEvent(server, None, type="info", msg='====================================================', say=True).guide()
        ChatEvent(server, None, type="info", msg=f'§cTools插件被禁用!版本：{VERSION}', say=True).guide()
        ChatEvent(server, None, type="info", msg=f'§c在{GithubUrl}阅读插件使用说明！', say=True).guide()
        ChatEvent(server, None, type="info", msg='====================================================', say=True).guide()
        return
    server.logger.info(f'{PLUGIN_NAME} 插件 加载成功 版本: {VERSION}')

def register_commands(server: PluginServerInterface):
    builder = SimpleCommandBuilder()

    @builder.command('!tools')
    def cmd_tools_help(source: CommandSource):
        help_msg = "§e[Help] §r- §bToolsPlugin 帮助信息§r\n"
        help_msg += "├─ §c!here | !h §r- 获取你当前所在位置的坐标和维度\n"
        help_msg += "├─ §c!kill §r- 自杀指令\n"
        help_msg += "├─ §c!tp <x> [<y>] <z> | !tp [<玩家>|<维度>] §r- 旁观模式传送指令\n"
        help_msg += "├─ §c!!restart §r- 重启服务器指令（需要权限）\n"
        help_msg += "├─ §c!l [<max>] §r- 生成随机数（默认100）\n"
        help_msg += "├─ §c!p <name> [<dim> <x> <y> <z>] §r- 假人生成\n"
        help_msg += "├─ §c!mp spawn|slow|kill|cmd <count|name|cmd> §r- 批量假人管理\n"
        help_msg += "├─ §c!sc <value> §r- 设置玩家大小\n"
        help_msg += "├─ §c!itemhl | !uitemhl §r- 高亮/取消高亮掉落物\n"
        help_msg += "├─ §c@a | @<玩家名> §r- 在聊天中@玩家\n"
        help_msg += "├─ §c!music §r- 音乐播放帮助\n"
        help_msg += "└─ §c!d §r- 传送点管理（支持点击翻页和操作按钮）"
        source.reply(help_msg)

    if settings.get('enable_here', True):
        @builder.command('!here')
        @builder.command('!h')
        def cmd_here(source: CommandSource):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            HereHandler(source).execute()

    if settings.get('enable_kill', True):
        @builder.command('!kill')
        def cmd_kill(source: CommandSource):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            KillHandler(source).execute()

    if settings.get('enable_tp', True):
        @builder.command('!tp')
        def cmd_tp_help(source: CommandSource):
            TpHandler(source).show_help()

        @builder.command('!tp <target>')
        def cmd_tp_player(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            TpHandler(source).tp_player(ctx['target'])

        @builder.command('!tp <x> <z>')
        def cmd_tp_xz(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            TpHandler(source).tp_xz(ctx['x'], ctx['z'])

        @builder.command('!tp <x> <y> <z>')
        def cmd_tp_xyz(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            TpHandler(source).tp_xyz(ctx['x'], ctx['y'], ctx['z'])

    if settings.get('enable_restart', True):
        @builder.command('!!restart')
        def cmd_restart(source: CommandSource):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            RestartHandler(source).execute()

    if settings.get('enable_random', True):
        @builder.command('!l')
        def cmd_random_100(source: CommandSource):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            RandomHandler(source).execute(100)

        @builder.command('!l <max>')
        def cmd_random_max(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            RandomHandler(source).execute(ctx['max'])

    if settings.get('enable_fakeplayer', True):
        @builder.command('!p')
        def cmd_fakeplayer_help(source: CommandSource):
            FakePlayerHandler(source).show_help()

        @builder.command('!p <name>')
        def cmd_fakeplayer_spawn(source: CommandSource, ctx: dict):
            FakePlayerHandler(source).spawn(ctx['name'])

        @builder.command('!p <name> <dim> <x> <y> <z>')
        def cmd_fakeplayer_spawn_at(source: CommandSource, ctx: dict):
            FakePlayerHandler(source).spawn_at(ctx['name'], ctx['dim'], ctx['x'], ctx['y'], ctx['z'])

    if settings.get('enable_manyplayer', True):
        @builder.command('!mp')
        def cmd_mp_help(source: CommandSource):
            ManyPlayerHandler(source).show_help()

        @builder.command('!mp spawn <count>')
        def cmd_mp_spawn(source: CommandSource, ctx: dict):
            ManyPlayerHandler(source).spawn(ctx['count'])

        @builder.command('!mp slow <count>')
        def cmd_mp_slow(source: CommandSource, ctx: dict):
            ManyPlayerHandler(source).spawn_slow(ctx['count'])

        @builder.command('!mp kill <name>')
        def cmd_mp_kill(source: CommandSource, ctx: dict):
            ManyPlayerHandler(source).kill(ctx['name'])

        @builder.command('!mp cmd <cmd>')
        def cmd_mp_cmd(source: CommandSource, ctx: dict):
            ManyPlayerHandler(source).run_cmd(ctx['cmd'])

    if settings.get('enable_scale', True):
        @builder.command('!sc <value>')
        def cmd_scale(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            ScaleHandler(source).set_scale(ctx['value'])

    if settings.get('enable_itemhighlight', True):
        @builder.command('!itemhl')
        def cmd_itemhl_on(source: CommandSource):
            ItemHLHandler(source).enable()

        @builder.command('!uitemhl')
        def cmd_itemhl_off(source: CommandSource):
            ItemHLHandler(source).disable()

    if settings.get('enable_music', True):
        @builder.command('!music')
        def cmd_music_help(source: CommandSource):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            MusicHandler(source).show_help()

        @builder.command('!music stop')
        def cmd_music_stop(source: CommandSource):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            MusicHandler(source).stop()

        @builder.command('!music p stop')
        def cmd_music_all_stop(source: CommandSource):
            MusicHandler(source).stop_all()

        @builder.command('!music p name <name>')
        def cmd_music_name(source: CommandSource, ctx: dict):
            MusicHandler(source).play_name(ctx['name'])

        @builder.command('!music p id <id>')
        def cmd_music_id(source: CommandSource, ctx: dict):
            MusicHandler(source).play_id(ctx['id'])

    if settings.get('enable_position', True):
        @builder.command('!d')
        def cmd_pos_help(source: CommandSource):
            PositionHandler(source).show_help()

        @builder.command('!d list')
        def cmd_list(source: CommandSource):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            PositionHandler(source).list_positions(1)

        @builder.command('!d list <page>')
        def cmd_list_page(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            PositionHandler(source).list_positions(ctx['page'])

        @builder.command('!d tp <name>')
        def cmd_tp(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            PositionHandler(source).teleport(ctx['name'])

        @builder.command('!d set <name>')
        def cmd_set(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            PositionHandler(source).set_location(ctx['name'])

        @builder.command('!d del <name>')
        def cmd_del(source: CommandSource, ctx: dict):
            if not source.is_player:
                source.reply('只有玩家才能使用此命令！')
                return
            PositionHandler(source).delete(ctx['name'])

    builder.arg('max', lambda n: Integer(n).at_min(1))
    builder.arg('count', lambda n: Integer(n).at_min(1))
    builder.arg('page', lambda n: Integer(n).at_min(1))
    builder.arg('value', Number)
    builder.arg('x', Number)
    builder.arg('y', Number)
    builder.arg('z', Number)
    builder.arg('dim', Integer)
    builder.arg('name', Text)
    builder.arg('target', Text)
    builder.arg('cmd', GreedyText)
    builder.arg('id', Text)

    builder.register(server)

def on_unload(server: PluginServerInterface):
    ChatEvent(server, None, type="info", msg='插件已卸载', log='插件已卸载', say=False).guide()

def on_info(server: PluginServerInterface, info: Info):
    if info.content is None or not settings.get('enable_tools', True):
        return

    if settings.get('enable_betterchat', True):
        BetterChat(server).Chat(info)

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
    config = server.load_config_simple('config.json', target_class=Config)
    settings = config.settings

class BaseHandler:
    def __init__(self, source: CommandSource):
        self.source = source
        self.server = source.get_server()
        self.player = source.player if source.is_player else None

class HereHandler(BaseHandler):
    @new_thread("Here")
    def execute(self):
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            self.source.reply('§cMinecraft Data API未启用，无法使用此功能！请联系管理员#106')
            return
        try:
            pos = api.get_player_coordinate(self.player)
            dim = api.get_player_dimension(self.player)
            x, y, z = round(pos.x), round(pos.y), round(pos.z)
        except Exception as e:
            self.source.reply(f'§c获取坐标时发生错误: {str(e)}')
            return

        x_n = round(x/8)
        y_n = y
        z_n = round(z/8)

        message = f"§a§u{self.player} §r在 "
        if dim == 0:
            message += f"[§2主世界:§a{x}  {y}  {z}§r]→ [§c下界:§6{x_n}  {y_n}  {z_n}§r]"
        elif dim == -1:
            message += f"[§c下界:§6{x}  {y}  {z}§r]→ [§2主世界:§a{x_n}  {y_n}  {z_n}§r]"
        elif dim == 1:
            message += f"[§5末地:§e{x}  {y}  {z}§r]"
        else:
            message += f"[§4未知维度:§c{x}  {y}  {z}§r]"

        ChatEvent(self.server, None, type="info", msg=message, log=f"[HerePlugin] {message}", say=True).guide()
        extra_msg = RTextList(
            RText('[', RColor.dark_gray),
            RText('Tools', RColor.dark_green),
            RText('] ', RColor.dark_gray),
            RText('[旁观TP坐标]', RColor.gold).h('Tools插件的TP功能').c(RAction.suggest_command, f'!tp {x} {y} {z}'),
            RText('   '),
            RText('[+H]', RColor.yellow, RStyle.bold).h('使用Carpet Org的高亮功能').c(RAction.run_command, f'/highlight {x} {y} {z}'),
            RText('   '),
            RText('[+C]', RColor.yellow, RStyle.bold).h('复制坐标').c(RAction.copy_to_clipboard, f'{x} {y} {z}')
        )
        self.server.broadcast(extra_msg)

class KillHandler(BaseHandler):
    def execute(self):
        self.server.execute(f'kill {self.player}')
        ChatEvent(self.server, None, type="info", msg=f'欸 {self.player} 你怎么似了啊？！', log=f"玩家 {self.player} 自杀", say=True).guide()

class PositionHandler(BaseHandler):
    def _load_config(self):
        return self.server.load_config_simple('config.json')

    def _save_config(self, config_data):
        self.server.save_config_simple(config_data, 'config.json')

    def _dimension_to_text(self, dimension_id):
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
        dimension_map = {
            0: 'minecraft:overworld',
            -1: 'minecraft:the_nether',
            1: 'minecraft:the_end',
            '0': 'minecraft:overworld',
            '-1': 'minecraft:the_nether',
            '1': 'minecraft:the_end'
        }
        return dimension_map.get(dimension_id, 'minecraft:overworld')

    def show_help(self):
        self.source.reply('§e!d 传送点管理§r')
        self.source.reply('§b!d list [页码] §r- 查看传送点列表')
        self.source.reply('§b!d tp <名称> §r- 传送到指定位置')
        self.source.reply('§b!d set <名称> §r- 保存当前位置')
        self.source.reply('§b!d del <名称> §r- 删除指定位置')

    def list_positions(self, page: int = 1, per_page: int = 5):
        config_data = self._load_config()
        positions = config_data.get('Position', {})

        if not positions:
            self.source.reply('§c没有保存的传送位置！')
            return

        items = list(positions.items())
        total_count = len(items)
        max_page = max(1, (total_count - 1) // per_page + 1)

        if not (1 <= page <= max_page):
            self.source.reply(RText(f'页码 {page} 超出范围 (1-{max_page})', RColor.gray).set_styles(RStyle.italic))
            page = max(1, min(page, max_page))

        self.source.reply(RTextList(
            RText('========== ', RColor.gray),
            RText('传送位置列表', RColor.gold),
            RText(' ==========', RColor.gray)
        ))
        self.source.reply(RTextList(
            RText('共有 ', RColor.gray),
            RText(str(total_count), RColor.yellow),
            RText(' 个位置', RColor.gray)
        ))

        start = (page - 1) * per_page
        for name, data in items[start:start + per_page]:
            location = data.get('location', '?')
            dimension = data.get('dimension', '?')
            by = data.get('by', '?')
            dim_text = self._dimension_to_text(dimension)

            name_text = RText(name, RColor.gold).h(f'位置名称: {name}')
            tp_button = RText('[传送]', RColor.green).h(f'点击传送到 {name}').c(RAction.run_command, f'!d tp {name}')
            del_button = RText('[删除]', RColor.red).h(f'点击删除 {name}').c(RAction.suggest_command, f'!d del {name}')

            self.source.reply(RTextList(
                name_text, RText(' - ', RColor.gray),
                RText(f'[{location}]', RColor.aqua), RText(' - ', RColor.gray),
                RText(dim_text, RColor.light_purple), RText(' - ', RColor.gray),
                RText(f'by {by}', RColor.yellow), RText(' ', RColor.gray),
                tp_button, RText(' ', RColor.gray), del_button
            ))

        prev_btn = RText('<-')
        if page > 1:
            prev_btn.set_color(RColor.green).h('上一页').c(RAction.run_command, f'!d list {page - 1}')
        else:
            prev_btn.set_color(RColor.dark_gray)

        next_btn = RText('->')
        if page < max_page:
            next_btn.set_color(RColor.green).h('下一页').c(RAction.run_command, f'!d list {page + 1}')
        else:
            next_btn.set_color(RColor.dark_gray)

        self.source.reply(RTextList(
            RText('---- ', RColor.gray), prev_btn, RText(' [', RColor.gray),
            RText(str(page), RColor.yellow), RText('/', RColor.gray),
            RText(str(max_page), RColor.yellow), RText('] ', RColor.gray),
            next_btn, RText(' ----', RColor.gray)
        ))

    def teleport(self, name: str):
        config_data = self._load_config()
        position_data = config_data.get('Position', {}).get(name, {})

        if not position_data:
            self.source.reply(f'§c未找到位置 "{name}"！')
            return

        pos_str = position_data.get('location')
        dimension_id = position_data.get('dimension')

        if not pos_str or dimension_id is None:
            self.source.reply('§c位置数据损坏！')
            return

        dimension = self._dimension_to_command(dimension_id)
        self.server.execute(f'execute in {dimension} run tp {self.player} {pos_str}')

        dim_text = self._dimension_to_text(dimension_id)
        self.source.reply(f'§a已将你传送到 §6{name} §a({dim_text})')

    @new_thread("SetPosition")
    def set_location(self, name: str):
        config_data = self._load_config()
        if name in config_data.get('Position', {}):
            self.source.reply(f'§c位置 "{name}" 已存在！请使用其他名称')
            return

        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            self.source.reply('§cMinecraft Data API未启用！')
            return

        try:
            dimension = api.get_player_dimension(self.player)
            location = api.get_player_coordinate(self.player)
            x, y, z = round(location.x), round(location.y), round(location.z)
            pos_str = f"{x} {y} {z}"

            config_data.setdefault('Position', {})
            config_data['Position'][name] = {
                'location': pos_str,
                'dimension': dimension,
                'by': self.player,
                'time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self._save_config(config_data)

            dim_text = self._dimension_to_text(dimension)
            self.source.reply(f'§a已保存位置 §6{name} §a: §e{x} {y} {z} §a在 §d{dim_text}')
        except Exception as e:
            self.source.reply(f'§c保存位置时发生错误: {str(e)}')

    def delete(self, name: str):
        perm = self.server.get_permission_level(self.player)
        required_perm = settings.get('position_permission_level', 2)
        if perm < required_perm:
            self.source.reply('§c你没有权限删除位置！')
            return

        config_data = self._load_config()
        if name in config_data.get('Position', {}):
            del config_data['Position'][name]
            self._save_config(config_data)
            self.source.reply(f'§a已删除位置 §6{name}')
        else:
            self.source.reply(f'§c未找到位置 "{name}"！')

class TpHandler(BaseHandler):
    def show_help(self):
        self.source.reply('§e!tp 旁观传送§r')
        self.source.reply('§b!tp <x> <y> <z> §r- 传送到指定坐标')
        self.source.reply('§b!tp <x> <z> §r- 传送到指定XZ坐标')
        self.source.reply('§b!tp <玩家> §r- 传送到指定玩家')
        self.source.reply('§b!tp <维度> §r- 传送到指定维度')

    def _check_gamemode(self):
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            return True
        perm = self.server.get_permission_level(self.player)
        if perm >= 3:
            return True
        gamemode = str(api.get_player_info(self.player, 'playerGameType'))
        if gamemode != '3':
            self.source.reply('§c你不是旁观模式，无法使用此指令！请切换到旁观模式后再试。')
            return False
        return True

    def _execute_teleport(self, x, y, z):
        api = self.server.get_plugin_instance('minecraft_data_api')
        player_dim = api.get_player_dimension(self.player)
        dimension_map = {0: 'minecraft:overworld', -1: 'minecraft:the_nether', 1: 'minecraft:the_end'}
        dimension = dimension_map.get(player_dim, 'minecraft:overworld')
        self.server.execute(f'execute in {dimension} run tp {self.player} {x} {y} {z}')

    def tp_xyz(self, x, y, z):
        if not self._check_gamemode():
            return
        self.source.reply(f"传送到 {x} {y} {z}")
        self._execute_teleport(x, y, z)

    def tp_xz(self, x, z):
        if not self._check_gamemode():
            return
        api = self.server.get_plugin_instance('minecraft_data_api')
        player_pos = api.get_player_coordinate(self.player)
        y = player_pos.y
        self.source.reply(f"传送到 {x} {y} {z}")
        self._execute_teleport(x, y, z)

    def tp_player(self, target: str):
        if not self._check_gamemode():
            return
        dim_map = {
            '主世界': ('minecraft:overworld', 0, 64, 0),
            '地狱': ('minecraft:the_nether', 0, 120, 0),
            '下界': ('minecraft:the_nether', 0, 120, 0),
            '下届': ('minecraft:the_nether', 0, 120, 0),
            '末地': ('minecraft:the_end', 0, 64, 0)
        }
        if target in dim_map:
            dimension, x, y, z = dim_map[target]
            self.server.execute(f'execute in {dimension} run tp {self.player} {x} {y} {z}')
        else:
            self.server.execute(f'tp {self.player} {target}')

class RestartHandler(BaseHandler):
    @new_thread("Restart")
    def execute(self):
        perm = self.server.get_permission_level(self.player)
        if perm < 3:
            self.source.reply('§c你没有权限重启服务器！')
            return
        ChatEvent(self.server, None, type="info", msg=f"由{self.player}执行的重启！", log=f"重启: {self.player}", say=True).guide()
        for i in range(10, -1, -1):
            ChatEvent(self.server, None, type="info", msg=f"服务器将在{i}秒后重启！", log=f"重启倒计时: {i}", say=True).guide()
            time.sleep(1)
        self.server.restart()

class RandomHandler(BaseHandler):
    def execute(self, max_val: int):
        number = random.randint(1, max_val)
        self.source.reply(f'§a随机数(1~{max_val}): §e{number}')

class FakePlayerHandler(BaseHandler):
    def show_help(self):
        self.source.reply('§e!p 假人管理§r')
        self.source.reply('§b!p <name> §r- 生成假人')
        self.source.reply('§b!p <name> <dim> <x> <y> <z> §r- 在指定位置生成假人')

    def spawn(self, name: str):
        self.server.execute(f'player {name} spawn')

    def spawn_at(self, name: str, dim: int, x, y, z):
        dim_map = {0: 'minecraft:overworld', -1: 'minecraft:the_nether', 1: 'minecraft:the_end'}
        dim_name = dim_map.get(dim, 'minecraft:overworld')
        self.server.execute(f'player {name} spawn at {x} {y} {z} facing 0 0 in {dim_name}')

class ManyPlayerHandler(BaseHandler):
    def show_help(self):
        self.source.reply('§e!mp 批量假人管理§r')
        self.source.reply('§b!mp spawn <count> §r- 批量生成假人')
        self.source.reply('§b!mp slow <count> §r- 慢速生成假人')
        self.source.reply('§b!mp kill <name> §r- 杀死假人')

    def spawn(self, count: int):
        perm = self.server.get_permission_level(self.player)
        if perm < 1 and count > 20:
            self.source.reply('§c你没有足够的权限创建超过20个假人！')
            return
        if perm < 2 and count > 50:
            self.source.reply('§c你没有足够的权限创建超过50个假人！')
            return
        for i in range(count):
            self.server.execute(f'player FakePlayer{i} spawn')

    @new_thread("SlowSpawn")
    def spawn_slow(self, count: int):
        perm = self.server.get_permission_level(self.player)
        if perm < 1:
            self.source.reply('§c你没有权限使用此命令！')
            return
        for i in range(count):
            self.server.execute(f'player FakePlayer{i} spawn')
            time.sleep(1)

    def kill(self, name: str):
        self.server.execute(f'player {name} kill')

    def run_cmd(self, cmd: str):
        for i in range(256):
            self.server.execute(f'player FakePlayer{i} {cmd}')

class ScaleHandler(BaseHandler):
    def set_scale(self, value):
        self.server.execute(f'attribute {self.player} minecraft:scale base set {value}')
        self.source.reply(f'§a成功将你的大小设置为 {value}！')

class ItemHLHandler(BaseHandler):
    def enable(self):
        self.server.execute('execute as @e[type=item] run data merge entity @s {Glowing:1b}')
        self.source.reply('§a所有掉落物已高亮，输入!uitemhl取消')

    def disable(self):
        self.server.execute('execute as @e[type=item] run data merge entity @s {Glowing:0b}')
        self.source.reply('§a所有掉落物高亮已取消，输入!itemhl开启')

class MusicHandler(BaseHandler):
    def show_help(self):
        helpmsg = "§e[Help] §r- §bMusic Plugin 帮助信息§r\n"
        helpmsg += "├┬─ §c!music p id <music_id> §r- 为所有玩家播放指定id的声音\n"
        helpmsg += "│├─ §c!music p name <music_name> §r- 为所有玩家播放指定唱片名称的音乐\n"
        helpmsg += "│└─ §c!music p stop §r- 停止所有玩家播放的音乐\n"
        helpmsg += "├─ §c!music §r- 显示帮助信息\n"
        helpmsg += "└─ §c!music stop §r- 停止当前播放的音乐"
        self.source.reply(helpmsg)

    def stop(self):
        self.server.execute(f'stopsound {self.player}')

    def stop_all(self):
        self.server.execute('stopsound @a')

    def play_name(self, name):
        global music_dict
        if name in music_dict:
            music_id = music_dict[name]
            self.server.execute(f'execute at @a run playsound {music_id} player @a')
        else:
            self.source.reply(f'§c未找到名为 {name} 的音乐！')

    def play_id(self, music_id):
        self.server.execute(f'execute at @a run playsound {music_id} player @a')

class BetterChat():
    def __init__(self, server: PluginServerInterface):
        self.server = server

    @new_thread("BetterChat")
    def Chat(self, info: Info):
        if not info.is_player:
            return
        if '@' not in info.content or info.player == 'Server':
            return
        if '@ ' in info.content:
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

class ChatEvent():
    def __init__(self, server: PluginServerInterface,
                 info = None,
                 type: str = None,
                 log: str = None,
                 msg: str = None,
                 say: bool = False):
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

    def guide(self):
        self.pack()
        if self.type == "info":
            if self.say:
                self.server.say(self.SendMsg)
            else:
                if self.info is not None and self.info.is_player:
                    self.server.tell(self.info.player, self.SendMsg)
            if self.SendLog is not None:
                self.server.logger.info(self.SendLog)
        elif self.type == "error":
            if self.say:
                self.server.say(self.SendMsg)
            else:
                if self.info is not None and self.info.is_player:
                    self.server.tell(self.info.player, self.SendMsg)
            if self.SendLog is not None:
                self.server.logger.error(self.SendLog)
        elif self.type == "warn":
            if self.say:
                self.server.say(self.SendMsg)
            else:
                if self.info is not None and self.info.is_player:
                    self.server.tell(self.info.player, self.SendMsg)
            if self.SendLog is not None:
                self.server.logger.warning(self.SendLog)
        elif self.type == "help":
            if self.SendLog is not None:
                self.server.logger.info(self.SendLog)
