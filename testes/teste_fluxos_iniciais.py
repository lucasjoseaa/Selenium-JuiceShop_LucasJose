"""Testes funcionais iniciais da aplicacao OWASP Juice Shop."""

from configuracoes.ambiente import url_aplicacao
from paginas.pagina_cadastro import PaginaCadastro
from paginas.pagina_carrinho import PaginaCarrinho
from paginas.pagina_detalhes_produto import PaginaDetalhesProduto
from paginas.pagina_inicial import PaginaInicial
from paginas.pagina_login import PaginaLogin
from paginas.pagina_produtos import PaginaProdutos


def testar_acesso_bem_sucedido_a_pagina_inicial(navegador) -> None:
    """Confirma que a pagina inicial abre e apresenta o conteudo principal."""
    pagina_inicial = PaginaInicial(navegador)

    pagina_inicial.abrir()

    assert navegador.current_url.startswith(url_aplicacao)
    assert navegador.title == "OWASP Juice Shop"
    assert pagina_inicial.conteudo_principal_visivel()


def testar_acesso_a_pagina_de_login(navegador) -> None:
    """Confirma que a pagina de login abre com seus campos principais."""
    pagina_login = PaginaLogin(navegador)

    pagina_login.abrir()

    assert navegador.current_url.endswith("#/login")
    assert pagina_login.campos_login_visiveis()


def testar_login_com_credenciais_invalidas_exibe_erro_real(
    navegador,
) -> None:
    """Confirma a mensagem exibida ao tentar login com conta inexistente."""
    pagina_login = PaginaLogin(navegador)

    pagina_login.abrir()
    pagina_login.informar_email("qa-inexistente-fase3@example.invalid")
    pagina_login.informar_senha("Senha-invalida-fase3-987")
    pagina_login.clicar_entrar()

    assert pagina_login.obter_mensagem_erro() == "Invalid email or password."


def testar_preenchimento_dos_campos_obrigatorios_do_cadastro(
    navegador,
) -> None:
    """Confirma o preenchimento do cadastro sem enviar o formulario."""
    pagina_cadastro = PaginaCadastro(navegador)

    pagina_cadastro.abrir()
    pagina_cadastro.informar_email("qa-nao-enviado-fase3@example.invalid")
    pagina_cadastro.informar_senha("SenhaTeste-fase3-987")
    pagina_cadastro.informar_confirmacao_senha("SenhaTeste-fase3-987")
    pagina_cadastro.selecionar_pergunta_seguranca(
        "Mother's maiden name?"
    )
    pagina_cadastro.informar_resposta_seguranca("RespostaNaoEnviada")

    assert pagina_cadastro.formulario_pronto_para_cadastro()


def testar_pesquisa_de_produtos_apresenta_resultados_relacionados(
    navegador,
) -> None:
    """Confirma que pesquisar por apple apresenta produtos relacionados."""
    pagina_produtos = PaginaProdutos(navegador)

    pagina_produtos.abrir()
    pagina_produtos.pesquisar("apple")
    nomes_produtos = pagina_produtos.obter_nomes_produtos()

    assert "Search Results - apple" in pagina_produtos.obter_titulo_listagem()
    assert nomes_produtos
    assert all("apple" in nome.lower() for nome in nomes_produtos)


def testar_visualizacao_dos_detalhes_de_um_produto(
    navegador,
) -> None:
    """Confirma nome, descricao e preco no modal de detalhes do produto."""
    pagina_produtos = PaginaProdutos(navegador)
    pagina_detalhes = PaginaDetalhesProduto(navegador)
    nome_produto = "Apple Juice (1000ml)"

    pagina_produtos.abrir()
    pagina_produtos.abrir_detalhes_produto(nome_produto)

    assert pagina_detalhes.obter_nome_produto() == nome_produto
    assert "The all-time classic." in pagina_detalhes.obter_descricao_e_preco()
    assert pagina_detalhes.obter_preco_produto() == "1.99¤"


def testar_produto_adicionado_esta_presente_no_carrinho(
    navegador,
) -> None:
    """Confirma que o produto adicionado aparece no carrinho."""
    pagina_produtos = PaginaProdutos(navegador)
    pagina_carrinho = PaginaCarrinho(navegador)
    nome_produto = "Apple Juice (1000ml)"

    pagina_produtos.abrir()
    pagina_produtos.adicionar_produto_ao_carrinho(nome_produto)
    pagina_carrinho.abrir()

    assert "Your Basket" in pagina_carrinho.obter_titulo()
    assert any(
        nome_produto in linha
        for linha in pagina_carrinho.obter_produtos_adicionados()
    )


