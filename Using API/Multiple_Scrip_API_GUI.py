from tkinter import *
import threading
from nsetools import Nse
import time

main_root = Tk()
main_root.title("Live price")
frame = LabelFrame(main_root, text=None)
frame.pack(padx=0.5, pady=0.5)
count = 0
nse = Nse()


def getltp(stock):
    price = nse.get_quote(stock)
    return price['lastPrice']


def getprice(stock, ltp):
    global count
    if count == 0 and stock.get():
        ltp.config(text="LTP : Loading...")
        try:
            while (True):
                a = getltp(stock.get())
                try:
                    ltp.config(text=f"NSE LTP : {a}")
                    print("Refreshed")
                except:
                    break
                time.sleep(1)
                count += 1
        except:
            try:
                ltp.config(text="NA")
            except:
                print("Error")
        finally:
            count += 1


def submit():
    for j in range(0, total):
        thr = "t" + str(j)
        thr = threading.Thread(target=lambda: getprice(N[j], P[j]))
        thr.start()


def sub():
    global total, N, P
    N = []
    P = []
    total = int(E1.get())
    for i in range(1, int(E1.get()) + 1):
        E1.destroy()
        btn.destroy()
        lbl1 = "L" + str(i)
        lbl1 = Button(frame, text=f"Name of the Stock {i}")
        lbl1.grid(row=i, column=0, sticky=E + W)
        ent = "name" + str(i)
        ent = Entry(frame)
        ent.grid(row=i, column=1, sticky=E + W)
        lbl2 = "ltp" + str(i)
        lbl2 = Button(frame, text="")
        lbl2.grid(row=i, column=2, sticky=E + W)
        N.append(ent)
        P.append(lbl2)

    sbtn = Button(frame, text="Submit", command=submit)
    sbtn.grid(row=total + 1, column=0, columnspan=3, sticky=E + W)
    # print(N)
    # print(P)


E1 = Entry(frame)
E1.grid(row=0, column=0)
btn = Button(frame, text="Submit", command=sub)
btn.grid(row=0, column=1)

main_root.mainloop()
