from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.daraz.com.np/wireless-earbuds/?spm=a2a0e.pdp.breadcrumb.4.7e9e31856toOV7")


try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ant-col-19"))
    )
    output_file_path = "root_data.txt"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(element.text)    
    # print("Text of the dynamic element:", element.text)
    child_divs = element.find_elements(By.CLASS_NAME,"gridItem--Yd0sa")
    data_list = []

# Iterate through each child div and extract their values
    for child_div in child_divs:
        print("entered in for loop: ")
        title ={"title": child_div.find_element(By.ID, "id-title").text,
                }
        data_list.append(title)
        try:
            ratings = {"ratings": child_div.find_element(By.CSS_SELECTOR, ".ratig-num--KNake").text}
            data_list.append(ratings)
        except Exception as e:
            ratings = {"ratings":None}
            data_list.append(ratings)
            pass   

    output_file_path = "output.txt"
    with open(output_file_path, "+a", encoding="utf-8") as output_file:
        for index, value in enumerate(data_list, start=1):
            output_file.write(f"{index}: {value}\n")
            print("succesfuly saved the data")


except Exception as e:
    print("Element not found within the specified time.")
    




# Perform other interactions as needed
# ...

# Close the browser window
driver.quit()