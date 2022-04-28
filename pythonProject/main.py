#Libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Expected_cond
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import unittest
import time

#Get the correct driver and configurarion according with your browser from https://pypi.org/project/selenium/

#Chrome browser config
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disabled-extensions')
service_path = Service('G:\\jorge\\OneDrive\\Documentos\\PycharmProjects\\chromedriver.exe')

#Generic methods definition

# Open the web page
def open_page(driver,URL):

    driver.get(URL)

# Method to click an element by CSS_Selector
def click_button_by_CSS_SELECTOR(driver,CSS_SELECTOR):

    WebDriverWait(driver, 5) \
        .until(Expected_cond.element_to_be_clickable((By.CSS_SELECTOR,
                                           CSS_SELECTOR.replace(' ', '.')))) \
        .click()

# Method to click an element by XPATH
def click_button_by_XPATH(driver, XPATH):
    WebDriverWait(driver, 5) \
        .until(Expected_cond.element_to_be_clickable((By.XPATH,
                                                      XPATH)))\
        .click()

# Method to write text into an element by CSS_Selector
def insert_text_by_CSS_SELECTOR(driver,CSS_SELECTOR,text):
    # Use a breakpoint in the code line below to debug your script.
    WebDriverWait(driver, 5) \
        .until(Expected_cond.element_to_be_clickable((By.CSS_SELECTOR,
                                           CSS_SELECTOR.replace(' ', '.')))) \
        .send_keys(text)

# Method that return if an element is displayed by XPATH
def displayed_by_XPATH(driver,XPATH):
    # Use a breakpoint in the code line below to debug your script.
    WebDriverWait(driver, 5) \
        .until(Expected_cond.element_to_be_clickable((By.XPATH,
                                           XPATH)))
    return driver.find_element(By.XPATH, XPATH).is_displayed()

# Method that return the elements that have a CLASS_NAME
def getElements_by_CLASS_NAME(driver,Class_Name):
    # Use a breakpoint in the code line below to debug your script.
    WebDriverWait(driver, 5) \
        .until(Expected_cond.element_to_be_clickable((By.CLASS_NAME,
                                           Class_Name)))
    return driver.find_elements(By.CLASS_NAME, Class_Name)


# This is an application to test the behavior of  # https://www.saucedemo.com/

# The following behaviors will be tested:
#   Test_00A : Login with a valid user
#   Test_00B : Login with an invalid user
#   Test_00C : Logout from the home page
#   Test_00D : Sort products by Price (low to high)
#   Test_00E : Add multiple items to the shopping cart
#   Test_00F : Add the specific product ‘Sauce Labs Onesie’ to the shopping cart
#   Test_00F : Complete a purchase

class TestLoginPage(unittest.TestCase):

    # Test-00A
    # This test insert a valid username and password then verify that the product page is displayed
    # Input:
    #   Username : standard_user
    #   Password: secret_sauce
    # Expected output
    #   URL : https://www.saucedemo.com/inventory.html

    def test_00A(self):
        driver = webdriver.Chrome(service=service_path, options=options)
        open_page(driver, 'https://www.saucedemo.com/')
        insert_text_by_CSS_SELECTOR(driver, 'input#user-name', 'standard_user')
        insert_text_by_CSS_SELECTOR(driver, 'input#password', 'secret_sauce')
        click_button_by_CSS_SELECTOR(driver, 'input#login-button')
        self.assertEqual(driver.current_url, 'https://www.saucedemo.com/inventory.html', driver.current_url+' is not equal to https://www.saucedemo.com/inventory.html')
        driver.quit()

    # Test-00B
    # This test insert an invalid username and password then verify that the login error message is displayed
    # Input:
    #   Username : invalid
    #   Password: invalid
    # Expected output
    #   Login error message displayed

    def test_00B(self):
        driver = webdriver.Chrome(service=service_path, options=options)
        open_page(driver, 'https://www.saucedemo.com/')
        insert_text_by_CSS_SELECTOR(driver, 'input#user-name', 'invalid')
        insert_text_by_CSS_SELECTOR(driver, 'input#password', 'invalid')
        click_button_by_CSS_SELECTOR(driver, 'input#login-button')
        self.assertEqual(True, displayed_by_XPATH(driver, '/html/body/div/div/div[2]/div[1]/div[1]/div/form/div[3]/h3'), 'Login error message was not displayed')
        driver.quit()

    # Test-00C
    # This test logout action from the page
    # Input:
    #   Click in logout button
    # Expected output
    #   Login page is displayed

    def test_00C(self):
        driver = webdriver.Chrome(service=service_path, options=options)
        open_page(driver, 'https://www.saucedemo.com/')
        insert_text_by_CSS_SELECTOR(driver, 'input#user-name', 'standard_user')
        insert_text_by_CSS_SELECTOR(driver, 'input#password', 'secret_sauce')
        click_button_by_CSS_SELECTOR(driver, 'input#login-button')
        click_button_by_CSS_SELECTOR(driver, 'button#react-burger-menu-btn')
        click_button_by_CSS_SELECTOR(driver, 'a#logout_sidebar_link')
        self.assertEqual(driver.current_url, 'https://www.saucedemo.com/', driver.current_url+' is not equal to https://www.saucedemo.com/')
        driver.quit()


