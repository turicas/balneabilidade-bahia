import io
import logging
import re

import rows


logging.getLogger("pdfminer").setLevel(logging.ERROR)
regexp_costa = re.compile("[ -]([A-Z]{3,4})[ -]")


def clean(text):
    return text.replace("\n", " ").strip()


def extrai_costa(ponto):
    """
    >>> extrai_costa('2ª. Praia de Morro de São Paulo - CDD- SP 200')
    'CDD'
    >>> extrai_costa('Costa - Canavieiras - CCA CN 100')
    'CCA'
    >>> extrai_costa('Madre de Deus - BTS MD 100')
    'BTS'
    >>> extrai_costa('Nativos - CDES NT 100')
    'CDES'
    """

    return regexp_costa.findall(ponto)[0]


def extract_table(fobj):
    table = rows.import_from_pdf(fobj, backend="pymupdf")
    result = []
    for row in table:
        row = row._asdict()
        row["local_da_coleta"] = clean(row["local_da_coleta"])
        row["ponto_codigo"] = clean(row["ponto_codigo"])
        row["costa_ponto"] = extrai_costa(row["ponto_codigo"])
        result.append(row)
    return result
