from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class MyLiveServerTestCase(LiveServerTestCase):    
    """
    BaseCleass for my selenium test cases
    """
    fixtures = ['test_data.json']

    def setUp(self):
        self.driver = WebDriver()
        self.url = self.live_server_url    

    def tearDown(self):

        self.driver.quit()


class LoginTest(MyLiveServerTestCase):
    """
    Test the following user story:
      - go to main page
      - go to edit page
      - edit data
      - return to main page
      - see data changed 
    """

    def test_valid_data(self):
        """
        test when user enters correct data
        """
        # import pdb; pdb.set_trace()
        self.driver.get(self.url)

        
        assert "Main Page" in self.driver.title
        elem = self.driver.find_element_by_name("login_page_link")
        elem.click()
        assert "Login Page" in self.driver.title

        elem = self.driver.find_element_by_id("id_username")
        elem.clear()
        elem.send_keys("leela")

        elem = self.driver.find_element_by_id("id_password")
        elem.clear()
        elem.send_keys("leela")

        elem = self.driver.find_element_by_name("login_submit")
        elem.click()
        assert "Main Page" in self.driver.title
        assert "Name: Leela" in self.driver.page_source

class AdminEditFormTest(MyLiveServerTestCase):
    """
    Test the following user story:
      - go to main page
      - go to edit page
      - edit data
      - return to main page
      - see data changed 
    """

    def test_valid_data(self):
        """
        test when user enters correct data
        """
        self.driver.get(self.url)

        assert "Main Page" in self.driver.title
        elem = self.driver.find_element_by_name("edit_page_link")
        elem.click()
        assert "Edit Page" in self.driver.title
        elem = self.driver.find_element_by_id("id_name")
        elem.clear()
        elem.send_keys("NewValue")
        elem = self.driver.find_element_by_name("save_and_back_submit")
        elem.click()
        # assert ("..." in elem.get_attribute("value")) or \
          # (":)" in elem.get_attribute("value"))
        

    # def test_invalid_data(self):
    #     """ test when user enters INcorrect data """
    #     self.driver.get(self.url)
    #     assert "Main Page" in self.driver.title
    #     elem = self.driver.find_element_by_name("edit_page_link")
    #     elem.click()
    #     assert "Edit Page" in self.driver.title
    #     elem = self.driver.find_element_by_id("id_email")
    #     elem.clear()
    #     elem.send_keys("BadEmail")
    #     elem = self.driver.find_element_by_name("save_and_back_submit")
    #     elem.click()
    #     assert "Edit Page" in self.driver.title