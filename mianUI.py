import konosubaScript
import tkinter as tk


class Ks_Win(konosubaScript.KonosubaScript):
    def __init__(self) -> None:
        super().__init__()
        root = tk.Tk()
        root.title("美好世界腳本")
        root.geometry("300x300+750+300")
        root.resizable(False, False)

        bt1 = tk.Button(text="刷活動小關卡", command=lambda: self.eventAdventureLoop())
        bt1.pack(padx=10, pady=10, ipadx=10, ipady=10)

        bt2 = tk.Button(text="刷活動boss", command=lambda: print("test"))
        bt2.pack(padx=10, pady=10, ipadx=10, ipady=10)

        bt3 = tk.Button(text="刷競技場", command=lambda: self.battleArenaLoop)
        bt3.pack(padx=10, pady=10, ipadx=10, ipady=10)
        root.mainloop()


if __name__ == "__main__":
    Ks_Win()
    print('test')