def testar_paginacao_exibe_outra_pagina_de_produtos(
    navegador,
) -> None:
    """Confirma que a pagina seguinte exibe outro conjunto de produtos."""
    pagina_produtos = PaginaProdutos(navegador)

    pagina_produtos.abrir()
    nomes_primeira_pagina = pagina_produtos.obter_nomes_produtos()
    intervalo_primeira_pagina = pagina_produtos.obter_intervalo_paginacao()

    pagina_produtos.avancar_pagina()
    nomes_pagina_seguinte = pagina_produtos.obter_nomes_produtos()
    intervalo_pagina_seguinte = pagina_produtos.obter_intervalo_paginacao()

    assert nomes_primeira_pagina
    assert nomes_pagina_seguinte
    assert nomes_primeira_pagina != nomes_pagina_seguinte
    assert intervalo_primeira_pagina != intervalo_pagina_seguinte


def testar_login_com_campos_obrigatorios_vazios_mantem_botao_desabilitado(
    navegador,
) -> None:
    """Valida que campos de login vazios impedem o envio."""
    pagina_login = PaginaLogin(navegador)

    pagina_login.abrir()

    assert not pagina_login.botao_entrar_habilitado()


def testar_login_com_email_em_formato_invalido_exibe_erro_da_aplicacao(
    navegador,
) -> None:
    """Valida a rejeicao de login com email malformado pela aplicacao."""
    pagina_login = PaginaLogin(navegador)

    pagina_login.abrir()
    pagina_login.informar_email("nao-e-um-email")
    pagina_login.informar_senha("SenhaInvalida-fase5-123")

    assert pagina_login.botao_entrar_habilitado()

    pagina_login.clicar_entrar()

    assert pagina_login.obter_mensagem_erro() == "Invalid email or password."


def testar_cadastro_incompleto_mantem_botao_desabilitado(
    navegador,
) -> None:
    """Valida que campos obrigatorios vazios impedem o cadastro."""
    pagina_cadastro = PaginaCadastro(navegador)

    pagina_cadastro.abrir()

    assert not pagina_cadastro.botao_cadastrar_habilitado()


def testar_cadastro_com_senhas_diferentes_exibe_validacao_e_impede_envio(
    navegador,
) -> None:
    """Valida mensagem e bloqueio do cadastro quando as senhas divergem."""
    pagina_cadastro = PaginaCadastro(navegador)

    pagina_cadastro.abrir()
    pagina_cadastro.informar_email("qa-divergencia-fase5@example.invalid")
    pagina_cadastro.informar_senha("SenhaCorreta-fase5-123")
    pagina_cadastro.informar_confirmacao_senha("SenhaDiferente-fase5-456")
    pagina_cadastro.desfocar_campo_confirmacao_senha()

    assert (
        pagina_cadastro.obter_mensagem_validacao_campo()
        == "Passwords do not match"
    )
    assert not pagina_cadastro.botao_cadastrar_habilitado()


def testar_pesquisa_sem_resultados_exibe_estado_vazio(
    navegador,
) -> None:
    """Valida o estado apresentado quando nenhum produto corresponde."""
    pagina_produtos = PaginaProdutos(navegador)
    termo_inexistente = "termo-inexistente-fase5-xyz"

    pagina_produtos.abrir()
    pagina_produtos.pesquisar(termo_inexistente)

    assert f"Search Results - {termo_inexistente}" in (
        pagina_produtos.obter_titulo_listagem()
    )
    assert pagina_produtos.obter_mensagem_sem_resultados() == "No results found"
    assert pagina_produtos.obter_quantidade_produtos() == 0


def testar_carrinho_impede_reduzir_quantidade_abaixo_de_um(
    navegador,
) -> None:
    """Valida que a tentativa de reduzir uma unidade mantem o produto no carrinho."""
    pagina_produtos = PaginaProdutos(navegador)
    pagina_carrinho = PaginaCarrinho(navegador)
    nome_produto = "Apple Juice (1000ml)"

    pagina_produtos.abrir()
    pagina_produtos.adicionar_produto_ao_carrinho(nome_produto)
    pagina_carrinho.abrir()
    pagina_carrinho.diminuir_quantidade_produto(nome_produto)

    assert pagina_carrinho.obter_quantidade_produto(nome_produto) == 1
