from signin import *
from signup import *
from list_chat import *
from chat_message import *

class Router:
    def __init__(self, page, cc):
        self.page = page
        self.routes = {
            "/sign-in": SignInView(page, cc),
            "/sign-up": SignUpView(page, cc),
            "/chat": ListChatView(page, cc),
            "/msgchat": ChatMessageView(page, cc)
        }
        self.body = Container(content=self.routes['/sign-in'])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()