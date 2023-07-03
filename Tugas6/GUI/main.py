from router import *
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'BE'))
import chat_cli

def main(page : Page):
    # Dimension
    page.title = "ChatKui"
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.bgcolor = '#1B202D'
    page.fonts = {
        "Poppins": "fonts/Poppins/Poppins-Bold.ttf",
        "Mulish": "fonts/Mulish/Mulish-VariableFont_wght.ttf"
    }

    try:
        ip, port = str(sys.argv[1]), int(sys.argv[2])
    except:
        ip, port = '127.0.0.1', 8889

    cc = chat_cli.ChatClient(ip, port)

    myRouter = Router(page, cc)
    page.on_route_change = myRouter.route_change

    page.add(myRouter.body)
    page.update()

if __name__ == "__main__":
    flet.app(port=8550, target=main, assets_dir='assets', view=WEB_BROWSER)