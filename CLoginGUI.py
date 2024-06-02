import tkinter as tk
from tkinter import PhotoImage

BTN_IMAGE = "./Images/GUI - button small.png"
BG_IMAGE = "./Images/GUI - BG Login.png"
FONT = "Calibri"
FONT_BUTTON = (FONT, 12)


class CLoginGUI:
    _login = ""
    _password = ""

    def __init__(self, parent_wnd, callback_register, callback_signin):

        self._parent_wnd = parent_wnd
        self._this_wnd = tk.Toplevel(parent_wnd)
        self._this_wnd.title("Login")
        self._callback_register = callback_register
        self._callback_signin = callback_signin

        self._canvas = None
        self._img_bg = None
        self._img_btn = None

        self._entry_Login = None
        self._entry_Password = None

        self._btn_register = None
        self._btn_signin = None
        self._btn_ok = None
        self._btn_cancel = None

        self.create_ui()

    def create_ui(self):

        # Load bg image
        self._img_bg = PhotoImage(file=BG_IMAGE)
        img_width = self._img_bg.width()
        img_height = self._img_bg.height()

        # Set size of the application window = image size
        self._this_wnd.geometry(f'{img_width}x{img_height}')
        self._this_wnd.resizable(False, False)

        # Create a canvas to cover the entire window
        self._canvas = tk.Canvas(self._this_wnd, width=img_width, height=img_height)
        self._canvas.pack(fill='both',expand=True)
        self._canvas.create_image(0,0,anchor="nw",image=self._img_bg)

        # Add labels, the same as.. add text on canvas
        self._canvas.create_text(50,50,text='Login:',font=FONT_BUTTON,fill='#000000',anchor='w')
        self._canvas.create_text(50,130,text='Password:',font=FONT_BUTTON,fill='#000000',anchor='w')

        # Load button image
        self._img_btn = PhotoImage(file=BTN_IMAGE)
        img_btn_w = self._img_btn.width()
        img_btn_h = self._img_btn.height()

        # Button Register
        self._btn_register = tk.Button(self._canvas, text="Register", font=FONT_BUTTON, fg="#c0c0c0", compound="center",
                                     width=img_btn_w, height=img_btn_h, image=self._img_btn, bd=0,
                                     command=self.on_click_register)
        self._btn_register.place(x=370, y=15)

        # Button SignIn
        self._btn_signin = tk.Button(self._canvas, text="SignIn", font=FONT_BUTTON, fg="#c0c0c0", compound="center",
                                     width=img_btn_w, height=img_btn_h, image=self._img_btn, bd=0,
                                     command=self.on_click_signin)
        self._btn_signin.place(x=370, y=65)

        # Button Ok
        self._btn_ok = tk.Button(self._canvas, text="Ok", font=FONT_BUTTON, fg="#c0c0c0", compound="center",
                                 width=img_btn_w, height=img_btn_h, image=self._img_btn, bd=0,
                                 command=self.on_click_ok)
        self._btn_ok.place(x=370, y=115)

        # Button Cancel
        self._btn_cancel = tk.Button(self._canvas, text="Cancel", font=FONT_BUTTON, fg="#c0c0c0", compound="center",
                                     width=img_btn_w, height=img_btn_h, image=self._img_btn, bd=0,
                                     command=self.on_click_cancel)
        self._btn_cancel.place(x=370, y=165)

        # Create Entry boxes
        self._entry_Login = tk.Entry(self._canvas, font=FONT_BUTTON, fg="#808080", width=20)
        self._entry_Login.place(x=50, y=80)

        self._entry_Password = tk.Entry(self._canvas, font=FONT_BUTTON, fg="#808080", width=20, show="*")
        self._entry_Password.place(x=50, y=160)

    def run(self):
        self._this_wnd.mainloop()

    def on_click_register(self):
        self._login = self._entry_Login.get()
        self._password = self._entry_Password.get()
        data = {"login": self._login, "password": self._password}
        self._callback_register(data)

    def on_click_signin(self):
        self._login = self._entry_Login.get()
        self._password = self._entry_Password.get()
        data = {"login": self._login, "password": self._password}
        self._callback_signin(data)

    def on_click_ok(self):
        ...

    def on_click_cancel(self):
        ...


