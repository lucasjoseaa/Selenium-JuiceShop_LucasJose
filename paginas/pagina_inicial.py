"""Page Object da pagina inicial do OWASP Juice Shop."""

from selenium.webdriver.common.by import By

from configuracoes.ambiente import url_aplicacao
from paginas.pagina_base import PaginaBase


class PaginaInicial(PaginaBase):
    """Representa a pagina inicial e a navegacao para o login."""

    LOCALIZADOR_CONTEUDO_PRINCIPAL = (By.CSS_SELECTOR, "main .heading")
    LOCALIZADOR_BOTAO_CONTA = (By.ID, "navbarAccount")
    LOCALIZADOR_BOTAO_LOGIN_MENU = (By.ID, "navbarLoginButton")

    def abrir(self) -> None:
        """Abre a pagina inicial e aguarda seu conteudo principal."""
        self.acessar(url_aplicacao)
        self.aguardar_elemento_visivel(self.LOCALIZADOR_CONTEUDO_PRINCIPAL)
        self.dispensar_avisos_iniciais_se_exibidos()

    def conteudo_principal_visivel(self) -> bool:
        """Indica se o conteudo principal da pagina esta visivel."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CONTEUDO_PRINCIPAL
        ).is_displayed()

    def acessar_login(self) -> None:
        """Abre o menu da conta e acessa a pagina de login."""
        self.aguardar_elemento_clicavel(self.LOCALIZADOR_BOTAO_CONTA).click()
        self.aguardar_elemento_clicavel(self.LOCALIZADOR_BOTAO_LOGIN_MENU).click()
        self.aguardar_elemento_visivel((By.ID, "email"))
