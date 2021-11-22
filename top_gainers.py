import time
from tkinter import *
from tkinter import messagebox
import threading
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def quit_code():
    global count
    try:
        driver.close()
        exit()
    except:
        exit()
    try:
        driver_top_gainers.close()
        top_gainers_frame.destroy()
        count=0
    except:
        pass


def ltp(stockID):
    global driver
    stock_name.destroy()
    # main_root.title(f"Specefic one -{name}")
    btn.grid(row=2, column=0, sticky='news')
    updated_time.grid(row=2, column=1, sticky='news')
    # nse_frame.config(text=f'Nse - {name}', font=('Helvetica', 10, 'bold'))
    # bse_frame.config(text=f'Bse - {name}', font=('Helvetica', 10, 'bold'))
    nse_val.config(text='Fetching..')
    nse_val_change.config(text='please wait')
    bse_val.config(text='Fetching..')
    bse_val_change.config(text='please wait')
    btn.config(text="Stop and quit", command=quit_code)
    options = Options()
    # options.headless = True

    # Don't allow images to load
    # chrome_prefs = {}
    # options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('start-maximized')
    PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=PATH, desired_capabilities=capa)
    driver.get(f'https://www.moneycontrol.com/technical-analysis/indianbank/{stockID}/daily')
    waits = WebDriverWait(driver, 5000)
    waits.until(EC.presence_of_element_located((By.XPATH, '//*[@id="div_bse_livebox_wrap"]/div[1]/div[1]/div/div[2]/span[1]')))
    driver.execute_script("window.stop();")
    # clear browser data
    # Open a new window
    time.sleep(2)
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome://settings/clearBrowserData')
    time.sleep(1)
    # driver.minimize_window()
    time.sleep(2)
    clearButton = driver.execute_script("return document.querySelector('settings-ui')"
                                        ".shadowRoot.querySelector('settings-main')"
                                        ".shadowRoot.querySelector('settings-basic-page')"
                                        ".shadowRoot.querySelector('settings-section > settings-privacy-page')"
                                        ".shadowRoot.querySelector('settings-clear-browsing-data-dialog')"
                                        ".shadowRoot.querySelector('#clearBrowsingDataDialog')")

    search_button = clearButton.find_element_by_css_selector("#clearBrowsingDataConfirm")
    search_button.click()

    # time.sleep(5)
    print("cleared cache")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # options.headless = True
    # driver = webdriver.Chrome(options=options, executable_path=PATH, desired_capabilities=capa)

    # driver.get(f'https://www.moneycontrol.com/technical-analysis/indianbank/{stockID}/daily')
    driver.refresh()
    wait1 = WebDriverWait(driver, 3000)
    wait1.until(EC.visibility_of_element_located((By.XPATH,
                                                  '//*[@id="div_bse_livebox_wrap"]/div[1]/div[1]/div/div[2]/span[1]')))
    # driver.execute_script("window.stop();")
    # driver.close()

    old_nse = 0.0000
    old_bse = 0.0000
    old_nse_bg = 'black'
    old_bse_bg = 'black'
    stock_name_lbl.grid(row=0, column=0, columnspan=2, sticky='news')
    name = driver.find_element_by_xpath('//*[@id="sec_quotes"]/div[3]/div/h1').text
    main_root.title(f"Specefic one -{name}")
    stock_name_lbl.config(text=name)
    print('Opened Moneycontrol for : ', name)
    while True:
        try:
            # driver.refresh()
            bse = driver.find_element_by_xpath('//*[@id="div_bse_livebox_wrap"]/div[1]/div[1]/div/div[2]/span[1]').text
            bse_change = driver.find_element_by_xpath(
                '//*[@id="div_bse_livebox_wrap"]/div[1]/div[1]/div/div[2]/span[3]').text
            nse = driver.find_element_by_xpath('//*[@id="div_nse_livebox_wrap"]/div[1]/div[1]/div/div[2]/span[1]').text
            nse_change = driver.find_element_by_xpath(
                '//*[@id="div_nse_livebox_wrap"]/div[1]/div[1]/div/div[2]/span[3]').text
            # print(f"nse:{float(nse)}, oldnse:{float(old_nse)}")
            # print(f"bse:{float(bse)}, oldbse:{float(old_bse)}")
            if float(nse) > float(old_nse):
                nse_bg = 'green'
            elif float(nse) < float(old_nse):
                nse_bg = 'red'
            else:
                nse_bg = old_nse_bg
            old_nse_bg = nse_bg

            if float(bse) > float(old_bse):
                bse_bg = 'green'
            elif float(bse) < float(old_bse):
                bse_bg = 'red'
            else:
                bse_bg = old_bse_bg
            old_bse_bg = bse_bg

            # driver.execute_script("window.stop();")
            nse_val.config(text=nse, bg=nse_bg)
            nse_val_change.config(text=nse_change)
            bse_val.config(text=bse, bg=bse_bg)
            bse_val_change.config(text=bse_change)
            old_nse = float(nse)
            old_bse = float(bse)
            updated_time.config(text=f"Updated at {datetime.now().time()}")
            time.sleep(0.5)
        except Exception as e:
            print(e)
            print("Stopped fetching the main")
            continue


