from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('play', '/{room}')
    config.add_route('userInput', '/{room}/play')
    config.add_route('polling', '/{room}/polling')
    config.scan()
    return config.make_wsgi_app()
