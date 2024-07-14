import allure


class AttachWeb:
    def __init__(self, driver):
        self.driver = driver

    def add_screenshot(self):
        png = self.driver.get_screenshot_as_png()
        allure.attach(
            body=png,
            name='screenshot',
            attachment_type=allure.attachment_type.PNG,
            extension='.png'
        )

    def add_logs(self):
        log = "".join(f'{text}\n' for text in self.driver.get_log(log_type='browser'))
        allure.attach(
            body=log,
            name='browser_logs',
            attachment_type=allure.attachment_type.TEXT,
            extension='.log'
        )

    def add_html(self):
        html = self.driver.page_source
        allure.attach(
            body=html,
            name='page_source',
            attachment_type=allure.attachment_type.HTML,
            extension='.html'
        )

    def add_html_xml(self):
        allure.attach(
            self.driver.page_source,
            name='add_html_xml',
            attachment_type=allure.attachment_type.XML
        )

    def add_video(self):
        video_url = "http://localhost:8080/video/" + self.driver.session_id + ".mp4"
        html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
               + video_url \
               + "' type='video/mp4'></video></body></html>"
        allure.attach(
            body=html,
            name='video_' + self.driver.session_id,
            attachment_type=allure.attachment_type.HTML,
            extension='.html')
