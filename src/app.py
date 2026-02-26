import json
import pandas as pd
import requests
import streamlit as st


#------------------- Configuração OLLAMA -------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b"

#------------------------------
#Carregamento dos arquivos CSV
#------------------------------

historico = pd.read_csv('data/historico_atendimento.csv')

transacoes = pd.read_csv('data/transacoes.csv')

#-------------------------------
#Carregamento dos arquivos Json
#-------------------------------

with open('data/perfil_cliente.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)

with open('data/tipos_investimento.json', 'r', encoding='utf-8') as f:
    investimentos = json.load(f)
    
#----------------------
# Montagem do contexto
# ---------------------    

contexto = f"""

CLIENTE:
Nome: {perfil.get('nome', 'Não consta')}
Idade: {perfil.get('idade', 'Não consta')}
Estado civil: {perfil.get('estado_civil', 'Não consta')}
Cidade: {perfil.get('cidade', 'Não consta')}
Objetivo principal: {perfil.get('objetivo_principal', 'Não consta')}
Objetivo secundario: {perfil.get('objetivo_secundario', 'Não consta')}
Perfil de investidor: {perfil.get('perfil_investidor', 'Não consta')}

SITUAÇÃO FINANCEIRA:
Renda mensal: {perfil.get('renda_mensal', 'Não consta')}
Renda extra: {perfil.get('renda_extra', 'Não consta')}
Patrimonio: {perfil.get('patrimonio_total', 'Não consta')}
Reserva de emergência: {perfil.get('reserva_emergencia_atual', 'Não consta')}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

TIPOS DE INVESTIMENTOS:
{json.dumps(investimentos, indent=2, ensure_ascii=False)}
"""

#------------- SYSTEM PROMPT -----------
SYSTEM_PROMPT = """Você é a Ju, sua especialista em inteligência financeira.

OBJETIVO:
Dar apoio ao usuário nos controles de gastos e receitas, planejamento de metas e financeiros, e explicar ao usuário os melhores investimentos que ele pode fazer de acordo com o perfil de investidor dele.

REGRAS:
1. NUMCA solicite e armazene dados sensíveis, como senha, email e nem informações pessoais
2. Nunca invente ou diga informações que você não sabe
3. Se não souber algo, admita e ofereça alternativas
4. Seja claro, didático e objetivo nas suas respostas
5. Só ofereça recomendação de investimentos se o usuário solicitar
6. Só utilize dados fornecidos pelo usuário
7. Toda estratégia deve ser dividida por objetivos temporais. Exemplo: (curto prazo), (Médio prazo), (Longo prazo)
8. Cada análise de dados deve vir acompanhada de um insight educativo. O usuário deve se tornar mais inteligente financeiramente a cada interação.
9. Antes de sugerir ações ou investimentos voláteis, você deve verificar se o usuário já possui uma reserva para imprevistos (geralmente de 3 a 6 meses de gastos).
10. Ser honesta sobre riscos. Investimento não é mágica, é estratégia.
"""

#----------- FUNÇÃO PARA CHAMAR O OLLAMA ----------

def perguntar(msg):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

Pergunta do usuário:
{msg}
"""
    
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False
            },
            timeout=600 
        )

        data = r.json()

#--------- Tratamento robusto da resposta -----------

        if isinstance(data, dict):
            # Caso padrão: resposta direta
            if "response" in data:
                return data["response"]

            if "message" in data and "content" in data["message"]:
                return data["message"]["content"]

            if "error" in data:
                return f"⚠️ Erro do modelo: {data['error']}"

        return "⚠️ Não consegui interpretar a resposta do modelo."

    except requests.exceptions.Timeout:
        return "⏳ O modelo demorou demais para responder. Tente novamente."

    except requests.exceptions.ConnectionError:
        return "❌ Não foi possível conectar ao servidor OLLAMA. Verifique se ele está rodando."

    except Exception as e:
        return f"❌ Erro inesperado ao consultar o modelo: {str(e)}"

    
#------------- INTERFACE ----------
st.title("💸 Ju - Especialista em Inteligência Financeira")

st.markdown(
    "Fale comigo para que eu possa lhe ajudar em planejamento de metas, controle financeiro e investimentos "
)

if pergunta := st.chat_input("Me faça uma pergunta sobre sua dúvida sobre finanças"):
    st.chat_message("user").write(pergunta)

    with st.spinner("..."):
        resposta = perguntar(pergunta)
        st.chat_message("assistant").write(resposta)