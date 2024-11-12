from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import requests





def initial():
    # Set up Chrome options to connect to the existing session
    options = Options()

    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # Connect to an existing Chrome instance via the debugger address
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to the specified debugging port


    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to the specified debugging port

    # Create a new WebDriver instance that connects to the existing browser
    driver = webdriver.Chrome(service=Service(), options=options)

    # Open the website

    # Find the "Provinsi Aceh" option and click it
    for i in range(1, 418):
        driver.get("https://infopemilu.kpu.go.id/Pemilihan/Pasangan_calon")

        time.sleep(1)

        # Select "Gubernur" from the "jenis_pemilihan" dropdown
        jenis_pemilihan_select = Select(driver.find_element(By.ID, "jenis_pemilihan"))
        jenis_pemilihan_select.select_by_visible_text("Bupati")


        time.sleep(1)
        # For the "nama_wilayah" select dropdown (using Select2)
        # Click on the dropdown to make the options visible
        wilayah_dropdown = driver.find_element(By.CSS_SELECTOR, ".select2-selection--single")
        wilayah_dropdown.click()

        # Wait for the options to load
        time.sleep(1)
        province_option = driver.find_element(By.XPATH, f"(//li)[{i + 1}]")

        res = province_option.get_attribute("innerText")

        province_option.click()

        province_option_value = f"{i+1}-{res}"

        # Optionally, wait for a few seconds to see the changes
        time.sleep(1)


        # Find the Filter button by its id and click it
        filter_button = driver.find_element(By.ID, "filter-btn")
        filter_button.click()

        time.sleep(1)

        no_paslon = driver.find_elements(By.CSS_SELECTOR, "#card-container .col-md-4 .card")
        
        for i in range(len(no_paslon)):
            text = no_paslon[i].text
            number = text.split("\n")[1].strip()
            calon = text.split("\n")[2].strip()
            wakil_calon = text.split("\n")[5].strip()

            print(f"Nomor Paslon: {number}")

            imgs = no_paslon[i].find_elements(By.CSS_SELECTOR, "#card-container .col-md-4 .card .row img")

            
            for j in range(len(imgs)):
                src = imgs[j].get_attribute("src")
                alt = imgs[j].get_attribute("alt")
                # Take a screenshot of the img element and save it
                # imgs[j].screenshot(f"img_{alt}_{j}.png")
                # time.sleep(1)
                # driver.get(src)
                # # Take a screenshot of the image page
                # driver.save_screenshot(f"image_{alt}.png")

                # if j is odd number, it means the image is calon
                if j % 2 == 0:
                    alt = f"{calon}-{alt}"
                else:
                    alt = f"{wakil_calon}-{alt}"

                # Optional: Create a custom name for the file
                custom_filename = f"paslon-{number}-{alt}.png"
                try:
                    response = requests.get(src)
                    if response.status_code == 200:
                        # Define the path where the image will be saved
                        # macos path
                        # folder_path = os.path.join("/Users/adith/Project/scraping_selenium/Bupati", province_option_value)

                        #windows path
                        folder_path = os.path.join("C:\\Users\\User\\Desktop\\Project\\selenium_scraping\\Bupati", province_option_value)

                        # Create the folder if it doesn't exist
                        os.makedirs(folder_path, exist_ok=True)

                        save_path = os.path.join(folder_path, custom_filename)

                        # Save the image wßith the new name
                        with open(save_path, "wb") as file:
                            file.write(response.content)
                        print(f"Image saved as {custom_filename}")
                    else:
                        print(f"Failed to download image {i} from {src}")

                except Exception as e:
                    print(f"Error downloading image {i}: {e}")
                    continue

                print(f"Image src: {src}")
                print(f"Image alt: {alt}")
                print(f"province_option_value: {province_option_value}")
                print("=====================================")


    # Optionally, close the browser
    driver.quit()





if __name__ == "__main__":
    initial()



