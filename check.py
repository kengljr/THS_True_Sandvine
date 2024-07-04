from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
#options.add_experimental_option("detach", True)
options.add_argument('--headless')

timeout = 20



def enabled_provisioner (host_ip,sub_ip):
    global options
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    driver.get(f"https://admin:pldemo01@{host_ip}/#/config/provisionerng")

    configured_host_element = EC.presence_of_element_located((By.XPATH,"//body[@class='claro']/div[1]/div/div[@id='dijit_layout_ContentPane_1']/div[@data-dojo-attach-point='currentContext']/div/div/div[3]/div/div/div[3]/div"))
    WebDriverWait(driver, timeout).until(configured_host_element).click()

    ip_count = (2*len(driver.find_elements(By.XPATH,"//div[@class='dijitTitlePaneContentInner']/div[@data-dojo-attach-point='listOfPacketLogics']/div"))) + 3
    provisioner_list=""
    for i in range (3,ip_count,2):
        ip_element = EC.presence_of_element_located((By.XPATH,f"//input[@id='dijit_form_ValidationTextBox_{i}']"))
        ip = WebDriverWait(driver, timeout).until(ip_element).get_attribute('value')
        for ip_check in sub_ip[:-1].split(" "):

            if (ip == ip_check):
                provisioner_list=provisioner_list + f"{ip_check},"
                option_click_element = EC.presence_of_element_located((By.XPATH,f"//table[@id='dijit_form_Select_{i+1}']"))
                WebDriverWait(driver, timeout).until(option_click_element).click()
                time.sleep(0.5)

                enabled_click_element = EC.presence_of_element_located((By.XPATH,f"//div[@id='dijit_form_Select_{i+1}_menu']/table/tbody/tr[1]/td[2]"))
                WebDriverWait(driver, timeout).until(enabled_click_element).click()

            else:
                continue
    
    commit_click_element = EC.presence_of_element_located((By.XPATH,"//span[@id='dijit_form_Button_0_label']"))
    WebDriverWait(driver, timeout).until(commit_click_element).click()

    description_element = EC.presence_of_element_located((By.XPATH,"//div[@data-dojo-attach-point='descriptionContainer']/div[2]/div/input"))
    WebDriverWait(driver, timeout).until(description_element).send_keys(f"Enabled ip : {provisioner_list[:-1]} timestamp : {datetime.now()}")

    send_commit_element = EC.presence_of_element_located((By.XPATH,"//span[@id='dijit_form_Button_20_label']"))
    WebDriverWait(driver, timeout).until(send_commit_element).click()
    
    percent_bar_element = driver.find_element(By.XPATH,"//div[@id='dijit_ProgressBar_0_label']").text
    print(percent_bar_element)

    while(percent_bar_element != '100%'):
        percent_bar_element = driver.find_element(By.XPATH,"//div[@id='dijit_ProgressBar_0_label']").text
        print(percent_bar_element)
        time.sleep(0.5)

    send_close_element = EC.presence_of_element_located((By.XPATH,"//span[@id='dijit_form_Button_18_label']"))
    WebDriverWait(driver, timeout).until(send_close_element).click()
    driver.close()


def disabled_provisioner (host_ip,sub_ip):
    global options
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    driver.get(f"https://admin:pldemo01@{host_ip}/#/config/provisionerng")

    configured_host_element = EC.presence_of_element_located((By.XPATH,"//body[@class='claro']/div[1]/div/div[@id='dijit_layout_ContentPane_1']/div[@data-dojo-attach-point='currentContext']/div/div/div[3]/div/div/div[3]/div"))
    WebDriverWait(driver, timeout).until(configured_host_element).click()

    ip_count = (2*len(driver.find_elements(By.XPATH,"//div[@class='dijitTitlePaneContentInner']/div[@data-dojo-attach-point='listOfPacketLogics']/div"))) + 3
    provisioner_list=""
    print(ip_count)
    for i in range (3,ip_count,2):
        ip_element = EC.presence_of_element_located((By.XPATH,f"//input[@id='dijit_form_ValidationTextBox_{i}']"))
        ip = WebDriverWait(driver, timeout).until(ip_element).get_attribute('value')
        for ip_check in sub_ip[:-1].split(" "):
            if (ip == ip_check):
                provisioner_list=provisioner_list + f"{ip_check},"
                option_click_element = EC.presence_of_element_located((By.XPATH,f"//table[@id='dijit_form_Select_{i+1}']"))
                WebDriverWait(driver, timeout).until(option_click_element).click()
                time.sleep(0.5)

                disabled_click_element = EC.presence_of_element_located((By.XPATH,f"//div[@id='dijit_form_Select_{i+1}_menu']/table/tbody/tr[2]/td[2]"))
                WebDriverWait(driver, timeout).until(disabled_click_element).click()
            else:
                continue
    
    commit_click_element = EC.presence_of_element_located((By.XPATH,"//span[@id='dijit_form_Button_0_label']"))
    WebDriverWait(driver, timeout).until(commit_click_element).click()

    description_element = EC.presence_of_element_located((By.XPATH,"//div[@data-dojo-attach-point='descriptionContainer']/div[2]/div/input"))
    WebDriverWait(driver, timeout).until(description_element).send_keys(f"Disbled ip : {provisioner_list[:-1]} timestamp : {datetime.now()}")

    send_commit_element = EC.presence_of_element_located((By.XPATH,"//span[@id='dijit_form_Button_20_label']"))
    WebDriverWait(driver, timeout).until(send_commit_element).click()

    percent_bar_element = driver.find_element(By.XPATH,"//div[@id='dijit_ProgressBar_0_label']").text
    
    while(percent_bar_element != '100%'):
        percent_bar_element = driver.find_element(By.XPATH,"//div[@id='dijit_ProgressBar_0_label']").text
        print(percent_bar_element)
        time.sleep(0.5)

    send_close_element = EC.presence_of_element_located((By.XPATH,"//span[@id='dijit_form_Button_18_label']"))
    WebDriverWait(driver, timeout).until(send_close_element).click()
    driver.close()

disabled_provisioner(sys.argv[1],sys.argv[2])
print(datetime.now())
time.sleep(600)
enabled_provisioner(sys.argv[1],sys.argv[2])
print(datetime.now())