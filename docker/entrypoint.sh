#!/bin/sh
set -e

# Espera Chroma e Ollama (com os modelos baixados), clona o repositório e indexa se a coleção estiver vazia.
python agent_local.py bootstrap

if [ "$#" -gt 0 ]; then
  exec "$@"          # ex.: docker compose run --rm agent python agent_local.py ask "..."
fi

echo ""
echo "=============================================================="
echo " Pronto! Abra http://localhost:8501 no navegador."
echo "=============================================================="
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
