# Passo a passo de Execução



## Setup do Ollama

```bash

# 1. Instalar Ollama (ollama.ai)
# 2. Baixar um modelo leve
ollama pull gpt-oss

# 3. Testar se funciona
ollama run gpt-oss "Olá!"
```

## Código Completo

Todo código-fonte está no arquivo `app.py`.


## Como Rodar

```bash
# 1. Instalar Dependências
pip install streamlit pandas requests

# 2. Garantir que o Ollama está rodando
ollama serve

# 3. Rosas o app
streamlit run .\src\app.py
```
