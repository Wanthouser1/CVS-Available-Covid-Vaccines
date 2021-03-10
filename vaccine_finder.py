import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler


# Your Account Sid and Auth Token from twilio.com/console (Need this info to send sms)

account_sid = 'TWILIO SID'
auth_token = 'TWILIO AUTH TOKEN'
sender = 'SENDER # FROM TWILIO ACCOUNT'
receiver = 'RECEIVER NUMBER'
client = Client(account_sid, auth_token)

# Launch driver, navigate to CVS site, scroll down

driver = webdriver.Chrome('DRIVER LOCATION')
action = ActionChains(driver)
driver.get("https://www.cvs.com/immunizations/covid-19-vaccine")
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)

# Driver finds your state's link and clicks on it

driver.find_element_by_partial_link_text('YOUR STATE').click()
element = driver.find_element_by_class_name("boxcontainer")
action.move_to_element(element).perform()


vaccine_is_available = 'Available'
nj_availability_status = driver.find_element_by_xpath('/html/body/div[2]/div/div[19]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table').text

#function looks to see if table includes any text that says "available". If yes, this triggers sms
def vaccine_finder():
    if nj_availability_status.find(vaccine_is_available) != -1:
        print("We found you a vaccine!")
        message = client.messages.create(body = 'We found you a vaccine! go to https://www.cvs.com/immunizations/covid-19-vaccine to schedule your appointment now!',from_ = sender,to = receiver)

    else:
     print("No vaccines available in your area.")

vaccine_finder()

# Schedules job_function to be run once each hour.
scheduler = BlockingScheduler()
scheduler.add_job(vaccine_finder, 'interval', hourss=1)
scheduler.start()
