import scrapy

from empoweredautoparts.items import EmpoweredautopartsItem
from empoweredautoparts.scraping_utility import process_description

class EmpoweredautopartsSpider(scrapy.Spider):
    name = "empoweredautoparts"
    allowed_domains = ["empoweredautoparts.com.au"]

    start_urls = ["https://www.empoweredautoparts.com.au/"]

    def start_requests(self):
        start_url = "https://www.empoweredautoparts.com.au/"

        # for url in urls:
        yield scrapy.Request(url=start_url, callback=self.inititialize)

    def inititialize(self, response):
        for url in response.css('ul.nav.navbar-nav.mega-menu').css('ul.dropdown-menu.dropdown-menu-horizontal> li > a::attr(href)').extract():
            url = response.urljoin(url)
            yield response.follow(url, callback=self.parse_products)

    def parse_products(self, response):
        for product_url in response.css('div.caption > span > a::attr(href)').extract():
            product_url = response.urljoin(product_url)
            yield response.follow(product_url, callback=self.parse_details, meta={"product_url": product_url})

        next_page_urls = response.css('ul.pagination > li > a::attr(href)').extract()
        if len(next_page_urls) != 0:
            next_page_url = response.urljoin(next_page_urls[-1])
            yield scrapy.Request(url=next_page_url, callback=self.parse_products)

    def parse_details(self, response):
        item = EmpoweredautopartsItem()

        item['product_url'] = response.meta["product_url"]
        item['product_name'] = response.css('div.wrapper-product-title > h1::text').extract_first()
        item['sku'] = response.css('div.wrapper-product-title > span::text').extract_first()[5:] #'SKU: 76036'
        item['current_price'] = response.css('div.productprice.productpricetext::text').extract_first().replace('\n', '') #'\n$204.86\n'
        if response.css('div.productrrp.text-muted::text').extract_first() is None:
            item['actual_price'] = item['current_price']
        else:
            item['actual_price'] = response.css('div.productrrp.text-muted::text').extract_first().replace('\n', '')[4:]   #'\nRRP $235.50\n'

        images_str = str(response.urljoin(response.css('div.main-image.text-center > a::attr(href)').extract_first()))
        for remaining_image in response.css('div.col-xs-3 >  a::attr(href)').extract(): #is an array
            images_str = images_str + ',' + str(response.urljoin(remaining_image))
        item['images'] = images_str

        item = process_description(item, response.xpath('.//div[@class="productdetails open"]/*').extract())

        item['specification'] = response.css('table.table').extract_first()
        yield item


