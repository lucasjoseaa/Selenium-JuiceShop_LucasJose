"""Fixtures compartilhadas pela suíte de testes."""

from collections.abc import Iterator
from datetime import datetime
import logging
from pathlib import Path
import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from configuracoes.navegador import criar_opcoes_chrome

_REGISTRO = logging.getLogger(__name__)


@pytest.fixture
def navegador() -> Iterator[WebDriver]:
    """Inicializa o Chrome para o teste e garante seu encerramento."""
    opcoes: Options = criar_opcoes_chrome()
    navegador_chrome = webdriver.Chrome(options=opcoes)

    try:
        yield navegador_chrome
    finally:
        navegador_chrome.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item):
    """Salva uma captura quando uma fase do teste falha."""
    resultado = yield
    relatorio = resultado.get_result()

    if not relatorio.failed or relatorio.when not in {"setup", "call"}:
        return

    navegador_chrome = item.funcargs.get("navegador")
    if navegador_chrome is None:
        return

    try:
        pasta_evidencias = Path(__file__).parent / "evidencias"
        pasta_evidencias.mkdir(parents=True, exist_ok=True)

        nome_teste = re.sub(r"[^A-Za-z0-9_-]+", "_", item.nodeid)
        nome_teste = nome_teste.strip("_")[:160] or "teste"
        data_hora = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        caminho = pasta_evidencias / f"{nome_teste}_{data_hora}.png"
        contador = 1
        while caminho.exists():
            caminho = pasta_evidencias / (
                f"{nome_teste}_{data_hora}_{contador}.png"
            )
            contador += 1

        if not navegador_chrome.get_screenshot_as_file(str(caminho)):
            raise OSError("O WebDriver não confirmou a gravação da captura.")
    except Exception:
        _REGISTRO.exception(
            "Não foi possível salvar a evidência do teste %s.",
            item.nodeid,
        )
