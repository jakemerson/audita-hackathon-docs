from decimal import Decimal

import pytest

from app.models.nfe_models import AuditContext, NFeItem


@pytest.fixture
def context() -> AuditContext:
    return AuditContext(rbt12=Decimal("1800000"), pgdas_segregated=False)


@pytest.fixture
def sale_item() -> NFeItem:
    return NFeItem(
        line_number=1,
        product_code="P-1",
        description="Pastilha de freio nova",
        ncm="8708.30.90",
        cfop="5102",
        product_value=Decimal("1000"),
        pis_cst="01",
        cofins_cst="01",
        csosn="102",
    )


def make_xml(
    *,
    ncm: str = "87083090",
    cfop: str = "5102",
    value: str = "1000.00",
    namespace: str = "http://www.portalfiscal.inf.br/nfe",
    wrapped: bool = True,
    description: str = "Pastilha de freio nova",
) -> bytes:
    nfe = f"""<NFe xmlns=\"{namespace}\"><infNFe Id=\"NFe{'1' * 44}\" versao=\"4.00\">
      <ide><cUF>35</cUF><mod>55</mod><serie>1</serie><nNF>1001</nNF><dhEmi>2026-08-19T10:00:00-03:00</dhEmi></ide>
      <emit><CNPJ>00000000000191</CNPJ><xNome>OFICINA FIXTURE</xNome><CRT>1</CRT></emit>
      <dest><CNPJ>00000000000272</CNPJ><xNome>CLIENTE FICTICIO</xNome></dest>
      <det nItem=\"1\"><prod><cProd>P1</cProd><xProd>{description}</xProd><NCM>{ncm}</NCM><CFOP>{cfop}</CFOP><qCom>1</qCom><vUnCom>{value}</vUnCom><vProd>{value}</vProd></prod>
        <imposto><ICMS><ICMSSN102><orig>0</orig><CSOSN>102</CSOSN></ICMSSN102></ICMS><PIS><PISAliq><CST>01</CST></PISAliq></PIS><COFINS><COFINSAliq><CST>01</CST></COFINSAliq></COFINS></imposto>
      </det><infAdic><infCpl>FIXTURE SINTETICA AUDITA - SEM VALOR FISCAL</infCpl></infAdic>
    </infNFe></NFe>"""
    if not wrapped:
        return nfe.encode()
    return f"<nfeProc xmlns=\"{namespace}\" versao=\"4.00\">{nfe}</nfeProc>".encode()
