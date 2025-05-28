from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta

app= Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    return "Welcome to the SBSTC Bus Route API"


# Fetch bus routes from the SBSTC website (From a specific stop)
@app.route('/bus_routes_all', methods=['POST'])
def get_bus_routes():
    input_data= request.get_json()
    bus_stop_id= input_data.get('bus_stop_id')

    driver = webdriver.Chrome()
    driver.get("https://sbstc.co.in/BusRoutes")

    try:
        wait = WebDriverWait(driver, 10)
        stop_dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#from")))
        Select(stop_dropdown).select_by_value(bus_stop_id) 
        search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success.btn-sm")))
        search_btn.click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".route-details")))
        time.sleep(1)

        table = driver.find_element(By.CSS_SELECTOR, "table.table.table-bordered.table-hover.tableBg")
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")  

        bus_routes = []
        for i, row in enumerate(rows, start=1):
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            bus_routes.append(row_data)

        print(bus_routes)
        return jsonify(bus_routes)

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        time.sleep(3)
        driver.quit()



#fetch all the bus from source to destination
@app.route('/bus_routes', methods=['POST'])
def get_bus_routes_all():
    input_data = request.get_json()
    source = input_data.get('source')
    destination = input_data.get('destination')
    bus_routes = []

    driver = webdriver.Chrome()

    
    # driver.get("https://sbstconline.co.in/reservation-home?faces-redirect=true&deviceType=browser")

    # try:
    #     wait = WebDriverWait(driver, 15)

    #     # Source
    #     source_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='search:fromStopPojo_input']")))
    #     source_input.clear()
    #     source_input.send_keys(source)
    #     time.sleep(5)

    #     first_source_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ui-autocomplete-items > li")))
    #     driver.execute_script("arguments[0].click();", first_source_option)


    #     # Destination
    #     destination_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='search:toStopPojo_input']")))
    #     destination_input.clear()
    #     destination_input.send_keys(destination)
    #     time.sleep(5)

    #     first_dest_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"ul.ui-autocomplete-items > li")))
    #     driver.execute_script("arguments[0].click();", first_dest_option)


    #     # Date
    #     tomorrow = datetime.now() + timedelta(days=1)
    #     tomorrow_str = tomorrow.strftime('%d-%m-%Y')
    #     date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='search:popup2_input']")))
    #     date_input.clear()
    #     date_input.send_keys(tomorrow_str)
    #     time.sleep(2)

    #     # Search
    #     search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='search:j_idt158'] span[class='ui-button-text ui-c']")))
    #     search_btn.click()

    #     time.sleep(5)

    #     results = driver.find_elements(By.CSS_SELECTOR, "div[id*='search:busDtls']")
    #     for res in results:
    #         bus_routes.append(res.text)

    #     # return jsonify({"routes": bus_routes})

    # except Exception as e:
    #     return jsonify({"error": str(e)})

    # finally:
    #     driver.quit()

    #fetch from red bus
    driver.get("https://www.redbus.in/")
    try:
        wait = WebDriverWait(driver, 15)

        # Source
        source_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#src")))
        source_input.clear()
        source_input.send_keys(source)
        time.sleep(1)
        first_source_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.autoFill li")))
        driver.execute_script("arguments[0].click();", first_source_option)
        time.sleep(1)

        # Destination
        destination_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dest")))
        destination_input.clear()
        destination_input.send_keys(destination)
        time.sleep(1)
        first_dest_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.autoFill li")))
        driver.execute_script("arguments[0].click();", first_dest_option)
        time.sleep(1)
    
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        driver.quit()


if __name__ == '__main__':
    app.run(debug=True)