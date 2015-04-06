
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class MyLiveServerTestCase(LiveServerTestCase):    
    """
    BaseCleass for my selenium test cases
    """
    pass
    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = WebDriver()
    #     cls.url = cls.live_server_url    

    #     super(MyLiveServerTestCase, cls).setUpClass()

    # @classmethod
    # def tearDownClass(cls):
    #     cls.driver.quit()
    #     # from psutil import process_iter
    #     # from signal import SIGTERM # or SIGKILL

    #     # for proc in process_iter():
    #     #     print proc
    #     #     for conns in proc.connections(kind='inet'):
    #     #         if conns.laddr[1] == 8081:
    #     #             import pdb; pdb.set_trace()
    #     #             proc.send_signal(SIGTERM) # or SIGKILL
    #     #             continue

    #     super(MyLiveServerTestCase, cls).tearDownClass()


    

class LoginTest(MyLiveServerTestCase):

    def setUp(self):
        self.driver = WebDriver()
        self.url = self.live_server_url    

    def tearDown(self):
        self.driver.quit()

    """
    Test the following user story:
      - go to main page
      - go to edit page
      - edit data
      - return to main page
      - see data changed 
    """

    # def setUp(self):        
    #     self.driver = WebDriver()
    #     self.url = self.live_server_url    

    def test_valid_data(self):
        """
        test when user enters correct data
        """
        # import pdb; pdb.set_trace()
        self.driver.get(self.url)
        print self.driver.title
        
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


    def setUp(self):
        self.driver = WebDriver()
        self.url = self.live_server_url    

    def tearDown(self):
        self.driver.quit()

    # def setUp(self):    
    #     self.driver = WebDriver()
    #     self.url = self.live_server_url    

        # self.driver = webdriver.Firefox()
        # self.url = "http://127.0.0.1:8000/"

    def test_valid_data(self):
        """
        test when user enters correct data
        """
        self.driver.get(self.url)
        print self.driver.title
        assert "Main Page" in self.driver.title
        elem = self.driver.find_element_by_name("edit_page_link")
        elem.click()
        assert "Edit Page" in self.driver.title
        elem = self.driver.find_element_by_id("id_name")
        elem.clear()
        elem.send_keys("NewValue")
        elem = self.driver.find_element_by_name("save_and_back_submit")
        elem.click()
        assert ("..." in elem.get_attribute("value")) or \
          (":)" in elem.get_attribute("value"))
        

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
        
    # def tearDown(self):
    #     self.driver.close()
    #     self.driver.quit()
        # print dir(self.driver)