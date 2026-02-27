from mcdreforged.api.all import *
from mcdreforged.api.rtext import RText, RTextList, RColor, RAction
from .utils import ChatEvent


class Here:
    def __init__(self, server: PluginServerInterface, info: Info):
        self.server = server
        self.info = info
    
    @new_thread("Here")
    def GetPos(self):
        if not self.info.source.is_player:
            return
            
        api = self.server.get_plugin_instance('minecraft_data_api')
        if api is None:
            ChatEvent(self.server, self.info, type="error", msg='§cMinecraft Data API未启用，无法使用此功能！请联系管理员#106', log='Minecraft Data API 未启用', say=False).guide()
            return
        try:
            pos = api.get_player_coordinate(self.info.source.player)
            dim = api.get_player_dimension(self.info.source.player)
            x, y, z = pos.x, pos.y, pos.z
        except Exception as e:
            ChatEvent(self.server, self.info, type="error", msg=f'§c获取坐标时发生错误: {str(e)}', log=f'获取坐标错误: {e}', say=False).guide()
            return
        
        x = round(x)
        y = round(y)
        z = round(z)
        
        message = f"§a§u{self.info.source.player} §r在 "
        if dim == 0:
            message += f"[§2主世界:§a{x}  {y}  {z}§r]→ [§c下界:§6{round(x/8)}  {y}  {round(z/8)}§r]"
        elif dim == -1:
            message += f"[§c下界:§6{x}  {y}  {z}§r]→ [§2主世界:§a{x*8}  {y}  {z*8}§r]"
        elif dim == 1:
            message += f"[§5末地:§e{x}  {y}  {z}§r]"
        else:
            message += f"[§4未知维度:§c{x}  {y}  {z}§r]"
            
        ChatEvent(self.server, None, type="info", msg=message, log=f"[HerePlugin] {message}", say=True).guide()
        
        buttons = RTextList(
            RText('[', RColor.dark_gray),
            RText('Tools', RColor.dark_green),
            RText('] ', RColor.dark_gray),
            RText('[旁观TP坐标]', RColor.gold)
                .h('Tools插件的TP功能')
                .c(RAction.suggest_command, f'!tp {x} {y} {z}'),
            RText('   '),
            RText('[+H]', RColor.yellow).set_bold(True)
                .h('使用Carpet Org的高亮功能')
                .c(RAction.run_command, f'/highlight {x} {y} {z}'),
            RText('   '),
            RText('[+C]', RColor.yellow).set_bold(True)
                .h('复制坐标')
                .c(RAction.copy_to_clipboard, f'{x} {y} {z}')
        )
        
        self.server.tell(self.info.source.player, buttons)
