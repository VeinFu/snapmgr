# -*- coding: utf-8 -*-

from snapmgr import app, scheduler

scheduler.init_app(app)
scheduler.start()
#app.run('0.0.0.0', port='8909', debug=True)
