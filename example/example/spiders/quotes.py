import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["daraz.com.np"]
    start_urls = ["https://www.daraz.com.np/products/pack-of-12-6-pairs-women-velvet-fur-inside-winter-socks-by-comfy-multicolor-i128764809-s1036827837.html?spm=a2a0e.searchlistcategory.sku.1.6da35884orwa8M&search=1"]

    def parse(self, response):
        product_title = response.css('div.pdp-mod-product-badge-title span::text').get()
        product_price = response.css('div.pdp-product-price span.pdp-price::text').get()

        yield {
            'title': product_title,
            'price': product_price,
        }
