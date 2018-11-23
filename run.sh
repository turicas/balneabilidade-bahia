#!/bin/bash

set +e

DATA_PATH=data
LOG_PATH=$DATA_PATH/log
OUTPUT_PATH=$DATA_PATH/output
BOLETIM_BA="$OUTPUT_PATH/ba-boletim.csv"
BALNEABILIDADE_BA="$OUTPUT_PATH/ba-balneabilidade.csv"

run_spider() {
	scrapy runspider "$1" \
		-s HTTPCACHE_ENABLED=False \
		--logfile=$3 \
		-o "$2"
}

rm -rf data/output data/log
mkdir -p data/output data/log data/download

time run_spider ba_lista_boletim.py "$BOLETIM_BA" "$LOG_PATH/ba-lista-boletim.log"
gzip "$BOLETIM_BA"
time run_spider ba_extrai_boletim.py "$BALNEABILIDADE_BA" "$LOG_PATH/ba-extrai-boletim.log"
gzip "$BALNEABILIDADE_BA"

