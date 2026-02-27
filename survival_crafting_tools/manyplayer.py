from mcdreforged.api.all import *
import time
from .utils import ChatEvent


class ManyPlayer:
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
                self.server.execute(f'execute as {info.source.player} at @s run player FakePlayer{i} spawn')
                
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
        if not info.source.is_player or not info.content.startswith('!mp'):
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
                permission_level = self.server.get_permission_level(info.source.player)
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
        else:
            ChatEvent(self.server, info, type="error", msg='§c未知的子命令！可用: kill, cmd, spawn', log='!mp 未知子命令', say=False).guide()
