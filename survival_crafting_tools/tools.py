from mcdreforged.api.all import *


def get_command_source(source):
    """
    从各种来源获取 CommandSource
    
    :param source: 可以是 CommandSource, CommandContext, Info 或其他对象
    :return: CommandSource 或 None
    """
    if source is None:
        return None
    if hasattr(source, 'is_player') and hasattr(source, 'player'):
        return source
    if hasattr(source, 'get_command_source'):
        return source.get_command_source()
    if hasattr(source, 'source'):
        return source.source
    return None


def get_player_name(source):
    """
    获取玩家名称
    
    :param source: 任意来源对象
    :return: 玩家名称或 None
    """
    cs = get_command_source(source)
    if cs is not None and cs.is_player:
        return cs.player
    if hasattr(source, 'player'):
        return source.player
    return None


def get_content(source):
    """
    获取命令内容
    
    :param source: 任意来源对象
    :return: 命令内容字符串
    """
    if hasattr(source, 'content'):
        return source.content
    if hasattr(source, 'command'):
        return source.command
    return ''


def is_player(source):
    """
    检查来源是否为玩家
    
    :param source: 任意来源对象
    :return: bool
    """
    cs = get_command_source(source)
    if cs is not None:
        return cs.is_player
    if hasattr(source, 'is_player'):
        return source.is_player
    return False


def dimension_to_text(dimension_id):
    """
    维度ID转显示文本
    
    :param dimension_id: 维度ID (0=主世界, -1=下界, 1=末地)
    :return: 维度中文名称
    """
    dimension_map = {
        0: '主世界',
        -1: '下界',
        1: '末地',
    }
    return dimension_map.get(dimension_id, f'未知({dimension_id})')


def dimension_to_command(dimension_id):
    """
    维度ID转命令维度名
    
    :param dimension_id: 维度ID
    :return: Minecraft 命令使用的维度名称
    """
    dimension_map = {
        0: 'minecraft:overworld',
        -1: 'minecraft:the_nether',
        1: 'minecraft:the_end',

    }
    return dimension_map.get(dimension_id, 'minecraft:overworld')
