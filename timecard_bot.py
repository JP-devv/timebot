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
login = driver.find_element(By.NAME, '_com_liferay_login_web_portlet_LoginPortlet_login')
login.clear()
login.send_keys(username)

# Find password box and send
print('Finding password box...')
login = driver.find_element(By.NAME, '_com_liferay_login_web_portlet_LoginPortlet_password')
login.send_keys(password)

# Click sign in button
print('Attempting sign in...')
sign_in = driver.find_element(By.CLASS_NAME, 'button-holder ')
sign_in.click()
time.sleep(0.5)

# Click on Peoplesoft
driver.find_element(By.ID, 'ql-name-peopleSoftAzure').click()
time.sleep(14)

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

# CHANGE THIS
for x in range(15):
  element = driver.find_element(By.ID, f'DAY_OF_WK_DISPLAY${x}').text
  print(f'Entering hours for {element} no. {x}')
  if 'Fri' in element:
    # Select dropdown
    dropdown = driver.find_element(By.NAME, f'TRC${x}')
    select = Select(dropdown)
    select.select_by_index(1)

    # In time
    box = driver.find_element(By.NAME, f'PUNCH_TIME_1${x}')
    box.clear()
    box.send_keys('1:30PM')

    # Out time 
    box = driver.find_element(By.NAME, f'PUNCH_TIME_2${x}')
    box.clear()
    box.send_keys('3:30PM')

    # In time
    box = driver.find_element(By.NAME, f'PUNCH_TIME_3${x}')
    box.clear()
    box.send_keys('8:00PM')

    # Out time 
    box = driver.find_element(By.NAME, f'PUNCH_TIME_4${x}')
    box.clear()
    box.send_keys('9:30PM')
 
  elif 'Tue' in element or 'Thu' in element:
    # Select dropdown
    dropdown = driver.find_element(By.NAME, f'TRC${x}')
    select = Select(dropdown)
    select.select_by_index(1)

    # In time
    box = driver.find_element(By.NAME, f'PUNCH_TIME_1${x}')
    box.clear()
    box.send_keys('1:00PM')

    # Out time 
    box = driver.find_element(By.NAME, f'PUNCH_TIME_2${x}')
    box.clear()
    box.send_keys('6:00PM')

  elif 'Wed' in element:
     # In time
    box = driver.find_element(By.NAME, f'PUNCH_TIME_1${x}')
    box.clear()
    box.send_keys('8:00PM')

    # Out time 
    box = driver.find_element(By.NAME, f'PUNCH_TIME_2${x}')
    box.clear()
    box.send_keys('9:30PM')
 
# Keep browser open
print("Success! Press enter to quit")
quit = input()
