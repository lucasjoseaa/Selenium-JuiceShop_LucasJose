# Automação E2E — OWASP Juice Shop com Selenium e Python

Projeto de estudo e prática de QA Automation que valida fluxos funcionais da
aplicação web OWASP Juice Shop com Selenium WebDriver e Pytest.

[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/lucasjoseaa/Selenium-JuiceShop_LucasJose/testes.yml?branch=main&label=GitHub%20Actions)](https://github.com/lucasjoseaa/Selenium-JuiceShop_LucasJose/actions/workflows/testes.yml)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.49.0-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-9.1.1-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![pytest-html](https://img.shields.io/badge/pytest--html-4.2.0-6A5ACD)](https://pytest-html.readthedocs.io/)
[![Google Chrome](https://img.shields.io/badge/Google_Chrome-Headless-4285F4?logo=googlechrome&logoColor=white)](https://www.google.com/chrome/)
[![Node.js](https://img.shields.io/badge/Node.js-24-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Execu%C3%A7%C3%A3o_local_e_CI-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Git](https://img.shields.io/badge/Git-Versionamento-F05032?logo=git&logoColor=white)](https://git-scm.com/)
[![OWASP Juice Shop](https://img.shields.io/badge/OWASP_Juice_Shop-v20.2.0-FF6B35?logo=owasp&logoColor=white)](https://owasp.org/www-project-juice-shop/)

## Sobre o projeto

Esta suíte demonstra a automação de testes end-to-end em uma aplicação web real.
O foco é qualidade de software e validação funcional da interface — não é um
projeto de exploração de vulnerabilidades ou pentest.

O projeto contém **14 testes automatizados**, organizados com Page Object Model
(POM), e executa localmente e no GitHub Actions.

## Tecnologias e ferramentas

- **Python 3.13** para a implementação e execução dos testes.
- **Selenium WebDriver** para controlar o Google Chrome.
- **Pytest** para organizar e executar os testes e suas fixtures.
- **pytest-html** para gerar o relatório HTML autocontido.
- **Page Object Model (POM)** para separar os testes das interações com a interface.
- **Google Chrome** como navegador de teste.
- **Docker** para iniciar a versão pré-compilada do Juice Shop localmente e no CI.
- **Node.js 24** configurado pelo workflow, compatível com a distribuição usada.
- **Git e GitHub** para versionamento e hospedagem do projeto.
- **GitHub Actions** para executar a suíte em integração contínua.
- **OWASP Juice Shop v20.2.0** como aplicação sob teste.

## Arquitetura

```text
Pytest
   ↓
Fixtures / conftest.py
   ↓
Selenium WebDriver
   ↓
Page Objects
   ↓
OWASP Juice Shop
```

- **Pytest** coleta os cenários, executa as verificações e produz o relatório.
- **`conftest.py`** fornece a fixture compartilhada do navegador e registra
  screenshots quando um teste falha.
- **Selenium WebDriver** inicializa e controla o Chrome.
- **Page Objects** encapsulam localizadores, navegação e interações com cada
  página; os testes ficam responsáveis pelas validações.
- **OWASP Juice Shop** é a aplicação funcional validada pelos cenários.

## Estrutura do projeto

```text
.
├── .github/
│   └── workflows/
│       ├── .gitkeep
│       └── testes.yml
├── configuracoes/
│   ├── __init__.py
│   ├── ambiente.py
│   └── navegador.py
├── dados/
│   └── __init__.py
├── evidencias/
│   └── .gitkeep
├── paginas/
│   ├── __init__.py
│   ├── pagina_base.py
│   ├── pagina_cadastro.py
│   ├── pagina_carrinho.py
│   ├── pagina_detalhes_produto.py
│   ├── pagina_inicial.py
│   ├── pagina_login.py
│   └── pagina_produtos.py
├── relatorios/
│   └── .gitkeep
├── testes/
│   ├── __init__.py
│   └── teste_fluxos_iniciais.py
├── utilitarios/
│   └── __init__.py
├── .env.example
├── .gitignore
├── conftest.py
├── pytest.ini
├── README.md
└── requirements.txt
```

- **`configuracoes/`**: endereço da aplicação e opções de inicialização do Chrome.
- **`dados/`**: espaço reservado para dados de teste.
- **`evidencias/`**: screenshots criados quando há falhas.
- **`paginas/`**: Page Objects e comportamentos compartilhados entre páginas.
- **`relatorios/`**: relatório HTML gerado pelo Pytest.
- **`testes/`**: cenários E2E automatizados.
- **`utilitarios/`**: espaço reservado para utilitários compartilhados.
- **`.github/workflows/`**: workflow de CI do GitHub Actions.

## Cenários automatizados

### Fluxos funcionais

- Acessar a página inicial e validar seu conteúdo principal.
- Acessar a página de login.
- Tentar login com credenciais inválidas e validar a resposta da aplicação.
- Preencher os campos obrigatórios do cadastro sem enviar o formulário.
- Pesquisar produtos e validar resultados relacionados.
- Abrir os detalhes de um produto e validar nome, descrição e preço.
- Adicionar um produto ao carrinho e confirmar sua presença.
- Avançar a paginação e validar a exibição de outro conjunto de produtos.

### Cenários negativos

- Login com campos obrigatórios vazios.
- Login com formato de e-mail malformado.
- Cadastro incompleto.
- Confirmação de senha diferente da senha informada.
- Pesquisa sem resultados.
- Tentativa de diminuir a quantidade do carrinho abaixo de uma unidade.

## Práticas aplicadas

- Page Object Model para centralizar seletores e interações com a interface.
- Separação entre ações da página e verificações feitas pelos testes.
- `WebDriverWait` e esperas explícitas para sincronizar interações.
- Fixture do Pytest para criar e encerrar um navegador por teste.
- Testes independentes, com o estado necessário preparado no próprio cenário.
- Reutilização de comportamentos comuns na página base.
- Relocalização de elementos atualizados dinamicamente no carrinho.
- Captura de screenshots em falhas.
- Execução do Chrome em modo headless no GitHub Actions.
- Versionamento com Git e execução contínua pelo GitHub Actions.

## Evidências de falhas

Quando uma fase de preparação ou execução falha e o WebDriver está disponível,
o hook do Pytest usa o próprio Selenium para salvar uma captura `.png` em
`evidencias/`. O nome do arquivo inclui o identificador do teste e a data e hora
da captura. Se a gravação da imagem falhar, o erro é registrado sem mascarar a
falha original do teste.

## Relatório HTML

O projeto utiliza `pytest-html`. Ao executar a suíte, o relatório autocontido é
gerado em `relatorios/relatorio.html`:

```powershell
python -m pytest
```

Abra esse arquivo em um navegador para consultar resultados, duração e resumo
da execução. O relatório é um artefato local de execução e está excluído do
versionamento pelo `.gitignore`.

## Executar localmente

### Pré-requisitos

- Python 3.13.
- Git.
- Docker em execução.
- Google Chrome e conexão à internet para o Selenium Manager obter um
  ChromeDriver compatível, se necessário.

### Clonar o projeto

```bash
git clone https://github.com/lucasjoseaa/Selenium-JuiceShop_LucasJose.git
cd Selenium-JuiceShop_LucasJose
```

### Criar o ambiente virtual

```bash
python -m venv .venv
```

### Ativar o ambiente virtual

Git Bash:

```bash
source .venv/Scripts/activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Iniciar o Juice Shop

O projeto usa a imagem oficial pré-compilada `bkimminich/juice-shop:v20.2.0`
no GitHub Actions. Para executar localmente a mesma versão, inicie o Docker e
execute:

```bash
docker run --detach --name juice-shop --publish 3000:3000 bkimminich/juice-shop:v20.2.0
```

Aguarde a inicialização e confirme que a aplicação está acessível em
`http://localhost:3000` antes de rodar os testes. Para parar e remover o
contêiner ao terminar:

```bash
docker rm --force juice-shop
```

### Executar os testes

Na raiz do projeto, com o ambiente virtual ativado e o Juice Shop disponível:

```bash
python -m pytest
```

O Chrome abre com interface por padrão. Para executá-lo em modo headless,
configure `CHROME_HEADLESS=true` no ambiente ou no arquivo `.env`.

## GitHub Actions / CI

O workflow [`.github/workflows/testes.yml`](.github/workflows/testes.yml) roda
em `push` e `pull_request`, usando um runner Ubuntu. Ele configura Python 3.13,
Node.js 24 e Google Chrome; inicia a imagem pré-compilada do Juice Shop v20.2.0;
aguarda a aplicação ficar disponível; e executa os testes Selenium em modo
headless. O Pytest gera o relatório HTML, publicado como artifact. Screenshots
também são publicados como artifact quando existem falhas que os geram. A
publicação é tentada mesmo quando os testes falham, sem alterar o resultado do
job.

Repositório: [Selenium-JuiceShop_LucasJose](https://github.com/lucasjoseaa/Selenium-JuiceShop_LucasJose).

## Resultado validado

- **Execução local:** 14 testes aprovados.
- **GitHub Actions:** workflow executado com sucesso em runner `ubuntu-latest`.
  [Ver execução validada](https://github.com/lucasjoseaa/Selenium-JuiceShop_LucasJose/actions/runs/36769144974).
- **Artifact:** relatório HTML publicado nessa execução do workflow.

## Observações

A cobertura atual é funcional e não pretende abranger todas as páginas e
funcionalidades do Juice Shop. A interface da versão validada não disponibiliza
navegação por categorias; o cenário correspondente foi substituído pela
validação da paginação. Os testes do carrinho não realizam checkout.

## Autor

**Lucas José — QA Engineer Jr.**

[GitHub](https://github.com/lucasjoseaa) · Projeto desenvolvido para o portfólio
de QA Automation.
