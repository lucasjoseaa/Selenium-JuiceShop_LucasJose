# Automação E2E — OWASP Juice Shop com Selenium e Python

Projeto de estudo e prática de **QA Automation** que valida fluxos funcionais da aplicação web **OWASP Juice Shop** utilizando **Selenium WebDriver** e **Pytest**.

## Sobre o projeto

Esta suíte demonstra a automação de testes **end-to-end (E2E)** em uma aplicação web real.

O foco é **qualidade de software e validação funcional da interface**, não exploração de vulnerabilidades ou pentest.

O projeto contém **14 testes automatizados**, organizados com **Page Object Model (POM)**, e executa tanto localmente quanto no **GitHub Actions**.

## 🛠️ Tecnologias e Ferramentas

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="25" />
  <strong> Python 3.13</strong> — implementação e execução dos testes.
</p>

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/selenium/selenium-original.svg" width="25" />
  <strong> Selenium WebDriver</strong> — automação e controle do navegador.
</p>

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytest/pytest-original.svg" width="25" />
  <strong> Pytest</strong> — organização e execução dos testes e fixtures.
</p>

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/chrome/chrome-original.svg" width="25" />
  <strong> Google Chrome</strong> — navegador utilizado nos testes.
</p>

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="25" />
  <strong> Docker</strong> — execução do Juice Shop localmente e no CI.
</p>

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" width="25" />
  <strong> Node.js 24</strong> — configuração do ambiente utilizado pelo workflow.
</p>

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" width="25" />
  <strong> Git</strong> — versionamento do projeto.
</p>

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="25" />
  <strong> GitHub</strong> — hospedagem do repositório.
</p>

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/githubactions/githubactions-original.svg" width="25" />
  <strong> GitHub Actions</strong> — integração e execução contínua da suíte.
</p>

<p>
  <img src="https://cdn.simpleicons.org/owasp/000000" width="25" />
  <strong> OWASP Juice Shop v20.2.0</strong> — aplicação utilizada como sistema sob teste.
</p>

<p>
  <strong>▣ Page Object Model (POM)</strong> — padrão utilizado para separar os testes das interações com a interface.
</p>

<p>
  <strong>▣ pytest-html</strong> — geração do relatório HTML autocontido.
</p>

## 🏗️ Arquitetura

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

* **Pytest** coleta os cenários, executa as verificações e produz o relatório.
* **`conftest.py`** fornece a fixture compartilhada do navegador e registra screenshots quando um teste falha.
* **Selenium WebDriver** inicializa e controla o Chrome.
* **Page Objects** encapsulam localizadores, navegação e interações com cada página, mantendo os testes focados nas validações.
* **OWASP Juice Shop** é a aplicação funcional validada pelos cenários.

## 📁 Estrutura do projeto

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

* **`configuracoes/`** — endereço da aplicação e opções de inicialização do Chrome.
* **`dados/`** — espaço reservado para dados de teste.
* **`evidencias/`** — screenshots criados quando há falhas.
* **`paginas/`** — Page Objects e comportamentos compartilhados entre páginas.
* **`relatorios/`** — relatório HTML gerado pelo Pytest.
* **`testes/`** — cenários E2E automatizados.
* **`utilitarios/`** — espaço reservado para utilitários compartilhados.
* **`.github/workflows/`** — workflow de CI do GitHub Actions.

## 🧪 Cenários automatizados

A suíte possui atualmente **14 testes automatizados**.

### Fluxos funcionais

* Acessar a página inicial e validar seu conteúdo principal.
* Acessar a página de login.
* Tentar login com credenciais inválidas e validar a resposta da aplicação.
* Preencher os campos obrigatórios do cadastro sem enviar o formulário.
* Pesquisar produtos e validar resultados relacionados.
* Abrir os detalhes de um produto e validar nome, descrição e preço.
* Adicionar um produto ao carrinho e confirmar sua presença.
* Avançar a paginação e validar a exibição de outro conjunto de produtos.

### Cenários negativos

* Login com campos obrigatórios vazios.
* Login com formato de e-mail malformado.
* Cadastro incompleto.
* Confirmação de senha diferente da senha informada.
* Pesquisa sem resultados.
* Tentativa de diminuir a quantidade do carrinho abaixo de uma unidade.