def check_stock():
    name = str(stock_name.get()).upper()
    # name_dict = {"TM":"TM03", "IB":"IB04", "JSL":"JSL01", "SAIL":"SAI", "GAIL":"GAI", "MRPL":"MRP"}
    if 'TM' in name:
        return 'TM03'
    if 'IB' in name:
        return 'IB04'
    if 'JSL' in name:
        return 'JSL01'
    if 'SAIL' in name:
        return 'SAI'
    if 'GAIL' in name:
        return 'GAI'
    if 'MRPL' in name:
        return 'MRP'
    if 'EXI' in name:
        return 'EI'
    else:
        return None

def top_gainers():
    global driver_top_gainers
    global top_gainers_frame
    top_gainers_frame = LabelFrame(main_root, text="Top_gainers")
    top_gainers_frame.grid(row=3, column=0, columnspan=2, sticky='news')

    options = Options()
    # options.headless = True

    # Don't allow images to load
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('start-minimized')
    PATH = 'chromedriver.exe'
    driver_top_gainers = webdriver.Chrome(options=options, executable_path=PATH, desired_capabilities=capa)
    driver_top_gainers.get('https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php?index=FNO')
    # driver_top_gainers.minimize_window()
    head1 = Label(top_gainers_frame, text="Stock", font=("Helvetica", 10, 'bold'), padx=40, anchor='w')
    head1.grid(row=0, column=0, columnspan=2, sticky='news')
    head2 = Label(top_gainers_frame, text="LTP", font=("Helvetica", 10, 'bold'), padx=40, anchor='w')
    head2.grid(row=0, column=2, sticky='news')
    head3 = Label(top_gainers_frame, text="Change", font=("Helvetica", 10, 'bold'), padx=40, anchor='w')
    head3.grid(row=0, column=3, sticky='news')
    head4 = Label(top_gainers_frame, text="Gain", font=("Helvetica", 10, 'bold'), padx=40, anchor='w')
    head4.grid(row=0, column=4, sticky='news')
    top_gainers_lbl = Label(top_gainers_frame, text='Loading please wait', font=('calibri', 20))
    top_gainers_lbl.grid(row=1, column=0,rowspan=8, sticky='news')
    # quit_btn = Button(top_gainers_frame, text="QUIT_top_gainers", command = quit_code)
    # quit_btn.grid(row=0, column=5, rowspan=10, sticky='news')
    while True:
        driver_top_gainers.minimize_window()
        try:
            waiter = WebDriverWait(driver_top_gainers, 20)
            waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mc_content"]/section/section/div[1]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[1]/span/span/a')))
        except Exception as e:
            try:
                if driver_top_gainers.find_element_by_xpath('//*[@id="mc_content"]/section/section/div[1]/div[2]/div/div/div[2]/table/tbody/tr/td').text:
                    a = driver_top_gainers.find_element_by_xpath('//*[@id="mc_content"]/section/section/div[1]/div[2]/div/div/div[2]/table/tbody/tr/td').text
                    print(a)
                    top_gainers_lbl.config(text=a)
                    continue
            except:
                print(e)
                continue
        if top_gainers_lbl:
            top_gainers_lbl.destroy()
        company = []
        last_traded_price = []
        change = []
        gain = []
        total = 10
        for i in range(1, total+1):
            company.append(driver_top_gainers.find_element_by_xpath('//*[@id="mc_content"]/section/section/div[1]/div[2]/div/div/div[2]/table/tbody/tr['+str(i)+']/td[1]/span/span/a').text)
            last_traded_price.append(driver_top_gainers.find_element_by_xpath('//*[@id="mc_content"]/section/section/div[1]/div[2]/div/div/div[2]/table/tbody/tr['+str(i)+']/td[4]').text)
            change.append(driver_top_gainers.find_element_by_xpath('//*[@id="mc_content"]/section/section/div[1]/div[2]/div/div/div[2]/table/tbody/tr['+str(i)+']/td[6]').text)
            gain.append(driver_top_gainers.find_element_by_xpath('//*[@id="mc_content"]/section/section/div[1]/div[2]/div/div/div[2]/table/tbody/tr['+str(i)+']/td[7]').text)
        for j in range(1, len(company)+1):
            lbl1 = Label(top_gainers_frame, text=company[j-1], padx=40, anchor='w', bd=2)
            lbl1.grid(row=j, column=0, columnspan=2, sticky='news')
            lbl2 = Label(top_gainers_frame, text=last_traded_price[j-1], padx=40, anchor='w')
            lbl2.grid(row=j, column=2, sticky='news')
            lbl3 = Label(top_gainers_frame, text=change[j-1], padx=40, anchor='w')
            lbl3.grid(row=j, column=3, sticky='news')
            lbl4 = Label(top_gainers_frame, text=gain[j-1], padx=40, anchor='w')
            lbl4.grid(row=j, column=4, sticky='news')
        src = Label(top_gainers_frame, text=f"Source = Moneycontrol, updated at : {datetime.now().time()}", anchor=E, font=('calibri', 8))
        src.grid(row=total + 1, column=0, columnspan=6, sticky='news')
        time.sleep(2)
        driver_top_gainers.refresh()


