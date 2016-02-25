import tornado.ioloop
import tornado.web
from tornado.options import (options, parse_command_line)

from api.urls import urlpatterns

import defaults


if __name__ == "__main__":
    parse_command_line()

    application = tornado.web.Application(urlpatterns, autoreload=options.autoreload)

    application.listen(options.port, address=options.host)
    print 'Server is running at http://%s:%d/' % (options.host, options.port)
    print 'Quit the server with CONTROL-C.'
    tornado.ioloop.IOLoop.instance().start()
