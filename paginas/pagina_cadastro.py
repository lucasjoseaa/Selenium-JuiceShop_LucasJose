"""Page Object da pagina de cadastro do OWASP Juice Shop."""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as condicoes_esperadas

from configuracoes.ambiente import url_aplicacao
from paginas.pagina_base import PaginaBase


class PaginaCadastro(PaginaBase):
    """Representa os campos e as interacoes da pagina de cadastro."""

    LOCALIZADOR_CAMPO_EMAIL = (By.ID, "emailControl")
    LOCALIZADOR_CAMPO_SENHA = (By.ID, "passwordControl")
    LOCALIZADOR_CAMPO_CONFIRMACAO_SENHA = (By.ID, "repeatPasswordControl")
    LOCALIZADOR_SELECAO_PERGUNTA_SEGURANCA = (
        By.CSS_SELECTOR,
        "mat-select[name='securityQuestion']",
    )
    LOCALIZADOR_OPCOES_PERGUNTA_SEGURANCA = (
        By.CSS_SELECTOR,
        "mat-option[role='option']",
    )
    LOCALIZADOR_CAMPO_RESPOSTA_SEGURANCA = (By.ID, "securityAnswerControl")
    LOCALIZADOR_BOTAO_CADASTRAR = (By.ID, "registerButton")
    LOCALIZADOR_MENSAGEM_VALIDACAO_CAMPO = (
        By.CSS_SELECTOR,
        "mat-error.mat-mdc-form-field-error",
    )

    def abrir(self) -> None:
        """Abre a pagina de cadastro e aguarda o campo de email."""
        self.acessar(f"{url_aplicacao.rstrip('/')}/#/register")
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

    def informar_confirmacao_senha(self, senha: str) -> None:
        """Preenche a confirmacao da senha."""
        campo_confirmacao = self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CAMPO_CONFIRMACAO_SENHA
        )
        campo_confirmacao.clear()
        campo_confirmacao.send_keys(senha)

    def desfocar_campo_confirmacao_senha(self) -> None:
        """Desfoca a confirmacao para acionar a validacao do formulario."""
        self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CAMPO_CONFIRMACAO_SENHA
        ).send_keys(Keys.TAB)

    def selecionar_pergunta_seguranca(self, pergunta: str) -> None:
        """Seleciona uma pergunta de seguranca pelo texto exibido."""
        self.aguardar_elemento_clicavel(
            self.LOCALIZADOR_SELECAO_PERGUNTA_SEGURANCA
        ).click()
        opcoes: list[WebElement] = self.espera.until(
            condicoes_esperadas.visibility_of_all_elements_located(
                self.LOCALIZADOR_OPCOES_PERGUNTA_SEGURANCA
            )
        )

        for opcao in opcoes:
            if opcao.text.strip() == pergunta:
                opcao.click()
                return

        raise LookupError(
            f"Nao foi encontrada a pergunta de seguranca: {pergunta}"
        )

    def informar_resposta_seguranca(self, resposta: str) -> None:
        """Preenche a resposta da pergunta de seguranca."""
        campo_resposta = self.aguardar_elemento_visivel(
            self.LOCALIZADOR_CAMPO_RESPOSTA_SEGURANCA
        )
        campo_resposta.clear()
        campo_resposta.send_keys(resposta)

    def clicar_cadastrar(self) -> None:
        """Aciona o botao de cadastro quando estiver habilitado."""
        self.aguardar_elemento_clicavel(self.LOCALIZADOR_BOTAO_CADASTRAR).click()

    def formulario_pronto_para_cadastro(self) -> bool:
        """Indica se o formulario esta valido sem enviar o cadastro."""
        return self.aguardar_elemento_clicavel(
            self.LOCALIZADOR_BOTAO_CADASTRAR
        ).is_enabled()

    def botao_cadastrar_habilitado(self) -> bool:
        """Indica se o botao de cadastro esta habilitado."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_BOTAO_CADASTRAR
        ).is_enabled()

    def obter_mensagem_validacao_campo(self) -> str:
        """Retorna a mensagem real apresentada na validacao de um campo."""
        return self.aguardar_elemento_visivel(
            self.LOCALIZADOR_MENSAGEM_VALIDACAO_CAMPO
        ).text.strip()
