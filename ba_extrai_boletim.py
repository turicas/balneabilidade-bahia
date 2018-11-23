import csv
import glob
import io
from pathlib import Path

import scrapy
from rows.utils import open_compressed

from ba_parse_pdf import extract_table


DOWNLOAD_PATH = Path(__file__).parent / 'data/download'
OUTPUT_PATH = Path(__file__).parent / 'data/output'
if not DOWNLOAD_PATH.exists():
    DOWNLOAD_PATH.mkdir()


class ExtraiBoletins(scrapy.Spider):

    name = 'balneabilidade-ba-extrai-boletim'

    def start_requests(self):

        filename = glob.glob(str(OUTPUT_PATH / 'ba-boletim.csv*'))[0]
        fobj = open_compressed(filename, encoding='utf8')
        for row in csv.DictReader(fobj):
            filename = DOWNLOAD_PATH / f'BA/{row["id_campanha"]}.pdf'
            if not filename.parent.exists():
                filename.parent.mkdir()
            row['filename'] = filename
            if filename.exists():
                url = 'file://' + str(filename.absolute())
            else:
                url = row['url']

            yield scrapy.Request(url=url, meta=row)

    def parse(self, response):
        meta = response.request.meta.copy()
        filename = meta['filename']
        meta['costa_menu'] = meta['costa']
        del_keys = [key for key in meta.keys()
                    if key.startswith('download_')
                    or key in ('url', 'filename', 'depth', 'costa')]
        for key in del_keys:
            del meta[key]
        if not filename.exists():
            with open(filename, mode='wb') as fobj:
                fobj.write(response.body)

        for row in extract_table(io.BytesIO(response.body)):
            row.update(meta)
            yield row
