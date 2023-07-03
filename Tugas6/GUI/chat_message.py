import json

import flet as ft

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="center"
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold", color="white"),
                        ft.Container(
                            bgcolor="#7A8194", 
                            padding=8, 
                            content= ft.Text(message.text, selectable=True, color="white"),
                            border_radius=4,
                            )
                    ],
                    tight=True,
                   
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def ChatMessageView(page, cc):
    def send_message_click(type):
        if type == "send":
            j = new_message.value.split(" ")
            command = j[0].strip()
            if command == "FILE":
                realm_id = cc.realm_id
                receiver = cc.receiver
                filepath = j[1].strip()
                protocol = "sendprivatefilerealm " + realm_id + " " + receiver + " " + filepath
                print(protocol)
                print(cc.proses(protocol))
                message = Message(cc.username, new_message.value, "chat_message")
                m = ChatMessage(message)
                chat.controls.append(m)
                new_message.value=""
                page.update()
            else:
                realm_id = cc.realm_id
                receiver = cc.receiver
                protocol = "sendprivaterealm " + realm_id + " " + receiver + " " + new_message.value
                print(protocol)
                print(cc.proses(protocol))
                message = Message(cc.username, new_message.value, "chat_message")
                m = ChatMessage(message)
                chat.controls.append(m)
                new_message.value=""
                page.update()

        elif type == "refresh":
            realm_id = cc.realm_id
            protocol = "inboxrealm " + realm_id
            data = cc.proses(protocol)
            message = Message(realm_id, data, "chat_message")
            m = ChatMessage(message)
            chat.controls.append(m)
            page.update()

    new_message = ft.TextField(
        hint_text="Write a message...(To send file: 'FILE /path')",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        color="white",
        bgcolor="#7A8194",
        on_submit=lambda e: send_message_click("send"),
    )
    submit_row = ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.REFRESH_ROUNDED,
                    tooltip="Refresh",
                    on_click=lambda e : send_message_click("refresh"),
                ),
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=lambda e: send_message_click("send"),
                ),
            ]
        )
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    chatBox = ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
            bgcolor="#3D4354"
        )
    
    msg_container = ft.Container(
        content= submit_row,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=5,
        # width=1600,
        # height=900,
        padding=10,
        # expand=True,
        bgcolor="#ffffff"
    )
    msg_column = ft.Column(
        controls=[chatBox,msg_container],
        height=720,
        alignment=ft.MainAxisAlignment.START,
    )
    return ft.Container(
        content=msg_column
    )
            
                
        
       
    
        
    