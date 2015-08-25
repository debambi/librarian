from .utils import close_databases, init_databases


def component_loaded(supervisor, component, config):
    supervisor.config.setdefault('database.sources', {})
    pkg_name = component['pkg_name']
    if pkg_name not in supervisor.config['database.sources']:
        db_names = config.pop('database.names', None)
        if db_names:
            supervisor.config['database.sources'][pkg_name] = db_names


def init_begin(supervisor):
    supervisor.exts.databases = init_databases(supervisor.config)


def shutdown(supervisor):
    close_databases(supervisor.exts.databases)


def immediate_shutdown(supervisor):
    close_databases(supervisor.exts.databases)
