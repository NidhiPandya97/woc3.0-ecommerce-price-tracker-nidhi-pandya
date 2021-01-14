# Flipkart Website Price Checker

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime 
import time
import smtplib
from email.mime.text import MIMEText
import json

# Function to send email
def send_mail(product_name, price, product_link, email_id):

    sender_email = "nidhipydemo@gmail.com"  # Enter your address
    #password = input("Type your password and press enter: ")
    password = "" #Enter your password

    subject = "Product Price Drop"
    body = "Dear Customer, \n\nProduct: "+product_name+"\nProduct's Current Price: "+price+"\nProduct Link: "+product_link
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email_id

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_email, password)
    session.sendmail(sender_email, email_id, msg.as_string())

    session.quit()


# Funtion to check product price 
def price_check(product_link, my_price, email_id):

    Path = "C:\Program Files\chromedriver.exe"
    driver = webdriver.Chrome(Path)
    driver.get(product_link)
    #product_name = driver.title

    try:
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "aMaAEs"))
        )
        price_ele = main.find_element_by_class_name("_30jeq3")
        price = str(price_ele.text)
        product_price = (str(price_ele.text))[1:]  # To remove rupee sign
        product_name = driver.title
        
        if "," in product_price:
            index = product_price.index(',')

        if "," in product_price:
            product_pr1 = product_price[0:index]+product_price[index+1:]
            product_price = product_pr1

        if (float(my_price) >= float(product_price)):
            global email_flag 
            email_flag = 1
            #print("Buy a product")
            send_mail(product_name, price, product_link,email_id)
            print("Product Detail's mail is send")
        else:
            print("Can't buy the product. Price is still high")
            pass

        driver.quit()
    except:
        print("Error Occured !!")

# Product Details 
data = {}
data['product_detail'] = []

temp = input("New Product y/n: ")

if (temp == "y"):
    product_link = input("Enter Product Link: ")
    my_price = input("Enter Product Price: ")
    email_id = input("Enter Email id: ")

elif(temp == "n"):       
    fileobj = open('flipkart_data.json','r') 
    data = json.load(fileobj)
    
    for i in data['product_detail']:
        product_link = i['product_link']
        my_price = i['my_price']
        email_id = i['email_id']

    fileobj.close()

#sleep_time_sec = 2*60*60  # 2hrs
#sleep_time_hr = 2
#slee_time_min = 120 

sleep_time_sec = 15*60  # 15 mins
sleep_time_min = 15

email_flag = 0
data['product_detail'] = []

if (product_link != " " and my_price != " " and email_id != " "):
    while True:
        current_time =  datetime.datetime.now()

        fileobj = open('flipkart_data.json','r') 
        data = json.load(fileobj)
            
        for i in data['product_detail']:
            time_val = i['time']    # Last time script was runned    
        
        fileobj.close()

        #print(time_val)
        #print(current_time)

        date_time_obj = datetime.datetime.strptime(time_val, '%Y-%m-%d %H:%M:%S.%f')

        time_diff = current_time - date_time_obj
        print(time_diff)
        time_diff_str = str(time_diff)

        for i in time_diff_str:
            if(i == ":"):
                index = time_diff_str.index(':')

        hours_diff = time_diff_str[0:index] # Needed if want to run script in differnce of 2 hrs

        if (hours_diff == '1'):
            minute_diff = int(time_diff_str[index+1:index+3]) + 60  # If want to run script in differnce of 2 hrs
        else:
            minute_diff = time_diff_str[index+1:index+3]

        if(int(minute_diff) >= sleep_time_min or int(hours_diff) > 1):
            print("Script can run now !!")
            try:
                data['product_detail'].append({
                        'time': str(current_time),
                        'product_link': product_link,
                        'my_price': my_price,
                        'email_id' : email_id
                })

                with open('flipkart_data.json', 'w') as fileobj:
                    json.dump(data, fileobj)

                fileobj.close()
                    
                price_check(product_link, my_price, email_id)
                #print(email_flag)
                if(email_flag == 1):
                    break
                
                time.sleep(sleep_time_sec)
            except:
                pass

        else:
            waiting_time = sleep_time_min - int(minute_diff) # Waiting time is in minutes
            
            print("Script can run after: ", waiting_time," mins")
            time.sleep(waiting_time*60) 
