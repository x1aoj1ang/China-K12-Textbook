import scrapy
import os
import errno

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
		# path = response.url.split('/')[-1]
		path =  "/".join(response.url.split('/')[4:6])+"/"+filename;
		self.logger.info('Saving PDF %s', path);
		if not os.path.exists(os.path.dirname(path)):
			try:
				os.makedirs(os.path.dirname(path))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		with open(path, "wb") as f:
			f.write(response.body);

			
