import bottle

from server_communication import ConfigSyncHandler

NAME = 'Easy Parental Control'
config = bottle.Bottle()


@config.route('/config')
def config_list():
    ful_configs = ''
    for i, c in enumerate(ConfigSyncHandler.configs.configs):
        for line in str(c).replace('ClientConfiguration(', '').split(', '):
            if '=' in line:
                key, value = line.split('=')
                ful_configs += f'<br>{key}=<input type="text" name="{i}{key}" value="{value}"/>'
            else:
                ful_configs += f', {line}'
        ful_configs += f'<br><input type="submit" name="remove{i}" value="remove"/>'
    return f'<meta http-equiv="refresh" content="60"><H1>{NAME}</H1><form action="/modify_config" method="post">{ful_configs}<input type="submit"/></form>'


@config.post('/modify_config')
def modify_config():
    for i, c in enumerate(ConfigSyncHandler.configs.configs):
        if bottle.request.forms.get(f'remove{i}'):
            ConfigSyncHandler.configs.configs.remove(c)
            break
        for line in str(c).replace('ClientConfiguration(', '').split(', '):
            if '=' in line:
                key, value = line.split('=')
                value = bottle.request.forms.get(f'{i}{key}').replace('\'', '')
                if isinstance(ConfigSyncHandler.configs.configs[i].__dict__[key], str) and ConfigSyncHandler.configs.configs[i].__dict__[key] != value:
                    ConfigSyncHandler.configs.configs[i].__dict__[key] = value
    bottle.redirect("/config")
