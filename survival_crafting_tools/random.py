from mcdreforged.api.all import *
import random
from .utils import ChatEvent
from .tools import get_command_source, get_content


class Random:
    def __init__(self, server: PluginServerInterface):
        self.server = server

    def ListNumber(self, source):
        cs = get_command_source(source)
        if cs is None or not cs.is_player:
            return
        try:
            parts = get_content(source).split()
            if len(parts) < 2:
                num = random.randint(1, 10)
                ChatEvent(self.server, source, type="info", msg=f'§a[骰子] §r- §b生成的数为: §e{num}', log=f"骰子: {num}", say=True).guide()
                return
            
            range_str = parts[1]
            if '-' not in range_str:
                ChatEvent(self.server, source, type="error", msg='§c[骰子] §r- §c格式错误！正确格式：!l 1-10', log='骰子 格式错误', say=False).guide()
                return
                
            range1 = int(range_str.split('-')[0])
            range2 = int(range_str.split('-')[1])
            
            if range1 > range2:
                ChatEvent(self.server, source, type="error", msg='§c[骰子] §r- §c范围错误：前一个数必须小于后一个数！', log='骰子 范围错误', say=False).guide()
                return
            elif range1 == range2:
                ChatEvent(self.server, source, type="error", msg='§c[骰子] §r- §c范围错误：两个数不能相等！', log='骰子 范围错误', say=False).guide()
                return
            
            num = random.randint(range1, range2)
            ChatEvent(self.server, source, type="info", msg=f'§a[骰子] §r- §b生成的数为: §e{num}', log=f"骰子: {num}", say=True).guide()
        except Exception as e:
            ChatEvent(self.server, source, type="error", msg=f'§c[骰子] §r- §c发生错误: {str(e)}', log=f"骰子错误: {e}", say=False).guide()


def register(server: PluginServerInterface):
    def on_random_command(source):
        Random(server).ListNumber(source)
    server.register_command(Literal('!l').runs(on_random_command))
