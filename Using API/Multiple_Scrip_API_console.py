from nsetools import Nse
import threading
import time

nse = Nse()
count = 0


def submit(a):
    global count
    if count == 0:
        while True:
            print(count, '. ' ,a['lastPrice'])
            time.sleep(1)
            count += 1


a = nse.get_quote(input("Which stock?\n"))
# print(a)
# t1 = threading.Thread(target=lambda :submit(a))
# # t1.daemon = True
# t1.start()
submit(a)
#
# print("maga hengidya??")
