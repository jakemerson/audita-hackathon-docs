"""Gera massas sintéticas de 300 NF-e para autopeças, farmácia e bar."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


OUTPUT = Path(__file__).resolve().parents[1] / "sample_invoices" / "sector_stress"
END_MONTH = date(2026, 8, 1)

SECTORS = {
    "autopecas": {
        "name": "AUDITA AUTOPECAS SINTETICA",
        "cnpj": "00000000010191",
        "mono": (
            ("PAST", "Pastilhas de freio novas", "87083090", "1250.00"),
            ("AMOR", "Amortecedores novos para automóvel", "87088000", "1680.00"),
            ("FILT", "Filtro de óleo para motor", "84212300", "890.00"),
            ("VELA", "Velas de ignição novas", "85111000", "740.00"),
            ("PNEU", "Pneu novo para automóvel", "40111000", "2140.00"),
        ),
        "regular": (
            ("CAPA", "Capa de banco automotiva", "63079090", "420.00"),
            ("SUPT", "Suporte plástico para celular veicular", "39269090", "180.00"),
            ("FERR", "Jogo de ferramentas manuais", "82060000", "560.00"),
            ("MACA", "Macaco hidráulico portátil", "84254200", "810.00"),
            ("PANO", "Pano de microfibra automotivo", "63071000", "95.00"),
        ),
    },
    "farmacia": {
        "name": "AUDITA FARMACIA SINTETICA",
        "cnpj": "00000000020191",
        "mono": (
            ("MED1", "Medicamento em comprimidos", "30049099", "185.00"),
            ("MED2", "Medicamento antibiótico", "30032099", "240.00"),
            ("PERF", "Perfume de uso pessoal", "33030010", "310.00"),
            ("CREM", "Creme hidratante corporal", "33049990", "95.00"),
            ("SHAM", "Shampoo capilar", "33051000", "68.00"),
        ),
        "regular": (
            ("TERM", "Termômetro clínico digital", "90251990", "72.00"),
            ("SERG", "Seringa descartável", "90183119", "18.00"),
            ("MASC", "Máscara de proteção descartável", "63079010", "32.00"),
            ("LUVA", "Luva descartável para procedimento", "40151900", "48.00"),
            ("ESCV", "Escova dental manual", "96032100", "22.00"),
        ),
    },
    "bar": {
        "name": "AUDITA BAR SINTETICO",
        "cnpj": "00000000030191",
        "mono": (
            ("CERV", "Cerveja de malte", "22030000", "18.00"),
            ("REFR", "Refrigerante de cola", "22021000", "12.00"),
            ("AGUA", "Água mineral natural", "22011000", "8.00"),
            ("ENER", "Energético em lata", "22029900", "16.00"),
            ("CERS", "Cerveja sem álcool", "22029100", "15.00"),
        ),
        "regular": (
            ("BATF", "Porção de batata frita", "20041000", "38.00"),
            ("AMEN", "Amendoim torrado", "20081100", "14.00"),
            ("HAMB", "Hambúrguer bovino preparado", "16025000", "42.00"),
            ("SAND", "Sanduíche preparado", "19059090", "35.00"),
            ("CHIP", "Batata chips preparada", "20052000", "19.00"),
        ),
    },
}


def shift_month(month: date, delta: int) -> date:
    index = month.year * 12 + month.month - 1 + delta
    return date(index // 12, index % 12 + 1, 1)


def tax_xml(cst: str, value: str) -> str:
    if cst == "04":
        return "<PIS><PISNT><CST>04</CST></PISNT></PIS><COFINS><COFINSNT><CST>04</CST></COFINSNT></COFINS>"
    base = Decimal(value)
    pis = (base * Decimal("0.0165")).quantize(Decimal("0.01"))
    cofins = (base * Decimal("0.076")).quantize(Decimal("0.01"))
    return (
        f"<PIS><PISAliq><CST>01</CST><vBC>{value}</vBC><pPIS>1.65</pPIS><vPIS>{pis}</vPIS></PISAliq></PIS>"
        f"<COFINS><COFINSAliq><CST>01</CST><vBC>{value}</vBC><pCOFINS>7.60</pCOFINS><vCOFINS>{cofins}</vCOFINS></COFINSAliq></COFINS>"
    )


def make_xml(sector: dict, issued: date, number: int, product: tuple[str, str, str, str], cst: str) -> str:
    code, description, ncm, value = product
    numeric_code = (number * 7919) % 100_000_000
    key = f"35{issued:%y%m}{sector['cnpj']}55001{number:09d}1{numeric_code:08d}0"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<NFe xmlns="http://www.portalfiscal.inf.br/nfe"><infNFe Id="NFe{key}" versao="4.00">
<ide><cUF>35</cUF><natOp>VENDA FIXTURE SETORIAL</natOp><mod>55</mod><serie>1</serie><nNF>{number}</nNF><dhEmi>{issued.isoformat()}T10:00:00-03:00</dhEmi></ide>
<emit><CNPJ>{sector['cnpj']}</CNPJ><xNome>{sector['name']}</xNome><CRT>1</CRT></emit>
<dest><CNPJ>00000000000272</CNPJ><xNome>CLIENTE FICTICIO SETORIAL</xNome></dest>
<det nItem="1"><prod><cProd>{code}-{number}</cProd><xProd>{description}</xProd><NCM>{ncm}</NCM><CFOP>5102</CFOP><qCom>1</qCom><vUnCom>{value}</vUnCom><vProd>{value}</vProd></prod>
<imposto><ICMS><ICMSSN102><orig>0</orig><CSOSN>102</CSOSN></ICMSSN102></ICMS>{tax_xml(cst, value)}</imposto></det>
<infAdic><infCpl>FIXTURE SINTETICA AUDITA - SEM VALOR FISCAL - TESTE SETORIAL</infCpl></infAdic>
</infNFe></NFe>
"""


def generate_sector(sector_index: int, slug: str, sector: dict) -> Path:
    first_month = shift_month(END_MONTH, -59)
    archive_path = OUTPUT / f"{slug}_300_xmls_60_meses.zip"
    mono_seen = 0
    number = (sector_index + 3) * 10_000
    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        for month_offset in range(60):
            month = shift_month(first_month, month_offset)
            for item_index in range(5):
                number += 1
                issued = date(month.year, month.month, (item_index + 1) * 5)
                is_monophase = (month_offset + item_index) % 2 == 0
                if is_monophase:
                    product = sector["mono"][(month_offset + item_index) % len(sector["mono"])]
                    cst = "04" if mono_seen % 2 == 0 else "01"
                    folder = "monofasicos_cst_04" if cst == "04" else "monofasicos_cst_comum"
                    mono_seen += 1
                else:
                    product = sector["regular"][(month_offset + item_index) % len(sector["regular"])]
                    cst = "01"
                    folder = "nao_monofasicos"
                filename = f"{folder}/nfe_{issued:%Y_%m}_{item_index + 1:02d}_{number}.xml"
                archive.writestr(filename, make_xml(sector, issued, number, product, cst))
    return archive_path


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for index, (slug, sector) in enumerate(SECTORS.items()):
        path = generate_sector(index, slug, sector)
        print(f"Criado {path.name} com 300 XMLs.")


if __name__ == "__main__":
    main()
