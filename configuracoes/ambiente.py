"""Configuracoes carregadas do ambiente e do arquivo .env."""

import os
from pathlib import Path

from dotenv import load_dotenv


_raiz_projeto = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=_raiz_projeto / ".env")

url_aplicacao = os.getenv(
    "JUICE_SHOP_URL",
    "http://localhost:3000",
).strip()

if not url_aplicacao:
    raise ValueError("A variavel JUICE_SHOP_URL nao pode estar vazia.")

_valor_modo_sem_interface = os.getenv("CHROME_HEADLESS", "false").strip().lower()

if _valor_modo_sem_interface in {"true", "1", "sim", "yes"}:
    modo_sem_interface = True
elif _valor_modo_sem_interface in {"false", "0", "nao", "no"}:
    modo_sem_interface = False
else:
    raise ValueError(
        "CHROME_HEADLESS deve conter um valor booleano: true ou false."
    )
