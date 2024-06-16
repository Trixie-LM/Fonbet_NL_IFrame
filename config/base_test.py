from fonbet_test_project.pages.lottery_page import Lottery
from fonbet_test_project.pages.main_page import MainPage
from fonbet_test_project.utils.attach_web import AttachWeb


class BaseTest(Lottery, MainPage, AttachWeb):
    def __init__(self, driver, wait, action):
        super().__init__(driver, wait, action)
        self.driver = driver
        self.wait = wait
        self.action = action
