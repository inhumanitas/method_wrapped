# coding: utf-8
import json

import tornado.ioloop
import tornado.web
import tornado.gen

from rest_method.db import init_db, User, DB
from rest_method.method_lib import method


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", BenefitHandler),
            (r"/calc", BenefitHandler),
            (r"/login", LoginHandler),
        ]

        settings = dict(
            cookie_secret='tests',
            login_url="/login",
            template_path='templates',
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # Have one global connection.
        self.db = DB


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            return None
        return User.get(int(user_id))


class BenefitHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return

        self.render('params.html')

    @tornado.web.authenticated
    @tornado.web.asynchronous
    async def post(self, *args, **kwargs):
        try:
            benefit_type = int(self.get_argument('benefitType'))
            a = int(self.get_argument('a')) or 1
            b = int(self.get_argument('b')) or 1
            c = int(self.get_argument('c')) or 1
            params = json.loads(self.get_argument('params', '{}')) or {}
        except ValueError:
            raise tornado.web.HTTPError(status_code=400,
                                        reason='Params error')

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        res = await method.method(self.current_user,
                                  benefit_type, *(a, b, c), **params)
        print(self.current_user, res)
        self.write(str(res))
        self.finish()


class LoginHandler(BaseHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        login = self.get_argument("login")
        password = self.get_argument("password")
        user = User.get_authenticated(login, password)

        if user:
            self.set_secure_cookie("user_id", str(user.id))
            self.redirect("/")
        else:
            self.write('Wrong login\password pair')


def make_app():
    application = Application()
    return application


def main():
    init_db()

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
