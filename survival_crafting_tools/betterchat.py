from mcdreforged.api.all import *
from .utils import ChatEvent


class BetterChat:
    def __init__(self, server: PluginServerInterface):
        self.server = server
    
    @new_thread("BetterChat")
    def process_chat(self, info: Info):
        """处理聊天消息中的@功能"""
        if not info.is_player or '@' not in info.content:
            return
        if 'Command' in info.content:
            return
        if info.player == "Server":
            return
        content = info.content
        player = info.player
        words = content.split()
        
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            ChatEvent(self.server, info, type="error", 
                     msg='§cMinecraft Data API未启用，无法使用@功能', 
                     log='Minecraft Data API 未启用', 
                     say=False).guide()
            return
            
        try:
            online_players = api.get_server_player_list().players
        except Exception as e:
            ChatEvent(self.server, info, type="error", 
                     msg=f'§c获取玩家列表失败: {str(e)}', 
                     log=f'获取玩家列表失败: {e}', 
                     say=False).guide()
            return
        
        for i, word in enumerate(words):
            if not word.startswith('@'):
                continue
            
            if word == '@' and i + 1 < len(words):
                target = words[i + 1]
                self._process_target(player, target, online_players)
            elif len(word) > 1:
                target = word[1:]
                self._process_target(player, target, online_players)
    
    def _process_target(self, sender: str, target: str, online_players: list):
        """处理@目标"""
        if target == 'a':
            self._at_all(sender, online_players)
            return
            
        if target in online_players:
            self._at_player(sender, target)
        else:
            ChatEvent(self.server, None, type="error", 
                     msg=f'§c玩家 §e{target} §c不在线', 
                     log=f"玩家不在线: {target}", 
                     say=True).guide()
    
    def _at_all(self, sender: str, players: list):
        """@所有人"""
        if not players:
            return
            
        ChatEvent(self.server, None, type="info", 
                 msg=f'§6{sender} §a@了所有人', 
                 log=f"{sender} @a", 
                 say=True).guide()
        
        self.server.execute('title @a title ""')
        self.server.execute(f'title @a subtitle [{{"text":"{sender}","color":"aqua"}},{{"text":"@了所有人","color":"blue"}}]')
        self.server.execute('playsound minecraft:entity.player.levelup master @a')
    
    def _at_player(self, sender: str, target: str):
        """@指定玩家"""
        ChatEvent(self.server, None, type="info", 
                 msg=f'§6{sender} §a@了 §b{target}', 
                 log=f"{sender} @{target}", 
                 say=True).guide()
        
        self.server.execute('title @a title ""')
        self.server.execute(f'title {target} subtitle [{{"text":"{sender}","color":"aqua"}},{{"text":"@了你","color":"blue"}}]')
        self.server.execute(f'playsound minecraft:entity.player.levelup master {target}')
