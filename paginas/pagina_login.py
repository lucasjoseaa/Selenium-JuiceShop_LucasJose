"""Page Object da pagina de login do OWASP Juice Shop."""

from selenium.webdriver.common.by import By

from configuracoes.ambiente import url_aplicacao
from paginas.pagina_base import PaginaBase


class PaginaLogin(PaginaBase):
    """Representa os campos e as interacoes da pagina de login."""

    LOCALIZADOR_CAMPO_EMAIL = (By.ID, "email")
    LOCALIZADOR_CAMPO_SENHA = (By.ID, "password")
    LOCALIZADOR_BOTAO_ENTRAR = (By.ID, "loginButton")
    LOCALIZADOR_LINK_CADASTRO = (By.CSS_SELECTOR, "a[href='#/register']")
    LOCALIZADOR_MENSAGEM_ERRO = (By.CSS_SELECTOR, ".mdc-card > .error")

    def abrir(self) -> None:
        """Abre a pagina de login e aguarda o campo de email."""
        self.acessar(f"{url_aplicacao.rstrip('/')}/#/login")
        self.dispensar_avisos_iniciais_se_exibidos()
        self.aguardar_elemento_visivel(self.LOCALIZADOR_CAMPO_EMAIL)

    def informar_email(self, email: str) -> None:
        """Preenche o campo de email."""
        campo_email = self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CAMPO_EMAIL
        )
        campo_email.clear()
        campo_email.send_keys(email)

    def informar_senha(self, senha: str) -> None:
        """Preenche o campo de senha."""
        campo_senha = self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CAMPO_SENHA
        )
        campo_senha.clear()
        campo_senha.send_keys(senha)

    def clicar_entrar(self) -> None:
        """Aciona o botao de login quando estiver habilitado."""
        self.aguardar_elemento_clicavel(self.LOCALIZADOR_BOTAO_ENTRAR).click()

    def botao_entrar_habilitado(self) -> bool:
        """Indica se o botao de login esta habilitado."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_BOTAO_ENTRAR
        ).is_enabled()

    def obter_mensagem_erro(self) -> str:
        """Aguarda e retorna a mensagem de erro apresentada no login."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_MENSAGEM_ERRO
        ).text.strip()

    def campos_login_visiveis(self) -> bool:
        """Indica se os campos de email e senha estao visiveis."""
        campo_email = self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CAMPO_EMAIL
        )
        campo_senha = self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CAMPO_SENHA
        )
        return campo_email.is_displayed() and campo_senha.is_displayed()

    def acessar_cadastro(self) -> None:
        """Abre o cadastro pelo link apresentado na pagina de login."""
        self.aguardar_elemento_clicavel(self.LOCALIZADOR_LINK_CADASTRO).click()
        self.aguardar_elemento_visivel((By.ID, "emailControl"))
