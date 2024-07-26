from mcdreforged.api.all import *

class Config(Serializable):
	default_distance: int = 32
	max_distance: int = 256

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()
config = Config.get_default()

@new_thread(PLUGIN_METADATA.name + ' - adsorb_item_default')
def adsorb_item_default(source: CommandSource, context: dict):
	if not source.is_player:
		source.reply(RText('指令只允许玩家使用', color=RColor.red))
		return

	tp_item_to_player(source,config.default_distance)


@new_thread(PLUGIN_METADATA.name + ' - adsorb_item')
def adsorb_item(source: CommandSource, context: dict):
	if not source.is_player:
		source.reply(RText('指令只允许玩家使用', color=RColor.red))
		return

	if(context['distance']>config.max_distance):
		source.reply(RText('指定范围过大，上限为{}格半径'.format(config.max_distance), color=RColor.red))
		return
	elif(context['distance']<1):
		source.reply(RText('指定范围过小，下限为1格半径', color=RColor.red))
		return

	tp_item_to_player(source,context['distance'])


def tp_item_to_player(source: CommandSource, distance: Integer):
	source.get_server().execute('execute as {} at {} run tp @e[type=item,distance=..{}] @s'.format(source.player,source.player,distance))
	source.reply(RText('已传送附近{}格半径内的掉落物到脚下'.format(distance), color=RColor.green))
	

#def on_info(server: PluginServerInterface, info: Info):
#    if info.is_from_server and not info.is_player:
#        server.logger.info('命令回显:[{}]'.format(info.content))

def on_load(server: PluginServerInterface, prev):
	global config
	config = server.load_config_simple(target_class=Config)

	if(config.max_distance<1):
		server.logger.error('配置文件最大距离指定范围过小，下限为1格半径，请修改配置文件重载插件')
		return

	if(config.default_distance>config.max_distance):
		server.logger.error('配置文件默认距离指定范围过大，上限为{}格半径，请修改配置文件重载插件'.format(config.max_distance))
		return
	elif(config.default_distance<1):
		server.logger.error('配置文件默认距离指定范围过小，下限为1格半径，请修改配置文件并重载插件')
		return

	server.register_help_message('!!abi [距离(可选)]', '吸附一定球形范围内的附近掉落物，默认距离为{}格半径，最大距离为{}格半径'.format(config.default_distance,config.max_distance))
	server.register_command(Literal('!!abi').then(Integer('distance').runs(adsorb_item)).runs(adsorb_item_default))
