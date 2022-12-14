import scrapy, tldextract, os
from urllib.parse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import candidateLanguageProcessor

class CandidateSpider(CrawlSpider):
    name = "issues"
    allowed_domains = ['nicolemalliotakis.com', 'maxroseforcongress.com', 'zeldinfornewyork.com', 'kathyhochul.com', 'jamesforny.com', 'michaelhenryforag.com']
    start_urls = ['https://nicolemalliotakis.com/', 'https://www.maxroseforcongress.com/', 'https://zeldinfornewyork.com/', 'https://kathyhochul.com/', 'https://www.jamesforny.com/', 'https://michaelhenryforag.com']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        domain = tldextract.extract(response.url)
        with open('/Users/nicholas.palermo/Desktop/CSC450/candidateSites/' + domain.registered_domain + '.txt', 'a') as f:
            f.write(' '.join(response.css('title::text').getall()).strip())
            f.write(' '.join(response.css('body::text').getall()).strip())
            f.write(' '.join(response.css('h1::text').getall()).strip())
            f.write(' '.join(response.css('h2::text').getall()).strip())
            f.write(' '.join(response.css('h3::text').getall()).strip())
            f.write(' '.join(response.css('h4::text').getall()).strip())
            f.write(' '.join(response.css('h5::text').getall()).strip())
            f.write(' '.join(response.css('h6::text').getall()).strip())
            f.write(' '.join(response.css('p::text').getall()).strip())
            f.write(' '.join(response.css('div::text').getall()).strip())
            f.write(' '.join(response.css('span::text').getall()).strip())
            f.write(' '.join(response.css('strong::text').getall()).strip())
            f.write(' '.join(response.css('em::text').getall()).strip())
            f.write(' '.join(response.css('br::text').getall()).strip())
            f.write(' '.join(response.css('br::text').getall()).strip())