import bottle

from server_communication import ConfigSyncHandler

NAME = 'Easy Parental Control'
home = bottle.Bottle()


@home.route('/')
def index():
    short_config = ''
    for i, c in enumerate(ConfigSyncHandler.configs.configs):
        short_config += f'''
            <form action="/modify_time_left" method="post"><font size="10">{c.user if c.user else c.client_ip}:\t{c.time_left_min}</font>
                <input name="{i}+10" value="+10" type="submit" style="font-size:50px"/>
                <input name="{i}-10" value="-10" type="submit" style="font-size:50px"/>
                <input name="{i}BAN" value="BAN" type="submit" style="font-size:50px"/>
            </form>'''
    return f'<meta http-equiv="refresh" content="60"><H1>{NAME}</H1>{short_config}'


@home.post('/modify_time_left')
def add_time():
    for i, c in enumerate(ConfigSyncHandler.configs.configs):
        if bottle.request.forms.get(f'{i}+10'):
            c.time_left_today += 600
        elif bottle.request.forms.get(f'{i}-10'):
            c.time_left_today -= 600
        elif bottle.request.forms.get(f'{i}BAN'):
            c.time_left_today = 0
    bottle.redirect("/")
