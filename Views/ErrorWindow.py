from tkinter import *


class ErrorWindow:
    """
    Iššaukia ERROR langą su tekstu
    :param text: priima error lango tekstą
    """

    def __init__(self, text):
        self.error_window = Toplevel()
        self.error_window.geometry("+900+500")
        self.error_window.title("Error")
        self.frame = Frame(self.error_window)
        self.error_text = Label(
            self.frame, text=text, anchor=CENTER, font=("courier", 25, "bold")
        )
        self.ok_button = Button(
            self.frame,
            text="Confirm",
            command=self.error_window.destroy,
            anchor=CENTER,
            bg="white",
            fg="black",
            font=("courier", 12, "bold"),
            relief="groove",
            height=1,
            width=15,
            activebackground="#0a0a0a",
            activeforeground="#e6d415",
        )
        self.error_text.grid(row=0, column=1)
        self.ok_button.grid(row=1, column=1)
        self.frame.pack(expand=True)
        self.error_window.bell()
