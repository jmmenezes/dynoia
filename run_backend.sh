#!/bin/bash

echo "Iniciando DynoIA Backend..."

cd backend

# Ativar ambiente virtual
source venv/bin/activate

echo "Iniciando servidor FastAPI..."
python main.py
