#-*- coding:utf-8 -*
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class CamaraSpider(BaseSpider):

    name = 'camara.gov.br'
    allowed_domains = ['camara.gov.br']
    start_urls = ['http://www.camara.gov.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?txOrador=&txPartido=&txUF=&dtInicio=01%2F01%2F1974&dtFim=30%2F12%2F1984&txTexto=&txSumario=&basePesq=plenario&CampoOrdenacao=dtSessao&PageSize=50&TipoOrdenacao=DESC&btnPesq=Pesquisar']
    #rules = [Rule(SgmlLinkExtractor(restrict_xpaths="//div[@class='listingBar']/span/a[@title='Próxima Página']", 'parse_discursos')]

    def parse_discursos(self, response):
        x = HtmlXPathSelector(response)
        discursos =  x.select("//table[@class='tabela-1 variasColunas']/tbody/tr")
        for d in discursos:
            discurso = DiscursoItem()
            discurso['data'] = d.select("./td")[0].select("./text()").extract()
            discurso['sessao'] = d.select("./td")[1].select("./text()").extract()
            discurso['fase'] = d.select("./td")[2].select("./text()").extract()
            discurso['discurso'] = ''
            discurso['sumario'] = ''
            discurso['orador'] = d.select("./td")[5].select("./text()").extract()
            discurso['partido'] = ''
            discurso['estado'] = ''
            discurso['hora'] = d.select("./td")[6].select("./text()").extract()
            discurso['publicacao'] = d.select("./td")[7].select("./a/@onclick").extract()