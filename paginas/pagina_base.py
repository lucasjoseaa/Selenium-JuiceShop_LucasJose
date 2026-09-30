"""Comportamentos comuns as paginas da aplicacao."""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as condicoes_esperadas
from selenium.webdriver.support.ui import WebDriverWait


class PaginaBase:
    """Disponibiliza esperas e navegacao compartilhadas entre paginas."""

    LOCALIZADOR_BOTAO_DISPENSAR_BEM_VINDO = (
        By.CSS_SELECTOR,
        "button[aria-label='Close Welcome Banner']",
    )
    LOCALIZADOR_BOTAO_DISPENSAR_COOKIES = (
        By.CSS_SELECTOR,
        "a[aria-label='dismiss cookie message']",
    )

    def __init__(self, navegador: WebDriver, tempo_espera: int = 10) -> None:
        self.navegador = navegador
        self.espera = WebDriverWait(navegador, tempo_espera)

    def acessar(self, url: str) -> None:
        """Navega para o endereco informado."""
        self.navegador.get(url)

    def aguardar_elemento_visivel(
        self,
        localizador: tuple[str, str],
    ) -> WebElement:
        """Aguarda um elemento identificado pelo localizador ficar visivel."""
        return self.espera.until(
            condicoes_esperadas.visibility_of_element_located(localizador)
        )

    def aguardar_elemento_clicavel(
        self,
        localizador: tuple[str, str],
    ) -> WebElement:
        """Aguarda um elemento identificado pelo localizador ficar clicavel."""
        return self.espera.until(
            condicoes_esperadas.element_to_be_clickable(localizador)
        )

    def dispensar_avisos_iniciais_se_exibidos(self) -> None:
        """Dispensa os avisos iniciais que bloqueiam a interacao com a pagina."""
        self._dispensar_aviso_bem_vindo()

        avisos = self.navegador.find_elements(
            *self.LOCALIZADOR_BOTAO_DISPENSAR_COOKIES
        )
        if not avisos or not avisos[0].is_displayed():
            return

        try:
            self.aguardar_elemento_clicavel(
                self.LOCALIZADOR_BOTAO_DISPENSAR_COOKIES
            ).click()
        except ElementClickInterceptedException:
            botoes_bem_vindo = self.navegador.find_elements(
                *self.LOCALIZADOR_BOTAO_DISPENSAR_BEM_VINDO
            )
            if not botoes_bem_vindo or not botoes_bem_vindo[0].is_displayed():
                raise

            self._dispensar_aviso_bem_vindo()
            self.aguardar_elemento_clicavel(
                self.LOCALIZADOR_BOTAO_DISPENSAR_COOKIES
            ).click()

    def _dispensar_aviso_bem_vindo(self) -> None:
        espera_aviso = WebDriverWait(self.navegador, 3)
        try:
            espera_aviso.until(
                condicoes_esperadas.visibility_of_element_located(
                    self.LOCALIZADOR_BOTAO_DISPENSAR_BEM_VINDO
                )
            )
        except TimeoutException:
            return

        self.aguardar_elemento_clicavel(
            self.LOCALIZADOR_BOTAO_DISPENSAR_BEM_VINDO
        ).click()
        self.espera.until(
            condicoes_esperadas.invisibility_of_element_located(
                self.LOCALIZADOR_BOTAO_DISPENSAR_BEM_VINDO
            )
        )
        self.espera.until(
            condicoes_esperadas.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".cdk-overlay-backdrop")
            )
        )