def start_thread():
    global count
    stockID = check_stock()
    if stockID == None:
        messagebox.showerror('Error', 'Enter the correct Stock name please!\n\n Available stocks:\nExide, TM, IB, JSL, SAIL, GAIL, MRPL')
    else:
        print("StockID :", stockID)
        t1 = threading.Thread(target=lambda: ltp(stockID))
        t1.daemon = True
        t1.start()
    print("Count : ", count)
    if count == 0:
        count+=1
        t2 = threading.Thread(target=lambda :top_gainers())
        t2.daemon = True
        t2.start()


if __name__ == '__main__':
    count = 0
    main_root = Tk()
    main_root.title('Specefic one😊')

    nse_frame = LabelFrame(main_root, text='NSE price', font=('Helvetica', 10, 'bold'))
    nse_frame.grid(row=1, column=0, sticky='news')

    bse_frame = LabelFrame(main_root, text='BSE price', font=('Helvetica', 10, 'bold'))
    bse_frame.grid(row=1, column=1, sticky='news')

    nse_val_change = Label(nse_frame, text="", font=('Helvetica', 20, 'bold'))
    nse_val = Label(nse_frame, text='No data', font=('Helvetica', 40, 'bold'), padx=70)
    bse_val_change = Label(bse_frame, text="", font=('Helvetica', 20, 'bold'))
    bse_val = Label(bse_frame, text='No data', font=('Helvetica', 40, 'bold'), padx=70)
    updated_time = Label(main_root, text='', anchor=E, font=('calibri', 8))

    nse_val.grid(row=0, column=0, sticky='news')
    nse_val_change.grid(row=1, column=0, sticky='news')
    bse_val.grid(row=0, column=0, sticky='news')
    bse_val_change.grid(row=1, column=0, sticky='news')

    btn = Button(main_root, text="Start to fetch", command=start_thread)
    btn.grid(row=2, column=1, sticky='news')

    stock_name = Entry(main_root)
    stock_name.grid(row=2, column=0, sticky='news')

    stock_name_lbl = Label(main_root, text='', font=('Helvetica', 20, 'bold'))

    main_root.mainloop()