class TestProductPage(unittest.TestCase):

    # Test-00D
    # This test the sorting in the product page
    # Input:
    #   Click in sort low to high
    # Expected output
    #   Items sorted from lower price to higher price

    def test_00D(self):
        driver = webdriver.Chrome(service=service_path, options=options)
        open_page(driver, 'https://www.saucedemo.com/')
        insert_text_by_CSS_SELECTOR(driver, 'input#user-name', 'standard_user')
        insert_text_by_CSS_SELECTOR(driver, 'input#password', 'secret_sauce')
        click_button_by_CSS_SELECTOR(driver, 'input#login-button')
        click_button_by_XPATH(driver, '/html/body/div/div/div/div[1]/div[2]/div[2]/span/select/option[3]')
        precio = getElements_by_CLASS_NAME(driver, 'inventory_item_price')
        sorted = True
        for i in range(0, len(precio)-1):
            if float(precio[i].text.replace('$','')) > float(precio[i+1].text.replace('$','')):
                sorted = False
        self.assertEqual(sorted, True, 'The prices are not sorted from low to high')
        driver.quit()

class TestShoppingCartPage(unittest.TestCase):

    # Test-00E
    # This test the addition of items to the shopping cart
    # Input:
    #   Add items to the shopping cart
    # Expected output
    #   Items are displayed in the shopping cart page

    def test_00E(self):
        driver = webdriver.Chrome(service=service_path, options=options)
        open_page(driver, 'https://www.saucedemo.com/')
        insert_text_by_CSS_SELECTOR(driver, 'input#user-name', 'standard_user')
        insert_text_by_CSS_SELECTOR(driver, 'input#password', 'secret_sauce')
        click_button_by_CSS_SELECTOR(driver, 'input#login-button')
        click_button_by_XPATH(driver, '/html/body/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/button')
        click_button_by_XPATH(driver, '/html/body/div/div/div/div[2]/div/div/div/div[6]/div[2]/div[2]/button')
        click_button_by_XPATH(driver, '/html/body/div/div/div/div[1]/div[1]/div[3]/a')
        items = getElements_by_CLASS_NAME(driver, 'inventory_item_name')
        items_added = True
        if(items[0].text != 'Sauce Labs Backpack' or items[1].text != 'Test.allTheThings() T-Shirt (Red)'):
            items_added = False
        self.assertEqual(items_added, True, 'Items were not added correctly')
        driver.quit()

    # Test-00F
    # This test the addition of items to the shopping cart
    # Input:
    #   Add item to the shopping cart
    # Expected output
    #   Item is displayed in the shopping cart page

    def test_00F(self):
        driver = webdriver.Chrome(service=service_path, options=options)
        open_page(driver, 'https://www.saucedemo.com/')
        insert_text_by_CSS_SELECTOR(driver, 'input#user-name', 'standard_user')
        insert_text_by_CSS_SELECTOR(driver, 'input#password', 'secret_sauce')
        click_button_by_CSS_SELECTOR(driver, 'input#login-button')
        click_button_by_XPATH(driver, '/html/body/div/div/div/div[2]/div/div/div/div[5]/div[2]/div[2]/button')
        click_button_by_XPATH(driver, '/html/body/div/div/div/div[1]/div[1]/div[3]/a')
        items = getElements_by_CLASS_NAME(driver, 'inventory_item_name')
        self.assertEqual(items[0].text, 'Sauce Labs Onesie', 'Item was not added correctly')
        driver.quit()

    # Test-00G
    # This test the checkout page
    # Input:
    #   Checkout the shopping cart
    # Expected output
    #   Checkout page is displayed

    def test_00G(self):
        driver = webdriver.Chrome(service=service_path, options=options)
        open_page(driver, 'https://www.saucedemo.com/')
        insert_text_by_CSS_SELECTOR(driver, 'input#user-name', 'standard_user')
        insert_text_by_CSS_SELECTOR(driver, 'input#password', 'secret_sauce')
        click_button_by_CSS_SELECTOR(driver, 'input#login-button')
        click_button_by_XPATH(driver, '/html/body/div/div/div/div[2]/div/div/div/div[5]/div[2]/div[2]/button')
        click_button_by_XPATH(driver, '/html/body/div/div/div/div[1]/div[1]/div[3]/a')
        items = getElements_by_CLASS_NAME(driver, 'inventory_item_name')
        click_button_by_CSS_SELECTOR(driver, 'button.btn btn_action btn_medium checkout_button')
        insert_text_by_CSS_SELECTOR(driver, 'input#first-name', 'Test_Name')
        insert_text_by_CSS_SELECTOR(driver, 'input#last-name', 'Test_Last_Name')
        insert_text_by_CSS_SELECTOR(driver, 'input#postal-code', 'Test_ZIP')
        click_button_by_CSS_SELECTOR(driver, 'input.submit-button btn btn_primary cart_button btn_action')
        self.assertEqual(driver.current_url, 'https://www.saucedemo.com/checkout-step-two.html',
                         driver.current_url + ' is not equal to https://www.saucedemo.com/checkout-step-two.html')
        driver.quit()

if __name__ == '__main__':
    unittest.main()



