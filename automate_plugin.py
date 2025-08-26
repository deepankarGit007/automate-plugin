from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

# Login credentials
username = "KRISHNA"
password = "Krishna@7588"

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Step 1: Open login page
    driver.get("https://partner.indinet.co.in/reseller/Login.aspx")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtUserName")))
    time.sleep(2)
    # Step 2: Enter credentials and login
    driver.find_element(By.ID, "txtUserName").send_keys(username)
    driver.find_element(By.ID, "txtPassword").send_keys(password)
    driver.find_element(By.ID, "save").click()
    time.sleep(2)
    # Step 3: Wait for dashboard and click on 'Account' option
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Account")))
    driver.find_element(By.LINK_TEXT, "Account").click()

    time.sleep(5)

    # Step 4: Wait for dropdowns to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddl_list")))
    driver.find_element(By.ID, "ContentPlaceHolder1_ddl_list").click()

    # Select first dropdown (Status)
    status_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddl_list"))
    status_dropdown.select_by_visible_text("Status")  # Or exact value from HTML

    time.sleep(5)

    # Select second dropdown (Active)
    driver.find_element(By.ID, "ContentPlaceHolder1_ddl_all").click()

    active_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddl_all"))
    active_dropdown.select_by_visible_text("Active")  # Or exact value from HTML

    # Step 5: Click on Search button
    driver.find_element(By.ID, "ContentPlaceHolder1_btnserch").click()

    # Wait for results to load
    time.sleep(10)

    # Step 6: Click on Print button
    driver.find_element(By.ID, "ContentPlaceHolder1_ButtonSearchPrint").click()

    # Optional: Handle new window or download
    time.sleep(10)

    # Step 7: Misc. task
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_btnCancelD")))
    driver.find_element(By.ID, "ContentPlaceHolder1_btnCancelD").click()

    time.sleep(10)

    #Step 8: Logout
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lbklogout")))
    driver.find_element(By.ID, "lbklogout").click()

    time.sleep(10)

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
    print("Task automated sucessfully...")
