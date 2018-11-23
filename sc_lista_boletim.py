import scrapy


class BalneabilidadeSCSpider(scrapy.Spider):

    name = "balneabilidade-sc-lista-boletim"

    def start_requests(self):
        yield scrapy.Request(
            "http://www.fatma.sc.gov.br/laboratorio/dlg_balneabilidade2.php",
            callback=self.parse_selects,
        )

    def parse_selects(self, response):
        anos = response.xpath('//select[@id="combo_ano"]/option/text()').extract()
        for municipio_option in response.xpath(
            '//select[@id="combo_municipio"]/option'
        ):
            municipio_id = municipio_option.xpath("./@value").extract_first()
            municipio_nome = municipio_option.xpath("./text()").extract_first()
            meta = {
                "anos": anos,
                "municipio_id": municipio_id,
                "municipio_nome": municipio_nome,
            }
            yield scrapy.Request(
                f"http://www.fatma.sc.gov.br/laboratorio/gravar.php?operacao=selecionarBalnearios&oid={municipio_id}",
                meta=meta,
                callback=self.parse_balnearios,
            )

    def parse_balnearios(self, response):
        meta = response.request.meta
        data = response.body_as_unicode().strip().split("|")[1:]
        for balneario_id, balneario_nome in zip(data[::2], data[1::2]):
            for ano in meta["anos"]:
                pdf_url = f'http://www.fatma.sc.gov.br/laboratorio/relatorio_ficha2.php?simplificado=1&where=0&d1={ano}-01-01&d2={ano}-12-31&mc={meta["municipio_id"]}&pc={balneario_id}'
                yield {
                    "ano": ano,
                    "balneario_id": balneario_id,
                    "balneario_nome": balneario_nome,
                    "municipio_id": meta["municipio_id"],
                    "municipio_nome": meta["municipio_nome"],
                    "pdf_url": pdf_url,
                }
