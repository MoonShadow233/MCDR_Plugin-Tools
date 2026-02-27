from mcdreforged.api.all import *
import random
from .utils import ChatEvent


class Random:
    def __init__(self, server: PluginServerInterface):
        self.server = server

    def ListNumber(self, info: Info):
        if not info.source.is_player or not info.content.split()[0] == '!l':
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
