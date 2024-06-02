import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
from CServerBL import CClientHandler


class CConnectionsGUI:
    BTN_IMAGE = "./Images/GUI - button.png"
    BG_IMAGE = "./Images/GUI - BG.png"
    FONT = "Calibri"
    FONT_BUTTON = (FONT, 16)

    def __init__(self, parent_wnd, client_handlers, awaiting_registration):
        self._parent_wnd = parent_wnd
        self._client_handlers: list[CClientHandler] = client_handlers
        self._awaiting_registration = awaiting_registration
        self._this_wnd = tk.Toplevel(parent_wnd)
        self._this_wnd.title("Connections")

        self._canvas = None
        self._img_bg = None
        self._img_btn = None

        self._connections: ttk.Treeview = None
        self._disconnect_client: tk.Button = None

        self._registration: ttk.Treeview = None
        self._register_client: tk.Button = None

        self.create_ui()

    def create_ui(self):
        # Load bg image
        self._img_bg = PhotoImage(file=self.BG_IMAGE)
        img_width = self._img_bg.width()
        img_height = self._img_bg.height()

        # Set size of the application window = image size
        self._this_wnd.geometry(f'{img_width}x{img_height}')
        self._this_wnd.resizable(False, False)

        # Create a canvas to cover the entire window
        self._canvas = tk.Canvas(self._this_wnd, width=img_width, height=img_height)
        self._canvas.pack(fill='both', expand=True)
        self._canvas.create_image(0, 0, anchor="nw", image=self._img_bg)
        self._canvas.create_text(200, 30, text="Active connections", font=("Calibri", 24))

        self._connections = ttk.Treeview(self._canvas, height=10, columns=("ip", "port"), show=["headings"])
        self._connections.insert("", 0, values=("127.0.0.1", "8080"))
        self._connections.heading("ip", text="ip")
        self._connections.column("ip", minwidth=0, width=200)
        self._connections.heading("port", text="port")
        self._connections.column("port", minwidth=0, width=100)
        self._connections.place(x=30, y=70)

        self._registration = ttk.Treeview(self._canvas, height=10, columns=("ip", "port"), show=["headings"])
        self._registration.heading("ip", text="ip")
        self._registration.column("ip", minwidth=0, width=200)
        self._registration.heading("port", text="port")
        self._registration.column("port", minwidth=0, width=100)
        self._registration.place(x=430, y=70)
        self._this_wnd.after(50, self.update_connected)

        self._img_btn = PhotoImage(file=self.BTN_IMAGE)
        img_btn_w = self._img_btn.width()
        img_btn_h = self._img_btn.height()
        self._disconnect_client = tk.Button(self._canvas, text="Disconnect", font=("Calibri", 16), image=self._img_btn,
                                            width=img_btn_w, height=img_btn_h, command=self.on_click_disconnect_client,
                                            compound="center")
        self._disconnect_client.place(x=30, y=300)
        self._register_client = tk.Button(self._canvas, text="Register", font=("Calibri", 16), image=self._img_btn,
                                          width=img_btn_w, height=img_btn_h, command=self.on_click_register_client,
                                          compound="center")
        self._register_client.place(x=430, y=300)

    def on_click_disconnect_client(self):
        item = self._connections.focus()
        if item:
            address = self._connections.item(item, "values")
            for handler in self._client_handlers:
                if handler.get_address() == address:
                    handler.stop()

    def on_click_register_client(self):
        pass

    def run(self):
        self._this_wnd.mainloop()

    def stop(self):
        self._this_wnd.quit()

    def update_connected(self):
        connections = [x.get_address() for x in self._client_handlers]
        all_values = []
        for item in self._connections.get_children():
            values = self._connections.item(item, 'values')
            all_values.append(values)
            if values not in connections:
                self._connections.delete(item)
        for values in connections:
            if values not in all_values:
                self._connections.insert("", len(self._connections.get_children()), values=values)
        self._this_wnd.after(50, self.update_connected)

    def update_awaiting(self):
        awaiting = []


if __name__ == "__main__":
    root = tk.Tk()
    a = CConnectionsGUI(root, [])
    a.run()
