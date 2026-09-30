"""Page Object da listagem e pesquisa de produtos."""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as condicoes_esperadas

from configuracoes.ambiente import url_aplicacao
from paginas.pagina_base import PaginaBase


class PaginaProdutos(PaginaBase):
    """Representa a listagem, a pesquisa e as acoes dos produtos."""

    LOCALIZADOR_CONTEUDO_PRINCIPAL = (By.CSS_SELECTOR, "main .heading")
    LOCALIZADOR_BOTAO_ABRIR_PESQUISA = (
        By.CSS_SELECTOR,
        "button[aria-label='Open search']",
    )
    LOCALIZADOR_CAMPO_PESQUISA = (
        By.CSS_SELECTOR,
        "app-mat-search-bar#searchQuery input",
    )
    LOCALIZADOR_CARTOES_PRODUTO = (By.CSS_SELECTOR, "main app-product")
    LOCALIZADOR_BOTAO_DETALHES_PRODUTO = (
        By.CSS_SELECTOR,
        "section[aria-label='Click for more information about the product']",
    )
    LOCALIZADOR_BOTAO_ADICIONAR_CARRINHO = (
        By.CSS_SELECTOR,
        "button[aria-label='Add to Basket']",
    )
    LOCALIZADOR_BOTAO_CARRINHO = (
        By.CSS_SELECTOR,
        "button[aria-label='Show the shopping cart']",
    )
    LOCALIZADOR_BOTAO_PROXIMA_PAGINA = (
        By.CSS_SELECTOR,
        "mat-paginator button[aria-label='Next page']",
    )
    LOCALIZADOR_INTERVALO_PAGINACAO = (
        By.CSS_SELECTOR,
        "mat-paginator .mat-mdc-paginator-range-label",
    )
    LOCALIZADOR_MENSAGEM_SEM_RESULTADOS = (
        By.CSS_SELECTOR,
        "main .noResultText",
    )

    def abrir(self) -> None:
        """Abre a listagem inicial de produtos."""
        self.acessar(url_aplicacao)
        self.aguardar_elemento_visivel(self.LOCALIZADOR_CONTEUDO_PRINCIPAL)
        self.dispensar_avisos_iniciais_se_exibidos()
        self.aguardar_elemento_visivel(self.LOCALIZADOR_CARTOES_PRODUTO)

    def pesquisar(self, termo: str) -> None:
        """Pesquisa produtos pelo termo informado."""
        campos_visiveis = [
            campo
            for campo in self.navegador.find_elements(
                *self.LOCALIZADOR_CAMPO_PESQUISA
            )
            if campo.is_displayed()
        ]
        if not campos_visiveis:
            self.aguardar_elemento_clicavel(
                self.LOCALIZADOR_BOTAO_ABRIR_PESQUISA
            ).click()

        campo_pesquisa = self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CAMPO_PESQUISA
        )
        campo_pesquisa.clear()
        campo_pesquisa.send_keys(termo, Keys.ENTER)

        self.espera.until(
            condicoes_esperadas.text_to_be_present_in_element(
                self.LOCALIZADOR_CONTEUDO_PRINCIPAL,
                f"Search Results - {termo}",
            )
        )
        self.espera.until(
            condicoes_esperadas.any_of(
                condicoes_esperadas.visibility_of_element_located(
                    self.LOCALIZADOR_CARTOES_PRODUTO
                ),
                condicoes_esperadas.visibility_of_element_located(
                    self.LOCALIZADOR_MENSAGEM_SEM_RESULTADOS
                ),
            )
        )

    def obter_nomes_produtos(self) -> list[str]:
        """Retorna os nomes dos produtos exibidos na listagem atual."""
        self.aguardar_elemento_visivel(self.LOCALIZADOR_CARTOES_PRODUTO)
        return [
            cartao.find_element(By.CSS_SELECTOR, "img").get_attribute("alt")
            for cartao in self.navegador.find_elements(
                *self.LOCALIZADOR_CARTOES_PRODUTO
            )
        ]

    def obter_titulo_listagem(self) -> str:
        """Retorna o titulo da listagem atual de produtos."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CONTEUDO_PRINCIPAL
        ).text.strip()

    def obter_mensagem_sem_resultados(self) -> str:
        """Retorna a mensagem exibida quando a pesquisa nao encontra itens."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_MENSAGEM_SEM_RESULTADOS
        ).text.strip()

    def obter_quantidade_produtos(self) -> int:
        """Retorna a quantidade de cartoes de produto visiveis na listagem."""
        return len(
            self.navegador.find_elements(*self.LOCALIZADOR_CARTOES_PRODUTO)
        )

    def abrir_detalhes_produto(self, nome_produto: str) -> None:
        """Abre os detalhes do produto identificado pelo nome."""
        cartao = self._obter_cartao_produto(nome_produto)
        cartao.find_element(
            *self.LOCALIZADOR_BOTAO_DETALHES_PRODUTO
        ).click()

        from paginas.pagina_detalhes_produto import PaginaDetalhesProduto

        PaginaDetalhesProduto(self.navegador).aguardar_abertura()

    def adicionar_produto_ao_carrinho(self, nome_produto: str) -> None:
        """Adiciona ao carrinho o produto identificado pelo nome."""
        cartao = self._obter_cartao_produto(nome_produto)
        cartao.find_element(
            *self.LOCALIZADOR_BOTAO_ADICIONAR_CARRINHO
        ).click()
        self.espera.until(
            condicoes_esperadas.text_to_be_present_in_element(
                self.LOCALIZADOR_BOTAO_CARRINHO,
                "1",
            )
        )

    def acessar_carrinho(self) -> None:
        """Abre o carrinho pela navegacao principal."""
        self.aguardar_elemento_clicavel(
            self.LOCALIZADOR_BOTAO_CARRINHO
        ).click()
        self.espera.until(condicoes_esperadas.url_contains("#/basket"))

    def avancar_pagina(self) -> None:
        """Avanca para a proxima pagina da listagem de produtos."""
        primeiro_cartao: WebElement = self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CARTOES_PRODUTO
        )
        self.aguardar_elemento_clicavel(
            self.LOCALIZADOR_BOTAO_PROXIMA_PAGINA
        ).click()
        self.espera.until(condicoes_esperadas.staleness_of(primeiro_cartao))
        self.aguardar_elemento_visivel(self.LOCALIZADOR_CARTOES_PRODUTO)

    def obter_intervalo_paginacao(self) -> str:
        """Retorna o intervalo de itens mostrado pelo paginador."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_INTERVALO_PAGINACAO
        ).text.strip()

    def _obter_cartao_produto(self, nome_produto: str) -> WebElement:
        cartoes = self.espera.until(
            condicoes_esperadas.visibility_of_all_elements_located(
                self.LOCALIZADOR_CARTOES_PRODUTO
            )
        )
        for cartao in cartoes:
            imagem = cartao.find_element(By.CSS_SELECTOR, "img")
            if imagem.get_attribute("alt") == nome_produto:
                return cartao

        raise LookupError(
            f"Nao foi encontrado o produto na listagem atual: {nome_produto}"
        )
