#!/bin/bash
# Sobe o servidor Ollama e baixa sozinho os modelos no primeiro start (ficam no volume).
set -u

ollama serve &
SERVER_PID=$!

until ollama list >/dev/null 2>&1; do sleep 1; done

for model in "${LLM_MODEL:-qwen2.5-coder:3b}" "${EMBEDDING_MODEL:-nomic-embed-text}"; do
  for attempt in 1 2 3 4 5; do
    echo "[ollama] baixando ${model} (tentativa ${attempt})..."
    if ollama pull "${model}"; then break; fi
    sleep 5
  done
done
echo "[ollama] modelos prontos."

wait "${SERVER_PID}"
