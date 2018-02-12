import scrapy
from bs4 import BeautifulSoup

from camprice.items import Thread

from scrapy.loader.processors import Join, MapCompose

from scrapy.loader import ItemLoader
from scrapy.selector import Selector

class ClubsnapSpider1(scrapy.Spider):
    name = "clubsnap1"
    def start_requests(self):
        urls = [
            'http://www.clubsnap.com/forums/forumdisplay.php?f=180',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split(".php")[-1]
        filename = 'html/clubsnap-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        for thread in response.css('.threadtitle a.title').extract():
            if "WTSell" in thread:
                soup = BeautifulSoup(thread)
                thread_text = soup.a.string
                for link in soup.find_all('a'):
                    thread_url = "http://www.clubsnap.com/forums/" + link.get('href')

                yield {
                    'action': str(thread_text).split(":")[-2],
                    'item_type': str(thread_text).split(": ")[1].split(" -")[-2],
                    'title': str(thread_text).split(" - ")[1],
                    'url': str(thread_url)
                }

        next_page = response.css("span.prev_next a::attr(href)").extract_first()
        print("Next Page: " + next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class ClubsnapSpider(scrapy.Spider):

    name = "clubsnap2"
    allowed_domains = ["www.clubsnap.com"]
    start_urls = [
        "http://www.clubsnap.com/forums/forumdisplay.php?f=102",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=104",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=111",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=180",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=113",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=115",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=118",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=119",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=120",
        "http://www.clubsnap.com/forums/forumdisplay.php?f=117"
        ]

    thread_list_xpath = '//div[@class="inner"]'
    item_fields = {
        'thread_id': './/a[@class="title"]/@href',
        'title': './/a[@class="title"]/text()',
        'link': './/a[@class="title"]/@href',
        'username': './/a[@class="username understate"]/text()',
    }



    def parse_page1(self, response):
        item = MyItem()
        item['main_url'] = response.url
        request = scrapy.Request("http://www.example.com/some_page.html",
                         callback=self.parse_page2)
        request.meta['item'] = item
        return request

    def parse_page2(self, response):
        item = response.meta['item']
        item['other_url'] = response.url
        return item


    def parse_details(self, response):
        print("YOOOHOOOOO")
        return

    def parse(self, response):
        selector = Selector(response)

        # iterate over deals
        for thread in selector.xpath(self.thread_list_xpath):
            print("Thread: " + str(thread))
            #print("Link to Follow: " + ''.join(thread.xpath('.//a[@class="title"]/@href').extract()))
            loader = ItemLoader(item=Thread(), selector=thread)
            # define processors
            loader.default_input_processor = MapCompose(str.strip)
            loader.default_output_processor = Join()

            thread_url= 'http://www.clubsnap.com/forums/' + ''.join(thread.xpath('.//a[@class="title"]/@href').extract())

            thread_detail = scrapy.Request(thread_url, callback=self.parse_details)

            # iterate over fields and add xpaths to the loader
            for field, xpath in self.item_fields.items():
                print("Load: " + field + " " + xpath)
                loader.add_xpath(field, xpath)
            yield loader.load_item()

        # follow next page links
        if response.css("a[rel='next']::attr(href)").extract():
            next_page = 'http://www.clubsnap.com/forums/' + response.css("a[rel='next']::attr(href)").extract()[0]
            print("NEXT PAGE: " + next_page)

            yield scrapy.Request(
                next_page,
                callback=self.parse,
                dont_filter = True
            )
