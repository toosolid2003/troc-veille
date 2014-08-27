import scrapy

class trocSpider(scrapy.Spider):
    name = "troc"
    allowed_domains = ["trocdestrains.org"]
    start_urls = [
        "http://trocdestrains.com/?choix=rech_evidence&tri_col=ville_dep&tri_sens=ASC"
    ]

    def parse(self, response):
        gares = response.xpath('//span[@class="gare-rech"]/text()').extract()
        date = response.xpath('//span[@class="date"]/text()').extract()
        prix = response.xpath('//span[@class="prix"]/text()').extract()
        heureDep = response.xpath('//span[@class="heure-rech"]/text()').extract()
        print gares, date, prix