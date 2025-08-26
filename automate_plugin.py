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
    status_dropdown.select_by_visible_text("Status")
    time.sleep(5)

    # Select second dropdown (Active)
    driver.find_element(By.ID, "ContentPlaceHolder1_ddl_all").click()
    active_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddl_all"))
    active_dropdown.select_by_visible_text("Active")

    # Step 5: Click on Search button
    driver.find_element(By.ID, "ContentPlaceHolder1_btnserch").click()
    time.sleep(5)

    # Step 6: Click on Print button
    driver.find_element(By.ID, "ContentPlaceHolder1_ButtonSearchPrint").click()
    time.sleep(5)

    # Step 6.1: Switch to Print window if a new one opened
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        print("Switched to Print window")

    # Step 6.2: Debug all iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print("Found iframes:", len(iframes))
    for i, f in enumerate(iframes):
        print(f"iframe {i}: id={f.get_attribute('id')} name={f.get_attribute('name')}")

    # Step 6.3: Try each iframe until Export is found
    found = False
    for i, f in enumerate(iframes):
        driver.switch_to.default_content()  # reset back to main document
        driver.switch_to.frame(f)          # go inside this iframe
        print(f"Switched to iframe {i}")
        try:
            export_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@value,'Export To Excel')]"))
            )
            export_btn.click()
            print(" Export to Excel clicked inside iframe", i)

            time.sleep(5)

            # 🔹 Step 6.4: Handle reason textarea + submit
            try:
                reason_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "TEXTAREA"))
                )
                reason_box.send_keys("Testing reason")
                print(" Filled reason textarea")
                time.sleep(2)
                # Click Submit
                submit_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "ucDownLoadVerification_btnSubmitreason"))
                )
                submit_btn.click()
                print(" Submit clicked")
                time.sleep(2)
                # Click Export again
                export_btn2 = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[contains(@value,'Export To Excel')]"))
                )
                export_btn2.click()
                print(" Export to Excel clicked again")

                time.sleep(2)

            except Exception as e:
                print(" No textarea/submit appeared:", e)

            found = True
            break
        except:
            print(f"No export button in iframe {i}, trying next...")

    if not found:
        print(" Export button not found in any iframe!")

        time.sleep(2)

    driver.switch_to.default_content()  # exit iframe

    # Step 7: Misc. task (Cancel dialog)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_btnCancelD")))
    driver.find_element(By.ID, "ContentPlaceHolder1_btnCancelD").click()
    time.sleep(2)

    # Step 8: Logout
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lbklogout")))
    driver.find_element(By.ID, "lbklogout").click()
    time.sleep(2)

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()