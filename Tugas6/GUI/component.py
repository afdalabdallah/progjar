from flet import *

import time
from math import pi

class HyperLink(UserControl):
    def __init__(self, name, font, route, page):
        self.name = name
        self.font = font
        self.route = route
        self.page = page
        super().__init__()

    def change_route(self, e):
        self.page.route = self.route
        self.page.update()

    def highlight_link(self, e):
        e.control.style.color = colors.BLUE
        e.control.update()

    def unhighlight_link(self, e):
        e.control.style.color = None
        e.control.update()

    def build(self):
        return Text(
            disabled=False,
            spans=[
                TextSpan(
                    self.name,
                    TextStyle(
                        decoration=TextDecoration.UNDERLINE,
                        size=15,
                        font_family=self.font
                    ),
                    on_click=lambda e: self.change_route(e),
                    on_enter=lambda e: self.highlight_link(e),
                    on_exit=lambda e: self.unhighlight_link(e),
                ),
            ],
        )

class Button(UserControl):
    def __init__(self, btn_name, route, type, page, cc):
        self.cc = cc
        self.btn_name = btn_name
        self.route = route
        self.type = type
        self.page = page
        super().__init__()

    def submit(self, e):
        if self.type == "SignIn":
            email = (self.page.controls[0].content.content.controls[3].controls[4].controls[0].content.controls[1].value)  # Email
            password = (self.page.controls[0].content.content.controls[3].controls[7].controls[0].content.controls[1].value) # Password
            protocol = "auth " + email + " " + password
            if email == "" or password == "":
                return
            self.cc.proses(protocol)
        elif self.type == "SignUp":
            fullname = (self.page.controls[0].content.content.controls[3].controls[3].controls[0].content.controls[1].value)  # Email
            email = (self.page.controls[0].content.content.controls[3].controls[5].controls[0].content.controls[1].value)  # Email
            password = (self.page.controls[0].content.content.controls[3].controls[8].controls[0].content.controls[1].value)  # Password
            protocol = "register " + email + " " + password + " " + fullname + " Indonesia"
            if fullname == "" or email == "" or password == "":
                return
            self.cc.proses(protocol)
        elif self.type == "Logout":
            protocol = "logout"
            self.cc.proses(protocol)

        self.page.route = self.route
        self.page.update()

    def build(self):
        return Container(
            content=ElevatedButton(
                content=Text(
                    self.btn_name,
                    size=16,
                    weight="bold",
                    font_family="Consolas"
                ),
                style=ButtonStyle(
                    shape={
                        "": RoundedRectangleBorder(radius=8)
                    },
                    color={
                        "": "black"
                    },
                    bgcolor={
                        "": "#7df6dd"
                    }
                ),
                height=42,
                width=320,
                on_click=self.submit,
            )
        )

class AnimationBox(UserControl):
    def __init__(self, border_color, bg_color, rotate_angle):
        self.border_color = border_color
        self.bg_color = bg_color
        self.rotate_angle = rotate_angle
        super().__init__()

    def build(self):
        # Rotation Boxes
        return Container(
            width=48,
            height=48,
            border=border.all(2.5, self.border_color),
            bgcolor=self.bg_color,
            border_radius=2,
            rotate=transform.Rotate(
                self.rotate_angle,
                alignment.center
            ),
            animate_rotation=animation.Animation(700, "easeInOut")
        )

