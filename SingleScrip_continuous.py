from tkinter import *
import threading
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from time import strftime

main_root = Tk()
main_root.title("Average Calculator")
frame = LabelFrame(main_root, text=None)
frame.pack(padx=0.5, pady=0.5)

def getltp():
    while True:
        try:
            if E1.get():
                base_url = "https://money.rediff.com/companies/"
                stock = E1.get()
                my_url = base_url + f"{stock}"
                uClient = uReq(my_url)
                page_html = uClient.read()
                uClient.close()
                page_soup = soup(page_html, "html.parser")
                containers = page_soup.findAll("div", {"class": "mainTab hide"})
                container = containers[0]
                price = container.findAll("span", {"class": "bold"})
                text = price[0].text
                L2.config(text=f"""{text} -- Refreshed at {strftime("%I:%M:%S %p")}""")
        except:
            L2.config(text=f"""Not recognised -- Refreshed at {strftime("%I:%M:%S %p")}""")


L1 = Label(frame, text="Stock to monitor :")
L1.grid(row=0, column=0)
E1 = Entry(frame)
E1.grid(row=0, column=1)
L2 = Label(frame, text=" -- ")
L2.grid(row=0, column=2)

thr = threading.Thread(target=getltp)
thr.daemon = True
thr.start()

main_root.mainloop()
