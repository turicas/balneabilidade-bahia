# Dados de Balneabilidade da Costa Brasileira

Conjunto de programas que baixam boletins de balneabilidade (condição que
indica se água está própria ou não para banho) de diversas praias da costa
brasileira, extraem, limpam e exportam os dados normalizados. As fontes dos
dados são:

- Bahia: [INEMA](http://balneabilidade.inema.ba.gov.br)
- Santa Catarina: [FATMA](http://www.fatma.sc.gov.br/laboratorio/dlg_balneabilidade2.php)


## Dados

[**Acesse diretamente os dados já
extraídos**](https://drive.google.com/open?id=1muf_9bG9xqwJPIz_g4Bui2ZCTsmOA8EZ).


## Rodando

Esse script depende de Python 3.6 e de algumas bibliotecas. Instale-as
executando:

```bash
pip install -r requirements.txt
```

Daí, basta executar (testado em sistema GNU/Linux - talvez precise de alteração
em Mac OS X e Windows):

```bash
./run.sh
```

Os arquivos finais serão criados no diretório `data/output`.
