import re
from collections import OrderedDict

import rows


FIELDS = OrderedDict(
    [
        ("data", rows.fields.TextField),
        ("hora", rows.fields.TextField),
        ("vento", rows.fields.TextField),
        ("mare", rows.fields.TextField),
        ("chuvas_ultimas_24h", rows.fields.TextField),
        ("temp_ar_celsius", rows.fields.TextField),
        ("temp_agua_celsius", rows.fields.TextField),
        ("ecoli", rows.fields.TextField),
        ("condicao", rows.fields.TextField),
    ]
)
regexp_ponto_referencia = re.compile(
    r"ponto de coleta: (.*)\s+referência: (.*)", flags=re.IGNORECASE
)
regexp_municipio_local = re.compile(
    r"município\.+: (.*)\s+local: (.*)", flags=re.IGNORECASE
)
starts_after = re.compile(r".*Condição.*")
ends_before = re.compile(r"Página [0-9]+")


class PtBrDateField(rows.fields.DateField):
    INPUT_FORMAT = "%d/%m/%Y"


def extract_page_metadata(page_text):
    municipio_local = regexp_municipio_local.findall(page_text)
    ponto_de_coleta_referencia = regexp_ponto_referencia.findall(page_text)
    if not municipio_local or not ponto_de_coleta_referencia:
        return None
    else:
        return {
            "municipio": municipio_local[0][0],
            "local": municipio_local[0][1],
            "ponto_de_coleta": ponto_de_coleta_referencia[0][0],
            "referencia": ponto_de_coleta_referencia[0][1],
        }


class YGroupsXPositionAlgorithm(rows.plugins.pdf.YGroupsAlgorithm):

    name = "y-groups-x-position"

    def get_lines(self):
        positions = [  # Must be in order
            (35, "data"),
            (100, "hora"),
            (160, "vento"),
            (210, "mare"),
            (280, "chuvas_ultimas_24h"),
            (335, "temp_ar_celsius"),
            (370, "temp_agua_celsius"),
            (430, "ecoli"),
            (550, "condicao"),
        ]
        for line in super().get_lines():
            line_data = {key: [] for key in FIELDS.keys()}
            for cell in line:
                if not cell:
                    continue
                selected_key = None
                cell_x0 = min(obj.x0 for obj in cell)
                for max_x0, key in positions:
                    if cell_x0 < max_x0:
                        selected_key = key
                        break
                if selected_key is None:
                    raise RuntimeError(f"ERROR selecting object from cell {cell}")
                line_data[selected_key] = cell
            yield [line_data[key] for key in FIELDS.keys()]


def convert_row(row):
    row = row._asdict()
    hour = row.pop("hora")
    if not hour:
        hour = "00:00:00"
    row["datahora"] = str(PtBrDateField.deserialize(row.pop("data"))) + "T" + hour
    return row


def extract_table(filename_or_fobj):
    total_pages = rows.plugins.pdf.number_of_pages(filename_or_fobj, backend="pymupdf")
    result = []
    for page_number in range(1, total_pages + 1):
        page_text = next(
            rows.plugins.pdf.pdf_to_text(
                filename_or_fobj, page_numbers=(page_number,), backend="pymupdf"
            )
        )
        page_meta = extract_page_metadata(page_text)
        if page_meta is None:  # Empty PDF
            return None

        table = rows.import_from_pdf(
            filename_or_fobj,
            page_numbers=(page_number,),
            backend="pymupdf",
            algorithm=YGroupsXPositionAlgorithm,
            fields=FIELDS,
            skip_header=False,
            starts_after=starts_after,
            ends_before=ends_before,
        )
        for row in table:
            if list(row._asdict().values()).count("") > 3:  # Empty line
                continue
            row = convert_row(row)
            row.update(page_meta)
            result.append(row)

    return result
