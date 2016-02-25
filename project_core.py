#!/usr/bin/env python
import ramona


class ConsoleApp(ramona.console_app):
    pass

if __name__ == '__main__':
    app = ConsoleApp(configuration='./project_core.conf')
    app.run()
