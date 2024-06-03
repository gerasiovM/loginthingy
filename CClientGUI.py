import tkinter as tk
from json import dumps
from tkinter import *
from CClientBL import *
from CLoginGUI import CLoginGUI

BTN_IMAGE = "./Images/GUI - button.png"
# Bg file resize to 1200x536
BG_IMAGE = "./Images/GUI - BG_BIG.png"
FONT = "Calibri"
FONT_BUTTON = (FONT, 16)


class CClientGUI(CClientBL):

    def __init__(self, host, port):

        super().__init__(host, port)

        self._root = tk.Tk()
        self._canvas = None
        self._img_bg = None
        self._img_btn = None

        self._entry_IP: tk.Entry = None
        self._entry_Port: tk.Entry = None
        self._text_box_Received: tk.Text = None
        self._entry_Send_CMD: tk.Entry = None
        self._entry_Send_ARG: tk.Entry = None

        self._btn_connect = None
        self._btn_disconnect = None
        self._btn_send = None
        self._btn_login = None

        self.create_ui()

    def create_ui(self):
        self._root.title("Client GUI")

        # Load bg image
        self._img_bg = PhotoImage(file=BG_IMAGE)
        img_width = self._img_bg.width()
        img_height = self._img_bg.height()

        # Set size of the application window = image size
        self._root.geometry(f'{img_width}x{img_height}')
        self._root.resizable(False,False)

        # Create a canvas to cover the entire window
        self._canvas = tk.Canvas(self._root,width=img_width,height=img_height)
        self._canvas.pack(fill='both',expand=True)
        self._canvas.create_image(0,0,anchor="nw",image=self._img_bg)

        # Add labels, the same as.. add text on canvas
        self._canvas.create_text(90,80,text='Client',font=('Calibri',28),fill='#808080')
        self._canvas.create_text(50,180,text='IP:',font=FONT_BUTTON,fill='#000000',anchor='w')
        self._canvas.create_text(50,230,text='Port:',font=FONT_BUTTON,fill='#000000',anchor='w')
        self._canvas.create_text(50,280,text='Send:',font=FONT_BUTTON,fill='#000000',anchor='w')
        self._canvas.create_text(50,330,text='Received:',font=FONT_BUTTON,fill='#000000',anchor='w')

        # Load button image
        self._img_btn = PhotoImage(file=BTN_IMAGE)
        img_btn_w = self._img_btn.width()
        img_btn_h = self._img_btn.height()

        # Button "Connect"
        self._btn_connect = tk.Button(self._canvas,text="Connect",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                      width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                      command=self.on_click_connect)
        self._btn_connect.place(x=950,y=50)

        # Button "Disconnect"
        self._btn_disconnect = tk.Button(self._canvas,text="Disconnect",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                         width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                         command=self.on_click_disconnect,state="disabled")
        self._btn_disconnect.place(x=950,y=130)

        # Button "Send Data"
        self._btn_send = tk.Button(self._canvas,text="Send Request",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                   width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                   command=self.on_click_send,state="disabled")
        self._btn_send.place(x=950,y=210)

        # Button "Login"
        self._btn_login = tk.Button(self._canvas,text="Login",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                   width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                   command=self.on_click_login,state="disabled")
        self._btn_login.place(x=950, y=290)

        # Create Entry boxes
        self._entry_IP = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080', width=12)
        self._entry_IP.insert(0,'127.0.0.1')
        self._entry_IP.place(x=200,y=168)

        self._entry_Port = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080', width=12)
        self._entry_Port.insert(0,"8822")
        self._entry_Port.place(x=200,y=218)

        self._entry_Send_CMD = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080', width=12)
        self._entry_Send_CMD.insert(0,"Command")
        self._entry_Send_CMD.place(x=200,y=268)

        self._entry_Send_ARG = tk.Entry(self._canvas, font=('Calibri', 16), fg="#808080", width=36)
        self._entry_Send_ARG.insert(0, "Arg")
        self._entry_Send_ARG.place(x=380, y=268)

        self._text_box_Received = tk.Text(self._canvas, font=('Calibri, 12'), fg="#808080",
                                          width=58, height=7)
        self._text_box_Received.place(x=200, y=318)
        self._text_box_Received.config(state="disabled")

        self._root.after(300, self.update_received_entry)

    def run(self):
        self._root.mainloop()

    def on_click_connect(self):
        self._client_socket = self.connect()
        if self._client_socket:
            self._entry_IP.config(state="disabled")
            self._entry_Port.config(state="disabled")
            self._btn_connect.config(state="disabled")
            self._btn_disconnect.config(state="normal")
            self._btn_send.config(state="normal")
            self._btn_login.config(state="normal")

    def on_click_disconnect(self):
        bres = self.disconnect()
        if bres:
            self._entry_IP.config(state="normal")
            self._entry_Port.config(state="normal")
            self._btn_connect.config(state="normal")
            self._btn_disconnect.config(state="disabled")
            self._btn_send.config(state="disabled")
            self._btn_login.config(state="disabled")

    def on_click_send(self):
        message = self._entry_Send_CMD.get() + ">" + self._entry_Send_ARG.get()
        if message:
            self.send_data(message)
            # Use "after" to update the GUI after a short delay
            self._root.after(100,self.update_received_entry)

    def on_click_login(self):
        def callback_register(data):
            self._entry_Send_CMD.delete(0, END)
            self._entry_Send_CMD.insert(0, "REG")
            self._entry_Send_ARG.delete(0, END)
            self._entry_Send_ARG.insert(0, dumps(data))
            write_to_log(f"[CLIENT GUI] Registration - received data from Login wnd : {data}")

        def callback_signin(data):
            write_to_log(f"[CLIENT GUI] Sign in - received data from Login wnd : {data}")

        write_to_log("[CLIENT GUI] login")
        obj = CLoginGUI(self._root, callback_register, callback_signin)
        obj.run()

    def update_received_entry(self):
        message = self.receive_data()
        if message == CProtocol.DISCONNECT_MSG:
            self.on_click_disconnect()
        if message:
            self._text_box_Received.config(state="normal")
            self._text_box_Received.delete(1.0,END)
            self._text_box_Received.insert(1.0,message)
            self._text_box_Received.config(state="disabled")
        self._root.after(300, self.update_received_entry)


if __name__ == "__main__":
    client = CClientGUI(CProtocol.CLIENT_HOST, CProtocol.PORT)
    client.run()
