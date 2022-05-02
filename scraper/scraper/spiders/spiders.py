import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.loader import ItemLoader
from scraper.items import ScraperItem


class MicroplaySpider(scrapy.Spider):
    name = "microplay"
    start_urls = [
        "https://www.microplay.cl/productos/juegos",
        "https://www.microplay.cl/productos/gamer",
        "https://www.microplay.cl/productos/geek",
        "https://www.microplay.cl/productos/computacion",
        "https://www.microplay.cl/productos/audiovideo",
        "https://www.microplay.cl/productos/juguetes",
        "https://www.microplay.cl/productos/juegosdemesa",
        "https://www.microplay.cl/productos/preventas/juegos",
        "https://www.microplay.cl/productos/ofertas"
    ]
    chrome_options = ChromeOptions()
    chrome_options.headless = True

    def start_requests(self):
        btn_xpath = ".//a[@class='load']"
        card_xpath = ".//div[@class='card__item']/a"

        for url in self.start_urls:
            driver = Chrome(options=self.chrome_options)
            wait = WebDriverWait(driver, 10)
            driver.get(url)

            # LOAD ITEMS
            while True:
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
                    driver.find_element_by_xpath(btn_xpath).click()
                except Exception as exce:
                    print(exce)
                    break

            # ITEMS LINKS
            products = driver.find_elements(by=By.XPATH, value=card_xpath)

            for prod in products:
                prod_url = prod.get_attribute("href")
                yield scrapy.Request(prod_url)

        driver.quit()

    def parse(self, response, **kwargs):
        loader = ItemLoader(item=ScraperItem(), selector=response)
        loader.add_xpath("name", ".//section[contains(@class, 'content__ficha')]/h1/text()")
        loader.add_xpath("price", ".//span[@class='text_web']/strong")
        loader.add_value("url", response.request.url)
        loader.add_xpath("description", ".//div[@id='box-descripcion']")

        yield loader.load_item()
