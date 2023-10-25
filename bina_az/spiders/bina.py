import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime

class BinaSpider(CrawlSpider):
    name = "bina"
    allowed_domains = ["bina.az"]
    start_urls = ["https://bina.az/baki/alqi-satqi/obyektler"]

    rules = (
        Rule(LinkExtractor(allow=r"\?page=", deny_domains='ru.bina.az', deny='/?mobile_site'), follow=True),
        Rule(LinkExtractor(allow=r"items/\d+", deny_domains='ru.bina.az', deny='/?mobile_site'), callback="parse_item", follow=False)
    )

    def parse_item(self, response):
        item = {}
        item['Scraped Date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        item['title'] = response.xpath('//h1[@class="product-title"]/text()').get()
        item['price_value'] = response.xpath('//span[@class="price-val"]/text()').get()
        item['price_currency'] = response.xpath('//span[@class="price-cur"]/text()').get()
        item['url'] = response.url

        description = response.css('div.product-description__content')
        paragraphs = description.css('p')
        description_text = ''
        for paragraph in paragraphs:
            text = paragraph.css('::text').get()
            if text:
                description_text += text.strip() + '\n'
        # item['Description'] = description_text.strip()

        statistics = response.css('div.product-statistics__i')
        for stat in statistics:
            stat_text = stat.css('span.product-statistics__i-text::text').get()
            if stat_text:
                if "Yeniləndi:" in stat_text:
                    item['Last Updated'] = stat_text.replace('Yeniləndi: ', '').strip()
                elif "Baxışların sayı:" in stat_text:
                    item['Number of Views'] = stat_text.replace('Baxışların sayı: ', '').strip()

        # Extract owner's name and region from the product-owner__info
        owner_info = response.css('div.product-owner__info')
        owner_name = owner_info.css('div.product-owner__info-name::text').get()
        owner_region = owner_info.css('div.product-owner__info-region::text').get()
        item['Owner Name'] = ''
        item['Owner Region'] = ''

        if owner_name:
            item['Owner Name'] = owner_name.strip()
        if owner_region:
            item['Owner Region'] = owner_region.strip()

        # Extract the shop owner's name and region
        shop_owner_info = response.css('div.product-shop__owner-right')
        shop_owner_name = shop_owner_info.css('div.product-shop__owner-name::text').get()
        shop_owner_region = shop_owner_info.css('div.product-owner__info-region::text').get()
        item['Shop Owner Name'] = ''
        item['Shop Owner Region'] = ''

        if shop_owner_name:
            item['Shop Owner Name'] = shop_owner_name.strip()
        if shop_owner_region:
            item['Shop Owner Region'] = shop_owner_region.strip()

        residence_info = response.css('div.product-owner__residence-description')
        residence_name = residence_info.css('div.product-owner__residence-info-name::text').get()
        residence_region = residence_info.css('div.product-owner__residence-info-region::text').get()
        item['Residence Name'] = ''
        item['Residence Region'] = ''
        if residence_name:
            item['Residence Name'] = residence_name.strip()
        if residence_region:
            item['Residence Region'] = residence_region.strip()

        map_element = response.css('div#item_map')
        lng = map_element.attrib['data-lng']
        lat = map_element.attrib['data-lat']
        
        item['Longitude'] = lng
        item['Latitude'] = lat
        item['Kateqoriya'] = ''
        item['Mərtəbə'] = ''
        item['Sahə'] = ''
        item['Otaq sayı'] = ''
        item['Çıxarış'] = ''
        item['İpoteka'] = ''
        item['Təmir'] = ''
        item['propperties_len'] = 0

        # Props
        properties = response.css('div.product-properties__i')
        item['propperties_len'] = len(properties)
        for prop in properties:
            key = prop.xpath('label[@class="product-properties__i-name"]/text()').get()
            value = prop.xpath('span[@class="product-properties__i-value"]/text()').get()
            
            if key and value:
                key = key.strip()
                value = value.strip()
                item[key] = value

        # print(item.values())
        return item
