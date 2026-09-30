# Automação E2E — OWASP Juice Shop

Projeto de automação funcional E2E em Python, com Selenium WebDriver e Pytest,
organizado com Page Object Model (POM). Os cenários implementados cobrem
acesso, login negativo, cadastro sem envio, pesquisa e detalhes de produtos,
carrinho sem checkout e paginação da listagem.

## Requisitos

- Windows 10 ou superior
- Python e o ambiente virtual `.venv` já configurado neste workspace
- Google Chrome
- Acesso à internet para abrir a aplicação e, se necessário, obter o ChromeDriver
  compatível via Selenium Manager

## Preparação

Ative o ambiente virtual existente e instale as dependências declaradas:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copie `.env.example` para `.env` e ajuste as configurações locais, se necessário:

| Variável | Finalidade | Valor padrão |
| --- | --- | --- |
| `JUICE_SHOP_URL` | Endereço da aplicação Juice Shop | `http://localhost:3000` |
| `CHROME_HEADLESS` | Executa o Chrome sem interface gráfica (`true` ou `false`) | `false` |
| `CHROME_BIN` | Caminho do executável do Google Chrome, quando a detecção automática não for suficiente | Detectado pelo Selenium |

O arquivo `.env` é ignorado pelo Git; mantenha nele apenas configurações locais.

## Execução

Execute a suíte a partir da raiz do projeto:

```powershell
python -m pytest
```

O Pytest gera automaticamente um relatório HTML autocontido em
`relatorios/relatorio.html`. Para gerar ou atualizar o relatório explicitamente:

```powershell
python -m pytest --html=relatorios/relatorio.html --self-contained-html
```

Abra `relatorios/relatorio.html` em um navegador para consultar o resultado de
cada teste, as durações, o resumo de aprovados e falhos e as informações de
ambiente disponibilizadas pelo `pytest-html`. O HTML é um artefato da execução,
está coberto pelo `.gitignore` e não deve ser versionado.

A fixture compartilhada `navegador`, em `conftest.py`, inicializa o Chrome e
encerra a sessão ao final de cada teste, inclusive quando ocorre uma falha.
`paginas/pagina_base.py` reúne recursos genéricos de navegação e sincronização
explícita. Os Page Objects das páginas e funcionalidades ficam em `paginas/`;
as validações de negócio pertencem aos testes.

## Cobertura funcional

Os testes automatizados estão em `testes/teste_fluxos_iniciais.py`. Na instância
local validada (OWASP Juice Shop v20.2.0), a interface não disponibiliza
categorias de produtos nem filtro ou navegação por categoria. Por isso, o
cenário de categoria previsto inicialmente foi substituído pela validação da
paginação real da listagem de produtos. O fluxo de carrinho não executa checkout.

A Fase 5 acrescenta validações negativas para campos de login vazios, tentativa
de login com e-mail malformado, cadastro incompleto, divergência de senha e
pesquisa sem resultados. Também valida que, com uma unidade no carrinho, a ação
de diminuir não reduz a quantidade abaixo de um. Na tela de login, o campo de
e-mail observado é do tipo texto e não apresenta validação de formato no
cliente; o caso malformado é submetido e valida a resposta genérica real de
autenticação inválida.

## Evidências de falhas

Quando uma fase de preparação ou execução de um teste falha e o WebDriver está
disponível, o hook do Pytest em `conftest.py` solicita ao Selenium uma captura
de tela no estado em que a falha ocorreu. Os arquivos `.png` são salvos em
`evidencias/`. O nome de cada arquivo contém o identificador do teste
(incluindo parâmetros, quando houver) e a data e hora da captura. Uma falha na
gravação é registrada no log e não substitui nem interrompe o resultado do
teste.

## Integração contínua com GitHub Actions

O workflow em `.github/workflows/testes.yml` é executado em cada `push` e
`pull_request`. Ele configura Python 3.13, Node.js 24 e Google Chrome, inicia a
imagem oficial pré-compilada do OWASP Juice Shop v20.2.0 e executa a suíte
Selenium/Pytest em modo headless. O job publica o relatório
`relatorios/relatorio.html` como artifact; screenshots são publicados como
artifact quando houver falhas que os gerem. A publicação dos artifacts ocorre
mesmo quando os testes falham, sem mascarar o resultado do job.

## Estrutura

```text
.
|-- .github/
|   `-- workflows/
|-- configuracoes/
|-- dados/
|-- evidencias/
|-- paginas/
|-- relatorios/
|-- testes/
|-- utilitarios/
|-- .env.example
|-- .gitignore
|-- conftest.py
|-- pytest.ini
`-- requirements.txt
```

Os seletores dos Page Objects foram conferidos na interface local da aplicação.
