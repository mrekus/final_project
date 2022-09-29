import tkinter


class ErrorWindow:
    """
    Iššaukia ERROR langą su tekstu
    :param text: priima error lango tekstą
    """

    def __init__(self, text):
        self.error_window = tkinter.Toplevel()
        self.error_window.geometry("+900+500")
        self.error_window.title("Error")
        self.frame = tkinter.Frame(self.error_window)
        self.error_text = tkinter.Label(
            self.frame, text=text, anchor=tkinter.CENTER, font=("courier", 25, "bold")
        )
        self.ok_button = tkinter.Button(
            self.frame,
            text="Confirm",
            command=self.error_window.destroy,
            anchor=tkinter.CENTER,
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
