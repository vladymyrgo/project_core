from tornado.options import define


# Django
define('django', default='http://127.0.0.0:8000', type=str)


# Redis
define('REDIS_HOST', default='localhost', type=str)
define('REDIS_PORT', default=6379, type=int)
define('REDIS_DB', default=7, type=int)


# Tornado
define('port', default=9000, help="run on the given port", type=int)
define('host', default='localhost', help='run on a given host name', type=str)
define('autoreload', default=False, help="enable autoreload after changing sources", type=bool)
