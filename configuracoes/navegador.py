"""Opcoes de inicializacao do Google Chrome."""

import os
from pathlib import Path

from selenium.webdriver.chrome.options import Options

from configuracoes.ambiente import modo_sem_interface


def criar_opcoes_chrome() -> Options:
    """Monta as opcoes do Chrome para execucao local ou em CI."""
    opcoes = Options()
    caminho_executavel = os.getenv("CHROME_BIN", "").strip()

    if caminho_executavel:
        caminho_chrome = Path(caminho_executavel)
        if not caminho_chrome.is_file():
            raise FileNotFoundError(
                f"O executavel informado em CHROME_BIN nao existe: {caminho_chrome}"
            )
        opcoes.binary_location = str(caminho_chrome)
    elif os.name == "nt":
        caminhos_chrome = [
            Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
            / "Google"
            / "Chrome"
            / "Application"
            / "chrome.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"))
            / "Google"
            / "Chrome"
            / "Application"
            / "chrome.exe",
            Path(os.environ.get("LOCALAPPDATA", ""))
            / "Google"
            / "Chrome"
            / "Application"
            / "chrome.exe",
        ]
        caminho_chrome = next(
            (caminho for caminho in caminhos_chrome if caminho.is_file()),
            None,
        )
        if caminho_chrome is not None:
            opcoes.binary_location = str(caminho_chrome)

    if modo_sem_interface:
        opcoes.add_argument("--headless")
        opcoes.add_argument("--window-size=1920,1080")
    else:
        opcoes.add_argument("--start-maximized")

    if os.name != "nt":
        opcoes.add_argument("--disable-dev-shm-usage")
        opcoes.add_argument("--no-sandbox")

    return opcoes
