#!/bin/bash

# Script para iniciar o servidor web simples
# Uso: ./start_webserver.sh [port]

PORT=${1:-6789}

echo "======================================"
echo "Iniciando Servidor Web Simples"
echo "Porta: $PORT"
echo "======================================"

cd "$(dirname "$0")"
python webserver.py $PORT
