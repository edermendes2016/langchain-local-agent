# Para que serve e uso em empresas

## O que a solução faz

Indexa o código de um ou mais repositórios e responde perguntas em português sobre ele, sempre mostrando de onde veio cada informação (arquivo, linha e o trecho). Tudo roda na máquina: embeddings, banco vetorial, LLM e interface. Não há chave de API nem envio de código para fora.

## Dores que resolve

- **Entrar num código desconhecido.** Achar onde algo é feito em milhares de arquivos leva horas. Aqui, uma pergunta devolve os trechos candidatos em segundos.
- **Estudar arquitetura.** Perguntar "onde e como isso é inicializado" e ir direto ao ponto em vez de navegar por pasta.
- **Revisão e auditoria técnica.** Levantar rapidamente como uma regra de negócio, uma validação ou um limite está implementado.
- **Treinar o olhar crítico.** Os trechos e notas de relevância ficam visíveis, então dá para conferir a resposta da IA em vez de aceitá-la. Veja o [Dojo](Dojo).
- **Equipes que não podem usar IA paga na nuvem.** Código proprietário, dados de clientes ou regras internas não precisam sair da empresa.

## Privacidade, custo e operação

| Tema | Como a solução ajuda | Limite a conhecer |
|---|---|---|
| Privacidade e LGPD | O código e as perguntas não saem do computador ou do servidor da empresa, o que reduz a exposição de dados a terceiros. | Isso não substitui a avaliação do jurídico e do time de segurança. Ao clonar repositórios do GitHub e baixar modelos, há tráfego de rede na primeira vez. Para código interno use repositórios locais. |
| Custo | Não há cobrança por token ou por usuário. O custo é o hardware (que muitas empresas já têm). | A qualidade acompanha o hardware: modelos melhores pedem mais RAM ou GPU. |
| Offline | Depois que imagens, modelos e repositórios estão nos volumes, a consulta não deveria depender de internet. | O primeiro start precisa de internet, e eu não testei a stack isolada da rede. Valide no seu ambiente. |
| Auditoria | Cada resposta cita as fontes, e as notas de similaridade e reranking ajudam a decidir quanto confiar. | A interface não tem login. Em rede compartilhada, coloque atrás de VPN ou de um proxy com autenticação. |

## Limites honestos do modelo

Os números abaixo vêm das 30 perguntas de referência do projeto ([Avaliação](Avaliacao)).

| Modelo e ambiente | Citaram o arquivo certo | Citaram o arquivo e as palavras-chave | Tempo médio por resposta |
|---|---|---|---|
| `prism-ml/bonsai-27b` no LM Studio, langchain (18 perguntas) | 14 de 18 | 11 de 18 | 49 s |
| `qwen2.5-coder:3b` no Docker, langchain (18 perguntas) | 11 de 18 | 3 de 18 | 18 s |

Leitura direta: o modelo de 3 bilhões de parâmetros é o que roda em qualquer máquina com 8 GB de RAM e responde rápido, mas parafraseia mais, erra detalhes e tem mais chance de afirmar com confiança algo que o trecho não diz. Um modelo de 7B ou maior, de preferência numa GPU, tende a melhorar a precisão (o 27B foi melhor na checagem de palavras-chave). Não medimos o 7B neste projeto, então trate essa melhora como hipótese a validar com o seu repositório e o `evaluate.py`.

Outro limite que não depende do modelo: se o trecho certo não for recuperado, nenhum modelo acerta. Por isso a recuperação é medida separadamente.

## Como escalar

1. **Modelo melhor.** Troque `LLM_MODEL` no `.env` (por exemplo `qwen2.5-coder:7b`) e, com GPU NVIDIA, use `docker-compose.gpu.yml`.
2. **Mais repositórios.** Cada repositório vira um bloco no `docker/repos.docker.yaml` com a sua própria coleção. Veja [Outro repositório](Outro-repositorio).
3. **Servidor compartilhado.** A stack já separa Ollama, Chroma e agente. Rode em um servidor da empresa e acesse pela rede, com autenticação na frente.
4. **Qualidade medida.** Monte perguntas de referência do seu código (`eval/<repo>.yaml`) e acompanhe `hit@k` e `MRR` a cada mudança de modelo, tamanho de bloco ou reranker.
5. **Próximos passos técnicos.** Reindexação incremental por arquivo alterado (hoje a reindexação é completa), busca híbrida e blocos por função em vez de por tamanho.

## Onde começar numa equipe

Uma boa primeira semana: indexar um repositório real, escrever 10 perguntas cujas respostas a equipe conhece, medir com `evaluate.py` e só então decidir se vale subir para um modelo maior. Em paralelo, usar o [Dojo](Dojo) para treinar a leitura crítica das respostas.
