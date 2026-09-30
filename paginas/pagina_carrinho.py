"""Page Object da pagina do carrinho de compras."""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as condicoes_esperadas

from paginas.pagina_base import PaginaBase
from paginas.pagina_produtos import PaginaProdutos


class PaginaCarrinho(PaginaBase):
    """Representa a listagem de produtos adicionados ao carrinho."""

    LOCALIZADOR_TITULO_CARRINHO = (By.CSS_SELECTOR, "h1")
    LOCALIZADOR_LINHAS_PRODUTOS = (By.CSS_SELECTOR, "mat-row")
    LOCALIZADOR_CELULA_PRODUTO = (By.CSS_SELECTOR, "mat-cell.mat-column-product")
    LOCALIZADOR_CELULA_QUANTIDADE = (
        By.CSS_SELECTOR,
        "mat-cell.mat-column-quantity",
    )

    def abrir(self) -> None:
        """Abre o carrinho pela navegacao da listagem de produtos."""
        PaginaProdutos(self.navegador).acessar_carrinho()
        self.aguardar_elemento_visivel(self.LOCALIZADOR_TITULO_CARRINHO)

    def obter_titulo(self) -> str:
        """Retorna o titulo apresentado na pagina do carrinho."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_TITULO_CARRINHO
        ).text.strip()

    def obter_produtos_adicionados(self) -> list[str]:
        """Retorna o texto das linhas de produtos do carrinho."""
        return [
            linha.text.strip()
            for linha in self.navegador.find_elements(
                *self.LOCALIZADOR_LINHAS_PRODUTOS
            )
            if linha.text.strip()
        ]

    def obter_quantidade_produto(self, nome_produto: str) -> int:
        """Retorna a quantidade do produto identificado no carrinho."""
        return self.espera.until(
            lambda _: self._obter_quantidade_atual(nome_produto)
        )

    def diminuir_quantidade_produto(self, nome_produto: str) -> None:
        """Tenta diminuir a quantidade do produto no carrinho."""
        linha = self._obter_linha_produto(nome_produto)
        botoes = linha.find_element(
            *self.LOCALIZADOR_CELULA_QUANTIDADE
        ).find_elements(By.CSS_SELECTOR, "button")
        botao_diminuir = botoes[0]
        self.espera.until(
            condicoes_esperadas.element_to_be_clickable(botao_diminuir)
        ).click()

    def _obter_linha_produto(self, nome_produto: str) -> WebElement:
        """Localiza a linha do produto pelo nome exibido no carrinho."""
        linhas = self.espera.until(
            condicoes_esperadas.visibility_of_all_elements_located(
                self.LOCALIZADOR_LINHAS_PRODUTOS
            )
        )
        for linha in linhas:
            nome_exibido = linha.find_element(
                *self.LOCALIZADOR_CELULA_PRODUTO
            ).text.strip()
            if nome_exibido == nome_produto:
                return linha

        raise LookupError(
            f"Nao foi encontrado o produto no carrinho: {nome_produto}"
        )

    def _obter_quantidade_atual(
        self,
        nome_produto: str,
    ) -> int | bool:
        """Relocaliza a quantidade caso a aplicacao atualize a linha."""
        try:
            linha = self._obter_linha_produto(nome_produto)
            quantidade = linha.find_element(
                *self.LOCALIZADOR_CELULA_QUANTIDADE
            ).text.strip()
        except StaleElementReferenceException:
            return False

        return int(quantidade)
