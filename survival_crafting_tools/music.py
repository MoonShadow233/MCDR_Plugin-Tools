from mcdreforged.api.all import *
from .utils import ChatEvent, music_dict


class Music:
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server
        self.info = info
        
    def help(self):
        helpmsg = "§e[Help] §r- "
        helpmsg += "§bMusic Plugin 帮助信息§r\n"
        helpmsg += "├┬─ §c!music p id <音乐ID> §r- 为所有玩家播放指定ID的音乐\n"
        helpmsg += "│├─ §c!music p name <音乐名称> §r- 为所有玩家播放指定名称的音乐\n"
        helpmsg += "│└─ §c!music p stop §r- 停止所有玩家播放的音乐\n"
        helpmsg += "├─ §c!music stop §r- 停止当前播放的音乐\n"
        helpmsg += "└─ §c!music §r- 显示帮助信息"
        ChatEvent(self.server, self.info, type="info", msg=helpmsg, log=None, say=False).guide()

    def PlayMusic(self):
        if not self.info.source.is_player or not self.info.content.startswith('!music'):
            return
            
        args = self.info.content.split()
        if len(args) < 2:
            self.help()
            return
            
        if args[1] == 'stop':
            self.server.execute(f'stopsound {self.info.source.player}')
            ChatEvent(self.server, self.info, type="info", msg='§a已停止播放音乐', log=f'停止音乐: {self.info.source.player}', say=False).guide()
            return
            
        if args[1] == 'p':
            if len(args) < 3:
                self.help()
                return
                
            if args[2] == 'stop':
                self.server.execute('stopsound @a')
                ChatEvent(self.server, self.info, type="info", msg='§a已停止所有玩家播放的音乐', log='停止所有音乐', say=False).guide()
                return
                
            if len(args) < 4:
                self.help()
                return
                
            if args[2] == 'name':
                music_name = args[3]
                if music_name not in music_dict:
                    ChatEvent(self.server, self.info, type="warn", msg=f"§c未找到名为 {music_name} 的音乐！可用音乐：{music_dict.keys()}...", log=f"未找到音乐: {music_name}", say=False).guide()
                    return
                music_id = music_dict[music_name]
                self.server.execute(f'execute as @a at @s run playsound {music_id} ui @a ~ ~ ~ 1 1 1')
                ChatEvent(self.server, self.info, type="info", msg=f'§a正在为所有玩家播放: {music_name}', log=f'播放音乐: {music_name}', say=False).guide()
                
            elif args[2] == 'id':
                music_id = args[3]
                self.server.execute(f'execute as @a at @s run playsound {music_id} ui @a ~ ~ ~ 1 1 1')
                ChatEvent(self.server, self.info, type="info", msg=f'§a正在为所有玩家播放音乐ID: {music_id}', log=f'播放音乐ID: {music_id}', say=False).guide()
            else:
                self.help()
                return
        else:
            self.help()
            return
