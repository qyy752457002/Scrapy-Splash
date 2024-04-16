import scrapy
from scrapy_splash import SplashRequest
from splash_project.items import SplashProjectItem

class AdamchoiSpider(scrapy.Spider):
    name = 'adamchoi'
    allowed_domains = ['www.adamchoi.co.uk']
    # start_urls = ['http://www.adamchoi.co.uk/']

    # Copy and paste the lua code written in splash inside the script variable
    script = '''
        function main(splash, args)

          splash: on_request(function(request)
          request: set_header('User-Agent',
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
          end)
          splash.private_mode_enabled = false
          assert(splash:go(args.url))
          assert(splash:wait(3))
          all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
          all_matches[2]:mouse_click()
          assert(splash:wait(3))
          splash:set_viewport_full()
          return {splash:png(), splash:html()}
        end
    '''

    # lua code for url directing to new page
    new_script = '''

    ''' 

    # Define a start_requests function to connect scrapy and splash
    def start_requests(self):
        yield SplashRequest(url='https://www.adamchoi.co.uk/overs/detailed', callback=self.parse, endpoint='render.html', args={'lua_source':self.script})

    # As usual, we use the parse function to extract data with xpaths
    def parse(self, response):

        png_data = response.body

        # Saving PNG data to a file
        if png_data:
            with open('./screenshot.png', 'wb') as f:
                f.write(png_data)

        rows = response.xpath('//tr')

        for row in rows:
            date = row.xpath('./td[1]/text()').get()
            home_team = row.xpath('./td[2]/text()').get()
            score = row.xpath('./td[3]/text()').get()
            away_team = row.xpath('./td[4]/text()').get()

            Item = SplashProjectItem(date=date, home_team=home_team, score=score, away_team=away_team)

            yield Item

            '''
                VERY IMPORTANT! Assuming we can extract new URLs from current page

                Extracting new URLs from rows and sending new requests with different Lua script
            '''
            # new_url = row.xpath('YOUR_XPATH_TO_EXTRACT_URL').get()  

            # if new_url:
            #     yield SplashRequest(url=response.urljoin(new_url), callback=self.parse_new_page, endpoint='execute', args={'lua_source': self.new_script})

    def parse_new_page(self, response):
        # Parsing logic for new page goes here
        pass