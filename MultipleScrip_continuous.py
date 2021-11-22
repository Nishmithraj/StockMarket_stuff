'''
Can be modified in between it is running
Advanced multiple stock live
Designed to be used in Phones, geometry wise
'''

from tkinter import *
import threading
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from time import strftime

main_root = Tk()
main_root.title("NSE Live")
frame = LabelFrame(main_root, text=None)
frame.pack(padx=0.5, pady=0.5, fill=BOTH)


def getltp(stock, value, refresh):
    while True:
        try:
            if stock.get():
                base_url = "https://money.rediff.com/companies/"
                put = stock.get()
                my_url = base_url + f"{put}"
                uClient = uReq(my_url)
                page_html = uClient.read()
                uClient.close()
                page_soup = soup(page_html, "html.parser")
                containers = page_soup.findAll("div", {"class": "mainTab hide"})
                container = containers[0]
                price = container.findAll("span", {"class": "bold"})
                text = price[0].text
                value.config(text=f"{text} ", font=("Helvetica",10, 'bold'))
                refresh.config(text=f"""at {strftime("%I:%M:%S %p")}""")
        except:
            value.config(text="NA ", font=("Helvetica",10, 'bold'))
            refresh.config(text=f"""at {strftime("%I:%M:%S %p")}""")


def sub():
    global total, N, P, T
    N = []
    P = []
    T = []
    total = int(E1.get())
    for i in range(1, int(E1.get()) + 1):
        L1.destroy()
        E1.destroy()
        btn.destroy()
        head1 = Label(frame, text="Stocks", font=("Helvetica",10, 'bold'))
        head1.grid(row=0, column=0, columnspan=2, sticky=E+W)
        head2 = Label(frame, text="Price", font=("Helvetica",10, 'bold'))
        head2.grid(row=0, column=2, sticky=E+W)
        head3 = Label(frame, text="Refreshed", font=("Helvetica", 10, 'bold'))
        head3.grid(row=0, column=3, sticky=E + W)
        lbl1 = "L" + str(i)
        lbl1 = Label(frame, text=f"S{i}")
        lbl1.grid(row=i, column=0)
        ent = "name" + str(i)
        ent = Entry(frame, width=12)
        ent.grid(row=i, column=1)
        lbl2 = "ltp" + str(i)
        lbl2 = Label(frame, text="")
        lbl2.grid(row=i, column=2)
        lbl3 = "refresh" + str(i)
        lbl3 = Label(frame, text="")
        lbl3.grid(row=i, column=3)
        N.append(ent)
        P.append(lbl2)
        T.append(lbl3)
    src = Label(frame, text="Source = https://money.rediff.com/companies/")
    src.grid(row=total + 1, column=0, columnspan=4, sticky=E + W)
    for j in range(0, total):
        thr = "t" + str(j)
        thr = threading.Thread(target=lambda: getltp(N[j], P[j], T[j]))
        thr.daemon = True
        thr.start()


L1 = Label(frame, text="How many to monitor :")
L1.grid(row=0, column=0, ipady=10)
E1 = Entry(frame)
E1.grid(row=0, column=1)
btn = Button(frame, text="Submit", command=sub, font=("Helvetica", 10, 'bold'))
btn.grid(row=1, column=0, columnspan=2, sticky=E+W)

main_root.mainloop()