## ✅ Práticas aplicadas

* **Page Object Model** para centralizar localizadores e interações com a interface.
* Separação entre ações das páginas e verificações realizadas pelos testes.
* `WebDriverWait` e esperas explícitas para sincronização das interações.
* Fixtures do Pytest para criação e encerramento do navegador.
* Testes independentes, com o estado necessário preparado no próprio cenário.
* Reutilização de comportamentos comuns na página base.
* Relocalização de elementos atualizados dinamicamente no carrinho.
* Captura automática de screenshots em falhas.
* Execução do Chrome em modo headless no GitHub Actions.
* Versionamento com Git.
* Integração contínua com GitHub Actions.

## 📸 Evidências de falhas

Quando uma fase de preparação ou execução falha e o WebDriver está disponível, o hook do Pytest utiliza o próprio Selenium para salvar uma captura `.png` em `evidencias/`.

O nome do arquivo inclui o identificador do teste e a data e hora da captura.

Se a gravação da imagem falhar, o erro é registrado sem mascarar a falha original do teste.

## 📊 Relatório HTML

O projeto utiliza **pytest-html** para gerar um relatório autocontido da execução.

Execute:

```bash
python -m pytest
```

O relatório é gerado em:

```text
relatorios/relatorio.html
```

Abra o arquivo em um navegador para consultar os resultados, duração e resumo da execução.

O relatório é um artefato local de execução e está excluído do versionamento pelo `.gitignore`.

## 🚀 Executar localmente

### Pré-requisitos

* Python 3.13
* Git
* Docker em execução
* Google Chrome
* Conexão com a internet para o Selenium Manager obter um ChromeDriver compatível, quando necessário

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

**Git Bash:**

```bash
source .venv/Scripts/activate
```

**PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Iniciar o Juice Shop

O projeto utiliza a imagem pré-compilada do **OWASP Juice Shop v20.2.0**.

Com o Docker em execução:

```bash
docker run --detach --name juice-shop --publish 3000:3000 bkimminich/juice-shop:v20.2.0
```

Aguarde a inicialização e confirme que a aplicação está disponível em:

```text
http://localhost:3000
```

Para parar e remover o contêiner:

```bash
docker rm --force juice-shop
```

### Executar os testes

Na raiz do projeto, com o ambiente virtual ativado e o Juice Shop disponível:

```bash
python -m pytest
```

O Chrome abre com interface por padrão.

Para executar em modo headless, configure:

```text
CHROME_HEADLESS=true
```

no ambiente ou no arquivo `.env`.

## ⚙️ GitHub Actions / CI

O workflow `.github/workflows/testes.yml` é executado em eventos de `push` e `pull_request`.

O pipeline:

1. utiliza um runner Ubuntu;
2. configura Python 3.13;
3. configura Node.js 24;
4. disponibiliza o Google Chrome;
5. inicia a imagem pré-compilada do Juice Shop v20.2.0;
6. aguarda a aplicação ficar disponível;
7. executa os testes Selenium em modo headless;
8. gera o relatório HTML;
9. publica o relatório como artifact;
10. publica screenshots como artifacts quando existem falhas.

A publicação dos artifacts é tentada mesmo quando os testes falham, sem alterar o resultado do job.

**Repositório:**
[Selenium-JuiceShop_LucasJose](https://github.com/lucasjoseaa/Selenium-JuiceShop_LucasJose)

## 📈 Resultado validado

* **Execução local:** 14 testes aprovados.
* **GitHub Actions:** workflow executado com sucesso em runner `ubuntu-latest`.
* **Relatório:** artifact HTML publicado na execução validada do workflow.

[Ver execução validada no GitHub Actions](https://github.com/lucasjoseaa/Selenium-JuiceShop_LucasJose/actions/runs/36769144974)

## ℹ️ Observações

A cobertura atual é funcional e não pretende abranger todas as páginas e funcionalidades do Juice Shop.

A interface da versão validada não disponibiliza navegação por categorias; por isso, o cenário correspondente foi substituído pela validação da paginação.

Os testes do carrinho não realizam checkout.

## 👤 Autor

**Lucas José — QA Engineer Jr.**

Projeto desenvolvido como parte do portfólio de **QA Automation**, com foco em automação E2E utilizando Selenium, Python e Pytest.
