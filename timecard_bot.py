import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Credentials
username, password = None, None
with open('credentials', 'r') as f:
    username = f.readline().strip()
    password = f.readline().strip()

# Create a webdriver object for Chrome
print('Opening Chrome...')
driver = webdriver.Chrome()

# Open the UTRGV website
print('Accessing UTRGV...')
driver.get('https://my.utrgv.edu/web/myutrgv/home?p_p_id=com_liferay_login_web_portlet_LoginPortlet&p_p_lifecycle=0&p_p_state=normal&refererPlid=18&_com_liferay_login_web_portlet_LoginPortlet_redirect=%2F')

# Find username box and send
print('Finding username box...')
login = driver.find_element(
    By.NAME, '_com_liferay_login_web_portlet_LoginPortlet_login')
login.clear()
login.send_keys(username)

# Find password box and send
print('Finding password box...')
login = driver.find_element(
    By.NAME, '_com_liferay_login_web_portlet_LoginPortlet_password')
login.send_keys(password)

# Click sign in button
print('Attempting sign in...')
sign_in = driver.find_element(By.CLASS_NAME, 'button-holder ')
sign_in.click()
time.sleep(0.5)

# Click on Peoplesoft
driver.find_element(By.ID, 'ql-name-peopleSoftAzure').click()
time.sleep(14)

# Wait for authentication
print('Complete Authentication.\nAre you late? Y/N')
msg = input()
print('Continuing...')

# Get window handler, and switch to new tab
window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])
time.sleep(0.5)

# Click on Payroll and compensation
driver.find_element(By.ID, 'PTNUI_LAND_REC_GROUPLET_LBL$2').click()
time.sleep(4.5)

# Website switches to an iframe, create a driver from that
frame = driver.find_element(By.ID, 'main_target_win0')
    
# switch to the frame
driver.switch_to.frame(frame)

# Click back button?
if 'y' in msg:
    driver.find_element(By.NAME, 'DERIVED_TL_WEEK_PREV_WK_BTN').click()
    time.sleep(1)

# Read schedule
schedule = {}
with open('schedule.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split()
        schedule[line[0]] = line[1:len(line)]
assert schedule, 'Schedule file is empty'

# Fill in schedule accordingly
for x in range(15):
    element = driver.find_element(By.ID, f'DAY_OF_WK_DISPLAY${x}').text
    print(f'Entering hours for {element} no. {x}')
    
    # Check if element is in schedule
    if element in schedule:
      
        # Select dropdown box
        dropdown = driver.find_element(By.NAME, f'TRC${x}')
        select = Select(dropdown)
        select.select_by_index(1)
        
        # Fill in time slots
        time = schedule[element]
        for i in range(len(time)):
            box = driver.find_element(By.NAME, f'PUNCH_TIME_{i+1}${x}')
            box.clear()
            box.send_keys(time[i])

# Keep browser open
print("Success! Press enter to quit")
quit = input()
