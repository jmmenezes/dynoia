#!/bin/bash

echo "Iniciando DynoIA Frontend..."

cd frontend

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "Instalando dependências do Node.js..."
    npm install --legacy-peer-deps
fi

echo "Iniciando servidor Angular..."
npm start
