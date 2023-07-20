import scrapy


class CompanySpider(scrapy.Spider):
    name = "company"
    allowed_domains = ["clutch.co"]
    start_urls = ["https://clutch.co/it-services"]

    def parse(self, response):
        pass
