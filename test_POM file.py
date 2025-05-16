import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[@type='submit']")

    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.username_input)).send_keys(username)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.password_input)).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.login_button)).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.pim_menu_item = (By.XPATH, "//span[text()='PIM']")
        self.user_dropdown = (By.CSS_SELECTOR, "p[class='oxd-userdropdown-name']")
        self.logout_link = (By.XPATH, "//a[text()='Logout']")

    def hover_and_click_pim(self):
        pim_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.pim_menu_item))
        actions = ActionChains(self.driver)
        actions.move_to_element(pim_element).click().perform()

    def click_user_dropdown(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.user_dropdown)).click()

    def click_logout(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.logout_link)).click()

    def logout(self):
        self.click_user_dropdown()
        self.click_logout()

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_employee_button = (By.XPATH, "//button[normalize-space()='Add']")

    def click_add_employee(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_employee_button)).click()

class AddEmployeePage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name_input = (By.NAME, "firstName")
        self.middle_name_input = (By.NAME, "middleName")
        self.last_name_input = (By.NAME, "lastName")
        self.save_button = (By.XPATH, "//button[@type='submit']")

    def enter_first_name(self, first_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.first_name_input)).send_keys(first_name)

    def enter_middle_name(self, middle_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.middle_name_input)).send_keys(middle_name)

    def enter_last_name(self, last_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.last_name_input)).send_keys(last_name)

    def click_save(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.save_button)).click()

    def add_employee(self, first_name, middle_name, last_name):
        self.enter_first_name(first_name)
        self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)
        self.click_save()

class EmployeeListPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_button = (By.XPATH, "//div[@class='orangehrm-header-container']/button[normalize-space()='Add']")
        self.search_input = (By.XPATH, "//div[@class='oxd-table-filter-area']//input[@placeholder='Type for hints...']")
        self.autocomplete_suggestion = (By.XPATH, "//div[@class='oxd-autocomplete-dropdown --positon-bottom']//span")
        self.search_button = (By.XPATH, "//div[@class='oxd-table-filter-area']//button[@type='submit']")
        self.employee_record_locator = "//div[@class='oxd-table-card']//div[contains(., '{}')]"

    def click_add(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_button)).click()

    def enter_employee_name_for_search(self, name_prefix):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.search_input)).send_keys(name_prefix)

    def select_autocomplete_suggestion(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.autocomplete_suggestion)).click()

    def click_search(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.search_button)).click()

    def verify_employee_present(self, full_name):
        locator = (By.XPATH, self.employee_record_locator.format(full_name))
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            print(f"Name Verified: {full_name} found in the list.")
            return True
        except:
            print(f"Verification Failed: {full_name} not found in the list.")
            return False


class OrangeHRMTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.pim_page = PIMPage(self.driver)
        self.add_employee_page = AddEmployeePage(self.driver)
        self.employee_list_page = EmployeeListPage(self.driver)


        self.login_page.login("Admin", "admin123")
        WebDriverWait(self.driver, 10).until(EC.url_contains("dashboard"))

    def test_add_and_verify_employees(self):
        self.dashboard_page.hover_and_click_pim()
        WebDriverWait(self.driver, 10).until(EC.url_contains("pim"))

        # Add Employees
        employees_data = [
            {"first_name": "Annie", "middle_name": "K", "last_name": "Kumar"},
            {"first_name": "Sneha", "middle_name": "P", "last_name": "Naik"},
            {"first_name": "Neha", "middle_name": "C", "last_name": "Das"},

        ]

        for emp_data in employees_data:
            self.pim_page.click_add_employee()
            self.add_employee_page.add_employee(
                emp_data["first_name"], emp_data["middle_name"], emp_data["last_name"]
            )
            WebDriverWait(self.driver, 10).until(EC.url_contains("pim/viewEmployeeList"))
            self.pim_page.click_add_employee() # Click Add again for the next employee
            WebDriverWait(self.driver, 10).until(EC.url_contains("pim/addEmployee"))

        # Navigate to Employee List
        self.dashboard_page.hover_and_click_pim() # Navigate back to PIM
        WebDriverWait(self.driver, 10).until(EC.url_contains("pim"))
        self.driver.find_element(*self.employee_list_page.add_button).click() # Click Add to see the list link
        self.driver.find_element(By.XPATH, "//a[text()='Employee List']").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("pim/viewEmployeeList"))

        # Verify Employees
        for emp_data in employees_data:
            full_name = f"{emp_data['first_name']} {emp_data['middle_name']} {emp_data['last_name']}"
            self.employee_list_page.enter_employee_name_for_search(emp_data["first_name"][:4])
            self.employee_list_page.select_autocomplete_suggestion()
            self.employee_list_page.click_search()
            self.employee_list_page.verify_employee_present(full_name)
            self.driver.find_element(By.XPATH, "//button[normalize-space()='Reset']").click()
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='oxd-loading-spinner']"))) # Wait for reset

    def tearDown(self):
        self.dashboard_page.logout()
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()