#!/usr/bin/env python3
"""Inicializador portátil do Audita."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Inicia o Audita na porta 8000.")
    parser.add_argument("--check", action="store_true", help="valida o ambiente sem iniciar o servidor")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        raise SystemExit("Audita requer Python 3.12 ou superior.")
    root = Path(__file__).resolve().parent
    os.chdir(root)
    try:
        import uvicorn
        from app.main import app  # noqa: F401
    except ImportError as exc:
        raise SystemExit("Dependências ausentes. Execute ./run.sh para preparar o .venv.") from exc
    if args.check:
        print(f"Audita pronto | Python {sys.version.split()[0]} | {root}")
        return
    host = os.getenv("AUDITA_HOST", "127.0.0.1")
    port = int(os.getenv("AUDITA_PORT", "8000"))
    print(f"Audita disponível em http://{host}:{port}")
    print("Modo local funciona sem chave OpenAI. Pressione Ctrl+C para encerrar.")
    uvicorn.run("app.main:app", host=host, port=port, reload=False, log_level="info")


if __name__ == "__main__":
    main()
