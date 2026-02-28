from mcdreforged.api.all import *
import time
from .utils import ChatEvent
from .tools import get_command_source, get_player_name, get_content


class ManyPlayer:
    def __init__(self, server: PluginServerInterface):
        self.server = server

    @new_thread("SpawnPlayer")
    def SpawnPlayer(self, source, player_num: int, sleep: float = 0):
        player_name = get_player_name(source)
        try:
            for i in range(player_num):
                self.server.execute(f'execute as {player_name} at @s run player FakePlayer{i} spawn')
                
                if sleep > 0:
                    time.sleep(sleep)
                    
            ChatEvent(self.server, source, type="info", msg=f'§a成功在当前位置生成{player_num}个假人', log=f'生成假人: {player_num}个', say=True).guide()
        except Exception as e:
            ChatEvent(self.server, source, type="error", msg=f'§c生成假人时发生错误: {str(e)}', log=f'生成假人错误: {e}', say=False).guide()

    @new_thread("ManyPlayer")
    def ManyPlayer(self, source):
        cs = get_command_source(source)
        if cs is None or not cs.is_player:
            return
        
        args = get_content(source).split()
        
        if len(args) < 2:
            ChatEvent(self.server, source, type="error", msg='§c语法错误：正确语法!mp <kill|cmd|spawn> <数量>', log='!mp 语法错误', say=False).guide()
            return
        
        if args[1] == 'kill':
            for i in range(256):
                self.server.execute(f'kill FakePlayer{i}')
            ChatEvent(self.server, source, type="info", msg='§a已清除所有假人', log='清除假人', say=True).guide()
            return
            
        elif args[1] == 'cmd':
            if len(args) < 3:
                ChatEvent(self.server, source, type="error", msg='§c语法错误：!mp cmd <命令>', log='!mp cmd 语法错误', say=False).guide()
                return
            cmd = ' '.join(args[2:])
            for i in range(256):
                self.server.execute(f'player FakePlayer{i} {cmd}')
            ChatEvent(self.server, source, type="info", msg=f'§a已对所有假人执行命令: {cmd}', log=f'假人批量命令: {cmd}', say=True).guide()
            return
            
        elif args[1] == 'spawn':
            if len(args) < 3:
                ChatEvent(self.server, source, type="error", msg='§c语法错误：!mp spawn <数量>', log='!mp spawn 参数不足', say=False).guide()
                return
                
            try:
                player_num = int(args[2])
            except ValueError:
                ChatEvent(self.server, source, type="error", msg='§c玩家数量必须是一个整数！', log='!mp 参数错误', say=False).guide()
                return
            
            player_name = get_player_name(source)
            try:
                permission_level = self.server.get_permission_level(player_name)
            except:
                permission_level = 0
                
            if permission_level < 1 and player_num > 20:
                ChatEvent(self.server, source, type="error", msg='§c你没有足够的权限创建超过20个假人！', log='权限不足', say=False).guide()
                return
            elif permission_level < 2 and player_num > 50:
                ChatEvent(self.server, source, type="error", msg='§c你没有足够的权限创建超过50个假人！', log='权限不足', say=False).guide()
                return
            elif player_num > 256:
                ChatEvent(self.server, source, type="error", msg='§c最多只能创建256个假人！', log='假人数量超限', say=False).guide()
                return
                
            self.SpawnPlayer(source, player_num, sleep=0)
        else:
            ChatEvent(self.server, source, type="error", msg='§c未知的子命令！可用: kill, cmd, spawn', log='!mp 未知子命令', say=False).guide()


def register(server: PluginServerInterface):
    def on_manyplayer_command(source):
        ManyPlayer(server).ManyPlayer(source)
    server.register_command(Literal('!mp').runs(on_manyplayer_command))
