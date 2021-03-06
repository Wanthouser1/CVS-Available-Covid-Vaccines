#!/usr/bin/env python3
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler


def vaccine_finder():
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'YOUR ACCOUNT SID'
    auth_token = 'YOUR AUTH TOKEN'
    sender = 'SENDER NUMBER FROM TWILIO'
    receiver = 'RECEIVER NUMBER'
    client = Client(account_sid, auth_token)

    driver = webdriver.Chrome('DRIVER LOCATION')
    action = ActionChains(driver)
    driver.get("https://www.cvs.com/immunizations/covid-19-vaccine")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)

    driver.find_element_by_partial_link_text('YOUR STATE').click()
    element = driver.find_element_by_class_name("boxcontainer")
    action.move_to_element(element).perform()


    vaccine_is_available = 'Available'
    nj_availability_status = driver.find_element_by_xpath('/html/body/div[2]/div/div[19]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table').text
    if nj_availability_status.find(vaccine_is_available) != -1:
        print("We found you a vaccine!")
        message = client.messages.create(body = 'We found you a vaccine! go to https://www.cvs.com/immunizations/covid-19-vaccine to schedule your appointment now!',from_ = sender,to = receiver)

    else:
        print("No vaccines available in your area.")
    driver.quit()

vaccine_finder()

# Schedules job_function to be run once each minute
scheduler = BlockingScheduler()
scheduler.add_job(vaccine_finder, 'interval', minutes=5)
scheduler.start()
