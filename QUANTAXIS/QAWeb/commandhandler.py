
import json
import tornado
import os
import subprocess
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler
from QUANTAXIS.QAWeb.basehandles import QABaseHandler, QAWebSocketHandler


class CommandHandler(QABaseHandler):
    def get(self):
        try:
            command = self.get_argument('command')
            # print(command)
            res = os.popen(command)
            # print(res.read())
            self.write({'result': res.read()})
        except:
            self.write({'result': 'wrong'})


if __name__ == "__main__":

    app = Application(
        handlers=[
            (r"/test",  CommandHandler),
        ],
        debug=True
    )
    app.listen(8011)
    tornado.ioloop.IOLoop.current().start()
