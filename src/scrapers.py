import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class BaseScraper:

    timeout = 2

    def setupDriver(self):
        self.driver = webdriver.Chrome()

    def closeDriver(self):
        self.driver.quit()

    def get_data(self):
        raise NotImplementedError


def extract_from_list(item, name):
    span = item.find_element_by_tag_name("span").text
    if name in span.lower():
        return item.find_element_by_tag_name("strong").text
    else:
        return None


class VehicleEnquiryScraper(BaseScraper):

    def get_data(self, vrn, make):
        driver = self.driver
        driver.get("https://www.vehicleenquiry.service.gov.uk")

        # Submit vrn and make
        driver.find_element_by_id("Vrm").send_keys(vrn)
        driver.find_element_by_id("Make").send_keys(make)
        driver.find_element_by_id("Search").click()

        try:
            # Wait until page loads and we can see the registrationNumber box.
            reg_mark = WebDriverWait(driver, self.timeout).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "registrationNumber")
                )
            ).text
            # Collect vehicle details
            try:
                valid_tax = True
                tax_text = driver.find_element_by_class_name(
                    "isValidTax"
                ).find_element_by_tag_name("p").text
                tax_expiry_date = tax_text[9:]
            except NoSuchElementException:
                valid_tax = None
                tax_expiry_date = None

            try:
                valid_mot = True
                mot_text = driver.find_element_by_class_name(
                    "isValidMot"
                ).find_element_by_tag_name("p").text
                if mot_text.startswith("No details"):
                    mot_expiry_date = None
                else:
                    mot_expiry_date = mot_text[9:]
            except NoSuchElementException:
                valid_mot = None
                mot_expiry_date = None

            payload = {
                "regMark": reg_mark,
                "make": make,
                "validMot": valid_mot,
                "motExpiryDt": mot_expiry_date,
                "validTax": valid_tax,
                "taxExpiryDt": tax_expiry_date,
            }

            list_items = driver.find_element_by_class_name("ul-data").find_elements_by_tag_name("li")
            labels = [
                "make", "registration", "manufacture", "capacity", "emissions",
                "fuel", "status", "colour", "approval", "wheelplan", "weight"
            ]
            for item in list_items:
                for label in labels:
                    extracted = extract_from_list(item, label)
                    if extracted is not None:
                        payload[label] = extracted

            return payload
        except TimeoutException:
            print("TimeoutException", sys.exc_info()[0])
            return {'error': 'The request timed out'}
