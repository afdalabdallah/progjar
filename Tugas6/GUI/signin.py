from component import *

def SignInView(page, cc):
    # Main Page Controls
    return Card(
            color="#1B202D",
            width=408,
            height=612,
            elevation=15,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=(
                    # Margin divider from card box for rotation box
                    Divider(height=40, color='transparent'),
                    # This is where the main controls will be added
                    Stack(
                        controls=[
                            AnimationBox("#e9665a", None, 0),
                            AnimationBox("#7df6dd", "#23262a", pi / 4)
                        ]
                    ),
                    # Margin divider from rotation box for title
                    Divider(height=20, color='transparent'),
                    Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            # Title for sign in page
                            Text("Welcome!", size=22, weight="bold", font_family="Consolas"),
                            Text("Sign in to continue", size=13, weight="bold", font_family="Consolas"),
                            # Margin divider from title for input field
                            Divider(height=20, color='transparent'),
                            Text("Email", size=20, weight="bold", font_family="Consolas"),
                            InputField("#3D4354", icons.PERSON_ROUNDED, "Email", False, True),
                            Divider(height=5, color='transparent'),
                            Text("Password", size=20, weight="bold", font_family="Consolas"),
                            InputField("#3D4354", icons.LOCK_OPEN_ROUNDED, "Password", True, False),
                            Divider(height=2, color='transparent'),
                            Row(
                                width=320,
                                alignment=MainAxisAlignment.END,
                                spacing=0,
                                controls=[
                                    Text("Don't have account? ", size=15, font_family="Consolas"),
                                    HyperLink("Sign Up", "Consolas", "/sign-up", page)
                                ]
                            ),
                            Divider(height=45, color='transparent'),
                            Button('Sign In', "/chat", "SignIn", page, cc)
                        ]
                    ),
                )
            )
        )
