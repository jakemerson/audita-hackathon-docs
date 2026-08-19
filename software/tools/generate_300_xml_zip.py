"""Gera um ZIP com 300 NF-e sintéticas para o teste de volume do Audita."""

from datetime import date
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

OUTPUT = Path(__file__).resolve().parents[1] / "sample_invoices" / "stress_60_months"
ARCHIVE = OUTPUT / "lote_300_xmls_ultimos_60_meses.zip"
PRODUCTS = (
    ("PAST", "Pastilhas de freio novas", "87083090", "1250.00", "01"),
    ("AMOR", "Amortecedores novos para automóvel", "87088000", "1680.00", "01"),
    ("FILT", "Filtro de óleo para motor", "84212300", "890.00", "04"),
    ("VELA", "Velas de ignição novas", "85111000", "740.00", "01"),
    ("PNEU", "Pneu novo para automóvel", "40111000", "2140.00", "04"),
)


def shift_month(month: date, delta: int) -> date:
    index = month.year * 12 + month.month - 1 + delta
    return date(index // 12, index % 12 + 1, 1)


def make_xml(issued: date, number: int, product: tuple[str, str, str, str, str]) -> str:
    code, description, ncm, value, cst = product
    numeric_code = (number * 7919) % 100_000_000
    key = f"35{issued:%y%m}0000000000019155001{number:09d}1{numeric_code:08d}0"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<NFe xmlns="http://www.portalfiscal.inf.br/nfe"><infNFe Id="NFe{key}" versao="4.00">
<ide><cUF>35</cUF><natOp>VENDA FIXTURE STRESS</natOp><mod>55</mod><serie>1</serie><nNF>{number}</nNF><dhEmi>{issued.isoformat()}T10:00:00-03:00</dhEmi></ide>
<emit><CNPJ>00000000000191</CNPJ><xNome>AUDITA LOJA SINTETICA</xNome><CRT>1</CRT></emit>
<dest><CNPJ>00000000000272</CNPJ><xNome>CLIENTE FICTICIO STRESS</xNome></dest>
<det nItem="1"><prod><cProd>{code}-{number}</cProd><xProd>{description}</xProd><NCM>{ncm}</NCM><CFOP>5102</CFOP><qCom>1</qCom><vUnCom>{value}</vUnCom><vProd>{value}</vProd></prod>
<imposto><ICMS><ICMSSN102><orig>0</orig><CSOSN>102</CSOSN></ICMSSN102></ICMS><PIS><PISOutr><CST>{cst}</CST></PISOutr></PIS><COFINS><COFINSOutr><CST>{cst}</CST></COFINSOutr></COFINS></imposto></det>
<infAdic><infCpl>FIXTURE SINTETICA AUDITA - SEM VALOR FISCAL - TESTE DE VOLUME</infCpl></infAdic>
</infNFe></NFe>
"""


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    first_month = shift_month(date(2026, 8, 1), -59)
    number = 20_000
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED) as archive:
        for month_offset in range(60):
            month = shift_month(first_month, month_offset)
            for item, product in enumerate(PRODUCTS, start=1):
                number += 1
                issued = date(month.year, month.month, item * 5)
                archive.writestr(
                    f"nfe_{issued:%Y_%m}_{item:02d}_{number}.xml",
                    make_xml(issued, number, product),
                )
    print(f"Criado {ARCHIVE} com 300 XMLs.")


if __name__ == "__main__":
    main()
