import scrapy
from scrapy_playwright.page import PageMethod


class PwspiderSpider(scrapy.Spider):
    name = "pwspider"
    page_number = 1

    def start_requests(self):
        yield scrapy.Request(
                #'https://www.boliga.dk', 
                #'https://www.boliga.dk/kortsoegning?latMin=53,199164503683036&latMax=56,603432577328334&lonMin=5,438503835985483&lonMax=17,949783740390266&sort=street-a&pageSize=500',
                #'https://www.boliga.dk/resultat',
                f'https://www.boliga.dk/resultat?page={PwspiderSpider.page_number}',
                meta = {
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_coroutines': [
                        PageMethod('wait_for_load_state','domcontentloaded')
                        ]
                    }
                )

    async def parse(self, response):
        items = {}
        addressZipCode = response.css('div.secondary-value.d-flex.flex-wrap span::text').getall()
        prices = response.css('div.primary-value.d-flex.justify-content-end::text').getall()
        items['addressZipCode'] = addressZipCode
        items['prices'] = prices
        yield items


        if PwspiderSpider.page_number <= 10:
            PwspiderSpider.page_number += 1
            next_page = f'https://www.boliga.dk/resultat?page={PwspiderSpider.page_number}'
            yield response.follow(next_page, callback = self.parse)

            
