"""Page Object do modal de detalhes de um produto."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condicoes_esperadas

from paginas.pagina_base import PaginaBase


class PaginaDetalhesProduto(PaginaBase):
    """Representa as informacoes e acoes do modal de detalhes."""

    LOCALIZADOR_MODAL = (By.CSS_SELECTOR, "mat-dialog-container")
    LOCALIZADOR_NOME_PRODUTO = (
        By.CSS_SELECTOR,
        "mat-dialog-container h1",
    )
    LOCALIZADOR_DESCRICAO_E_PRECO = (
        By.CSS_SELECTOR,
        "mat-dialog-container .details-row",
    )
    LOCALIZADOR_PRECO_PRODUTO = (
        By.CSS_SELECTOR,
        "mat-dialog-container .item-price",
    )
    LOCALIZADOR_BOTAO_FECHAR = (
        By.CSS_SELECTOR,
        "button[aria-label='Close Dialog']",
    )

    def aguardar_abertura(self) -> None:
        """Aguarda o modal de detalhes ficar visivel."""
        self.aguardar_elemento_visivel(self.LOCALIZADOR_MODAL)

    def obter_nome_produto(self) -> str:
        """Retorna o nome do produto exibido no modal."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_NOME_PRODUTO
        ).text.strip()

    def obter_descricao_e_preco(self) -> str:
        """Retorna a descricao e o preco exibidos no modal."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_DESCRICAO_E_PRECO
        ).text.strip()

    def obter_preco_produto(self) -> str:
        """Retorna o preco exibido no modal."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_PRECO_PRODUTO
        ).text.strip()

    def fechar(self) -> None:
        """Fecha o modal de detalhes do produto."""
        self.aguardar_elemento_clicavel(
            self.LOCALIZADOR_BOTAO_FECHAR
        ).click()
        self.espera.until(
            condicoes_esperadas.invisibility_of_element_located(
                self.LOCALIZADOR_MODAL
            )
        )
