import glob
import pathlib

import rows
import scrapy
from rows.utils import open_compressed

from sc_parse_pdf import extract_table
from settings import DOWNLOAD_PATH, OUTPUT_PATH


class ExtraiBoletinsSpider(scrapy.Spider):

    name = "balneabilidade-sc-extrai-boletim"

    def start_requests(self):
        filename = glob.glob(str(OUTPUT_PATH / "sc-boletim.csv*"))[0]
        table = rows.import_from_csv(open_compressed(filename, mode="rb"))
        for row in table:
            row = row._asdict()
            pdf_url = row.pop("pdf_url")
            row["filename"] = (
                DOWNLOAD_PATH
                / f'SC/{row["ano"]}-{row["municipio_id"]}-{row["balneario_id"]}.pdf'
            )
            if not row["filename"].parent.exists():
                row["filename"].parent.mkdir()
            if not row["filename"].exists():
                url = pdf_url
            else:
                url = "file://" + str(row["filename"].absolute())
            yield scrapy.Request(url=url, meta=row, callback=self.parse_pdf)

    def parse_pdf(self, response):
        meta = response.request.meta
        filename = meta["filename"]
        for key in (
            "filename",
            "download_timeout",
            "download_slot",
            "download_latency",
            "depth",
        ):
            if key in meta:
                del meta[key]

        if not filename.exists():
            with open(filename, mode="wb") as fobj:
                fobj.write(response.body)

        result = extract_table(filename)
        if result is not None:
            for row in result:
                row.update(meta)
                yield row
