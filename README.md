# gestao-br-scrapers

Scripts de scraping dos dados que serão usados no Gestão BR


## Preparando o Ambiente de Desenvolvimento

Esse projeto está sendo desenvolvido usando Python 3.5. Veja instruções de
instalação em seu sistema no site [python.org](http://www.python.org/).

Depois de ter o Python 3.5 instalado, você precisará instalar alguns outros
pacotes utilizando o gerenciador de pacotes
[pip](https://pypi.python.org/pypi/pip) (que já é instalado por padrão junto
com o Python 3.5). Se você usa Debian e derivados, basta executar:

    sudo apt-get install python3.5

Para criar o ambiente virtual, clonar o repositório e instalar as dependências
execute os seguintes comandos:

    sudo pip install virtualenv
    git clone https://github.com/CodeForCuritiba/gestao-br-scrapers.git
    cd gestao-br-scrapers
    virtualenv .env
    source .env/bin/activate
    pip install -r requirements/development.txt

Além de todas as dependências você precisará do [driver do Firefox para o
Selenium](https://github.com/mozilla/geckodriver/releases) (acesse o site e
veja as instruções de instalação para seu sistema).  Caso seu sistema


## Executando o Scraper

Para rodar os scripts você precisará estar em um terminal com o
[virtualenv](https://pypi.python.org/pypi/virtualenv) ativado - basta executar
os comandos abaixo a cada nova sessão do seu terminal:

    cd gestao-br-spiders
    source .env/bin/activate

### Prefeitura de Marmeleiro

O script `cli.py` é uma interface de linha de comando que:

- Recebe parâmetros de busca de licitações (ano e unidade gestora);
- Navega no [site da Prefeitura de
  Marmeleiro](http://www.marmeleiro.pr.gov.br/sitio/), faz a busca e baixa os
  HTMLs das páginas de resultado (*crawling*);
- Extrai os dados dos HTMLs baixados (*parsing*);
- Exporta os dados para um arquivo CSV.

Para rodá-lo, basta executar:

    python cli.py <ano> "<unidade gestora>"

Onde `<ano>` e `<unidade gestora>` são os possíveis valores apresentados no
formulário do site, a saber:

- `<ano>`: `2013`, `2014`, `2015`, `2016` ou `2017`.
- `<unidade gestora>`: `CONSOLIDADA`, `PREFEITURA MUNICIPAL`,
  `FUNDO MUNICIPAL DE SAÚDE` ou `ASSISTÊNCIA SOCIAL`.

> Note que caso a `<unidade gestora>` possua espaço você precisará colocar o
> parâmetro entre aspas na linha de comando.


## Metodologia de Trabalho

- Use a metodologia do [git
  flow](http://nvie.com/posts/a-successful-git-branching-model/) para criar
  seus *branches*;
- Use [Semantic Versioning](http://semver.org/) para nomear as versões;
- Sempre que possível crie [testes
  automatizados](https://en.wikipedia.org/wiki/Test-driven_development).
