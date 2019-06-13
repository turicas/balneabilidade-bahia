# Dados de Balneabilidade da Costa Brasileira

Conjunto de programas que baixam boletins de balneabilidade (condição que
indica se água está própria ou não para banho) de diversas praias da costa
brasileira, extraem, limpam e exportam os dados normalizados. As fontes dos
dados são:

- Bahia: [INEMA](http://balneabilidade.inema.ba.gov.br)
- Santa Catarina: [FATMA](http://www.fatma.sc.gov.br/laboratorio/dlg_balneabilidade2.php)


## Licença

A licença do código é [LGPL3](https://www.gnu.org/licenses/lgpl-3.0.en.html) e
dos dados convertidos [Creative Commons Attribution
ShareAlike](https://creativecommons.org/licenses/by-sa/4.0/). Caso utilize os
dados, **cite a fonte original e quem tratou os dados**, como: **Fonte:
INEMA/BA e FATMA/SC, dados tratados por Álvaro
Justen/[Brasil.IO](https://brasil.io/)**. Caso compartilhe os dados, **utilize
a mesma licença**.


## Dados

Caso você não queira/possa rodar o script, **[acesse diretamente os dados
convertidos no Brasil.IO](https://brasil.io/dataset/balneabilidade-bahia)**.

Se esse programa e/ou os dados resultantes foram úteis a você ou à sua empresa,
considere [fazer uma doação ao projeto Brasil.IO](https://brasil.io/doe), que é
mantido voluntariamente.


## Rodando

Esse script depende de Python 3.6 e de algumas bibliotecas. Instale-as
executando:

```bash
pip install -r requirements.txt
```

Você pode rodar o script para apenas um arquivo ou para baixar todos os
arquivos.

### Rodando para um arquivo

O programa de linha de comando `extract.py` faz a extração de um único arquivo,
que pode estar em sua máquina ou mesmo disponível em algum site. Passe a sigla
do estado que deseja extrair, o arquivo de origem e o arquivo de destino.

Exemplo para Bahia:

```bash
URL="http://balneabilidade.inema.ba.gov.br/index.php/relatoriodebalneabilidade/geraBoletim?idcampanha=36381"
python extract.py BA "$URL" BA-36381.csv
```

O boletim será baixado de `$URL`, extraído e o resultado será gravado em
`BA-36381.csv`.

Exemplo para Santa Catarina:

```bash
URL="http://www.fatma.sc.gov.br/laboratorio/relatorio_ficha2.php?simplificado=1&where=0&d1=2018-01-01&d2=2018-12-31&mc=2&pc=72"
python extract.py SC "$URL" SC-floripa-2018.csv
```

O boletim será baixado de `$URL`, extraído e o resultado será gravado em
`SC-floripa-2018.csv`.


### Baixando todos os arquivos

Existe um script que roda todos os spiders (para todos os estados disponíveis):

```bash
./run.sh
```

Os arquivos finais serão criados no diretório `data/output`.


## Testando

Instale as dependências de desenvolvimento:

```bash
pip install -r dev-requirements.txt
```

Rode os testes:

```bash
pytest
```
