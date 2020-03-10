import scrapy
import os
import errno
from scrapy.http import Request


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ['bp.pep.com.cn']

    def start_requests(self):
        urls = [
            'http://bp.pep.com.cn/jc/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow pagination links
        for href in response.xpath('//a[not(contains(@href, ".pdf"))]'):
            yield response.follow(href, self.parse)
        # selector of pdf file.
        xpath = '//a[contains(@href, ".pdf")]/../..'
        for item in response.xpath(xpath):
            bookname = item.xpath('.//a/@title')[0].root
            yield Request(
                url=response.urljoin(item.xpath(
                    './/a[contains(@href, ".pdf")]').attrib['href']),
                callback=self.save_pdf,
                cb_kwargs=dict(filename='{}.pdf'.format(bookname))
            )

    def save_pdf(self, response, filename):
        """ Save pdf files """
        # path = response.url.split('/')[-1]
        path = "/".join(response.url.split('/')[4:6])+"/"+filename
        self.logger.info('Saving PDF %s', path)
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(path, "wb") as f:
            f.write(response.body)