class InputField(UserControl):
    def __init__(self, bg_color, icon_name, text_hint, hide, function_emails):
        self.icon_name = icon_name
        self.bg_color = bg_color
        self.text_hint = text_hint
        self.hide = hide
        self.function_emails = function_emails
        super().__init__()

    def return_email_prefix(self, e):
        email = self.controls[0].content.controls[1].value
        if e.control.data in email:
            pass
        else:
            self.controls[0].content.controls[1].value += e.control.data
            self.controls[0].content.controls[2].offset = transform.Offset(0.5, 0)
            self.controls[0].content.controls[2].opacity = 0
            self.update()

    def prefix_email_containers(self):
        email_labels = ["@kelompok5.com", "@kelompok6.com", "@kelompok7.com"]
        label_title = ["KEL5", "KEL6", "KEL7"]
        __ = Row(
            spacing=1,
            alignment=MainAxisAlignment.END
        )
        for index, label in enumerate(email_labels):
            __.controls.append(
                Container(
                    width=45,
                    height=30,
                    alignment=alignment.center,
                    data=label,
                    on_click= lambda e: self.return_email_prefix(e),
                    content=Text(
                        label_title[index],
                        size=9,
                        weight="bold",
                        font_family="Consolas"
                    )
                )
            )
        return Row(
            vertical_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.END,
            spacing=2,
            opacity=0,
            animate_opacity=200,
            offset=transform.Offset(0.35, 0),
            animate_offset=animation.Animation(400, 'decelerate'),
            controls=[__]
        )

    def get_prefix_email(self, e):
        if self.function_emails:
            email = self.controls[0].content.controls[1].value
            if e.data:
                if "@kelompok5.com" in email or "@kelompok6.com" in email or "@kelompok7.com" in email or "@" in email:
                    self.controls[0].content.controls[2].offset = transform.Offset(0, 0)
                    self.controls[0].content.controls[2].opacity = 0
                    self.update()
                else:
                    self.controls[0].content.controls[2].offset = transform.Offset(-0.9, 0)
                    self.controls[0].content.controls[2].opacity = 1
                    self.update()
            else:
                self.controls[0].content.controls[2].offset = transform.Offset(0.5, 0)
                self.controls[0].content.controls[2].opacity = 0
                self.update()
        else:
            pass


    def build(self):
        return Container(
            width=320,
            height=40,
            border=border.all(0.5, "white54"),
            bgcolor=self.bg_color,
            border_radius=25,
            content=Row(
                spacing=20,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Icon(
                        offset=[0.5,0,0,0],
                        name=self.icon_name,
                        size=16,
                        opacity=0.85
                    ),
                    TextField(
                        border_color="transparent",
                        bgcolor="#3D4354",
                        height=22,
                        width=250,
                        text_style=TextStyle(size=14, font_family="Consolas"),
                        content_padding=2,
                        cursor_color="black",
                        hint_text=self.text_hint,
                        hint_style=TextStyle(size=14, font_family="Consolas"),
                        password=self.hide,
                        on_change=lambda e: self.get_prefix_email(e),
                        on_blur=None
                    ),
                    self.prefix_email_containers(),
                ]
            )
        )

class UserData(UserControl):
    def __init__(self, name, initial_name, route, page, group_chat, cc, realm_id, receiver):
        self.group_chat = group_chat
        self.route = route
        self.initial_name = initial_name
        self.name = name
        self.page = page
        self.realm_id = realm_id
        self.receiver = receiver
        self.cc = cc
        super().__init__()

    def OpenMessage(self, e):
        self.cc.realm_id = self.realm_id
        self.cc.receiver = self.receiver
        self.page.route = self.route
        self.page.update()

    def build(self):
        type_text = ""
        if self.group_chat:
            type_text = "~ Group"
        else:
            type_text = "~ Private"

        return Container(
            offset=[0.03, 0, 0, 0],
            on_click=lambda e: self.OpenMessage(e),
            content=Row(
                controls=[
                    Column(
                        spacing=1,
                        alignment="center",
                        controls=[
                            Text(
                                value=self.initial_name,
                                size=21,
                                weight="bold",
                                color="white",
                                opacity=1,
                                animate_opacity=200
                            ),

                        ]
                    ),
                    Column(
                        spacing=1,
                        alignment="center",
                        controls=[
                            Text(
                                value=self.name,
                                size=21,
                                weight="bold",
                                color="white",
                                opacity=1,
                                animate_opacity=200
                            ),

                        ]
                    ),
                    Column(
                        spacing=1,
                        offset=[0, 0, 0, 0],
                        alignment="center",
                        controls=[
                            Text(
                                value=type_text,
                                size=21,
                                weight="bold",
                                color="white",
                                opacity=1,
                                animate_opacity=200
                            )
                        ]
                    )
                ]
            )
        )