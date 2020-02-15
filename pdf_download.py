import scrapy

from scrapy.http import Request

class PdfDownloader(scrapy.Spider):
	name = 'pdf_downloader'
	# domain URL
	allowed_domains = ['bp.pep.com.cn']
	# links to the specific pages
	start_url = 'http://bp.pep.com.cn/jc/'
	start_urls = ['http://bp.pep.com.cn/jc/ywjygjkcjc/']


	def parse(self, response):
		# selector of pdf file.
		xpath = '//a[contains(@href, ".pdf")]/../..'
		for item in response.xpath(xpath):
			bookname = item.xpath('.//a/@title')[0].root
			yield Request(
				url=response.urljoin(item.xpath('.//a[contains(@href, ".pdf")]').attrib['href']),
				callback=self.save_pdf,
				cb_kwargs=dict(filename='{}.pdf'.format(bookname))
			)


	def save_pdf(self, response, filename):
		""" Save pdf files """
		path = response.url.split('/')[-1]
		self.logger.info('Saving PDF %s', path+filename);
		with open(filename, 'wb') as file:
			file.write(response.body);
