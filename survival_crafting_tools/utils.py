from mcdreforged.api.all import *


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


class ChatEvent:
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
                if self.info and self.info.source.is_player:
                    self.server.tell(self.info.source.player, send_msg)
                    
        if send_log is not None:
            self.server.logger.info(send_log)

    def help(self):
        if not self.info or not getattr(self.info.source, "is_player", False) or self.info.content != '!tools':
            return
            
        helpmsg = "§e[Help] §r- "
        helpmsg += "§bTools Plugin 帮助信息§r\n"
        helpmsg += "├─ §c!h §r- 发送当前位置信息\n"
        helpmsg += "├─ §c!here §r- 发送当前位置信息\n"
        helpmsg += "├─ §c!kill §r- 自杀\n"
        helpmsg += "├─ §c!restart §r- 重启服务器（需要权限）\n"
        helpmsg += "├─ §c!l §r- 投骰子\n"
        helpmsg += "├─ §c!sc §r- 玩家大小缩放\n"
        helpmsg += "└─ §c!music §r- 音乐播放帮助"
        self.server.tell(self.info.source.player, helpmsg)
