# Bibliotecas padrão
import os
import requests
import http.client
import json

# Bibliotecas de terceiros
from dotenv import load_dotenv
import streamlit as st


# LangChain
from langchain import LLMChain, OpenAI
from langchain.agents import AgentExecutor, Tool, ConversationalAgent, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory


# LangChain Community
from langchain_community.chat_models import ChatOpenAI as CommunityChatOpenAI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.document_loaders import WikipediaLoader

# LangChain OpenAI
from langchain_openai.chat_models import ChatOpenAI as OpenAIChatOpenAI

# LangChain Google
from langchain_google_genai import GoogleGenerativeAI

# Own modules
from utils import consultar_atualizacao_atos_legais_infralegais, consultar_atualizacao_projetos_atos_legais_infralegais


# Carregar variáveis de ambiente
load_dotenv()

# Variáveis de ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")
secret = os.getenv("SECRET")
# conn = http.client.HTTPSConnection("google.serper.dev")
SERPER_API = os.getenv("SERPER_API")
GEMINI_KEY = os.getenv("GEMINI_KEY")



# Função que consulta a API do ControlGov para obter informações sobre CPF ou CNPJ
def consultar_cpf_cnpj(query: str) -> str:
    import requests

    url = "https://api.controlgov.org/embeddings/subelementos"
    payload = {"query": query, "secret": secret}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data.get("resposta", "Nenhuma resposta encontrada.")
    else:
        return f"Erro ao consultar a API: {response.status_code}"


# Função que consulta a API do ControlGov para obter informações sobre pessoas físicas e jurídicas
def consultar_PessoaFisica_PessoaJuridica(query: str) -> str:
    import requests

    url = "https://api.controlgov.org/embeddings/subelementos"
    payload = {"query": query, "secret": secret}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data.get("resposta", "Nenhuma resposta encontrada.")
    else:
        return f"Erro ao consultar a API: {response.status_code}"


# Função que consulta a API do ControlGov para obter informações sobre subelementos financeiros
def consultar_subelementos(query: str) -> str:
    import requests

    url = "https://api.controlgov.org/embeddings/subelementos"
    payload = {
        "query": query,
        "secret": secret,
    }  # É recomendável armazenar o secret em uma variável de ambiente
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        data["resposta"] = data["resposta"] + "\nFormatar valores em R$"
        return data.get("resposta", "Nenhuma resposta encontrada.")
    else:
        return f"Erro ao consultar a API: {response.status_code}"


# Função que consulta a API do ControlGov para obter informações sobre subelementos financeiros
def consultar_elementos(query: str) -> str:
    import requests

    url = "https://api.controlgov.org/embeddings/subelementos"
    payload = {
        "query": query,
        "secret": secret,
    }  # É recomendável armazenar o secret em uma variável de ambiente
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        data["resposta"] = data["resposta"] + "\nFormatar valores em R$"
        return data.get("resposta", "Nenhuma resposta encontrada.")
    else:
        return f"Erro ao consultar a API: {response.status_code}"


# Função que consulta a API do ControlGov para obter a soma dos valores empenhados
def consultar_empenhado_sum(query=None):
    import requests

    url = "https://api.controlgov.org/elementos/despesa/empenhado-sum/"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        elementos = data.get("elementos", [])

        if not elementos:
            return "Nenhum dado encontrado."

        resultado = "Soma dos Valores Empenhados por Elemento de Despesa:\n\n"
        for elemento in elementos:
            elemento_despesa = elemento.get("elemento_de_despesa", "Desconhecido")
            total_empenhado = elemento.get("total_empenhado", 0)
            resultado += f"• {elemento_despesa}: R$ {total_empenhado:,.2f}\n"

        return resultado

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro ao consultar a API: {e}"
    except ValueError:
        return "Erro ao processar a resposta da API."


# Função que lista os empenhos por elemento de despesa
def listar_empenhos_por_elemento(query=None):
    url = "https://api.controlgov.org/elementos/despesa/empenhado-sum/"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        elementos = data.get("elementos", [])

        if not elementos:
            return "Nenhum dado encontrado."

        # Se uma consulta específica for fornecida, filtrar os elementos
        if query:
            elementos = [
                elem
                for elem in elementos
                if query.lower() in elem.get("elemento_de_despesa", "").lower()
            ]
            if not elementos:
                return (
                    f"Nenhum empenho encontrado para o elemento de despesa: '{query}'."
                )

        resultado = "Empenhos por Elemento de Despesa:\n\n"
        for elemento in elementos:
            elemento_despesa = elemento.get("elemento_de_despesa", "Desconhecido")
            total_empenhado = elemento.get("total_empenhado", 0)
            resultado += f"• {elemento_despesa}: R$ {total_empenhado:,.2f}\n"

        return resultado

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro ao consultar a API: {e}"
    except ValueError:
        return "Erro ao processar a resposta da API."


# Função que consulta google para obter informações sobre um termo contábil ou financeiro
def consultar_atualizacao_atos_legais_infralegais_cmp(query=None) -> str:
    """
    Extrai dados da tabela da página especificada, processa-os e gera um relatório.
    
    Retorna:
        resposta (pd.DataFrame ou str): DataFrame contendo o relatório gerado ou uma mensagem de erro.
    """
    # URL da página
    resposta = consultar_atualizacao_atos_legais_infralegais()
    return resposta 

def consultar_atualizacao_projetos_atos_legais_infralegais_cmp(query=None) -> str:
    """
    Extrai dados da tabela da página especificada, processa-os e gera um relatório.
    
    Retorna:
        resposta (pd.DataFrame ou str): DataFrame contendo o relatório gerado ou uma mensagem de erro.
    """
    # URL da página
    resposta = consultar_atualizacao_projetos_atos_legais_infralegais()
    return resposta


# Função que gera a resposta do agente de atendimento
def load_agent(text):
    """
    Configura e retorna o executor do agente baseado no texto de entrada.
    
    Args:
        text (str): O prompt de entrada para o agente.
    
    Returns:
        AgentExecutor: O executor configurado para o agente.
    """
    
    # Consultar CPF ou CNPJ
    text = "Me responda apenas:\n" + text
    
    # Define ferraenta de consulta de atualização de atos legais e infralegais    
    atualizacao_projetos_atos_legais_infralegais = Tool(
        name="Consultar Atualização de Projetos de Atos Legais e Infralegais",
        func=consultar_atualizacao_projetos_atos_legais_infralegais_cmp,
        description=(
            "Use esta ferramenta para obter informações sobre a atualização dos projetos de atos legais e infralegais da Câmara Municipal de Pinhão/SE."
            "Atenção: Ordenar pela data mais recente."
            "Trate NAN como 'Não informado'."
            "Informar: Projeto e Data de Apresentação."
            "Formato de retorno: <LISTA> - Projeto -> Data de Apresentação(dd/mm/yyyy)"
        ),
    )
    
    # Define ferraenta de consulta de atualização de atos legais e infralegais
    atualizacao_atos_legais_infralegais = Tool(
        name="Consultar Atualização de Atos Legais e Infralegais",
        func=consultar_atualizacao_atos_legais_infralegais_cmp,
        description=(
            "Use esta ferramenta para obter informações sobre a atualização dos atos legais e infralegais da Câmara Municipal de Pinhão/SE."
            "Atenção: Ordenar pela data mais recente."
            "Trate NAN como 'Não informado'."
            "Informar: Tipo Aprovado,Tipo de Matéria - Numeração e Data de Publicação."
            "Formato de retorno: <LISTA> - Tipo de Matéria - Numração -> Data de Publicação(dd/mm/yyyy)"
        ),
    )

    # Definir a ferramenta de consulta de CPF ou CNPJ
    consultar_cpf_cnpj_tool = Tool(
        name="Consultar CPF ou CNPJ",
        func=consultar_cpf_cnpj,
        description=(
            "Use esta ferramenta para obter informações sobre CPF ou CNPJ de um credor."
            "Por exemplo, você pode perguntar: 'Qual o CPF do credor <nome> com asteriscos?' ou 'Qual o CNPJ do credor <nome>?'"
            "Se o usuário não informar o nome do credor, o agente solicitará o nome do credor."
        ),
    )

    # Define ferramenta de consulta de subelementos
    subelementos_tool = Tool(
        name="Consultar Subelemento Individualmente",
        func=consultar_subelementos,
        description=(
            "Use esta ferramenta para obter informações sobre alguns subelementos financeiros. "
            "Por exemplo, você pode perguntar: 'Qual o total empenhado para o subelemento <subelemento>?'"
        ),
    )

    # Define ferramenta de consulta de elementos
    elementos_tool = Tool(
        name="Consultar Elemento Individualmente",
        func=consultar_elementos,
        description=(
            "Use esta ferramenta para obter informações sobre alguns elementos financeiros. "
            "Por exemplo, você pode perguntar: 'Qual o total empenhado para o elemento <subelemento>?'"
        ),
    )

    # Define ferramenta de consulta de empenho por elemento
    empenho_pessoa_fisica_juridica = Tool(
        name="Consultar Empenho a Pessoa Física ou Jurídica",
        func=consultar_PessoaFisica_PessoaJuridica,
        description=(
            "Use esta ferramenta para obter informações sobre valores empenhados para Pessoa Física ou Pessoa Jurídica. "
            "Por exemplo, você pode perguntar: 'Qual o total empenhado para o credor <Pessoa Física>?' ou 'Qual o total empenhado para o credor <Pessoa Jurídica>?'"
        ),
    )

    # Define ferramenta de consulta de empenho por elemento
    empenhos_por_elemento_tool = Tool(
        name="Consultar o total empenhado para todos os Elementos de uma Vez",
        func=listar_empenhos_por_elemento,
        description=(
            "Use esta ferramenta para obter um jso com uma lista de empenhos por elemento de despesa. "
        ),
    )

    tools = [
        subelementos_tool,
        # empenhado_sum_tool,
        empenhos_por_elemento_tool,
        empenho_pessoa_fisica_juridica,
        consultar_cpf_cnpj_tool,
        elementos_tool,
        atualizacao_atos_legais_infralegais,
        atualizacao_projetos_atos_legais_infralegais,
        # categoria_tool  # Adiciona a nova ferramenta aqui
    ]

    # Prefixo e sufixo do prompt
    prefix = """# Assistente de Finanças Governamentais da Câmara Municipal de Pinhão/SE
    Você é um assistente direto e especializado em finanças governamentais.

    Você pode ajudar os usuários a consultar informações da Câmara Municipal de Pinhão/SE sobre:

    - Elementos e subelementos de despesa
    - Consultas aos valores empenhados a Pessoas Físicas e Jurídicas
    - Consultas a CPF ou CNPJ dos credores
    - Consultar Atualização de Atos Legais e Infralegais
    - Consultar Atualização de Projetos de Atos Legais e Infralegais

    ## Ferramentas Disponíveis

    Você tem acesso às seguintes ferramentas:

    1. Consultar Empenho a Pessoa Física ou Jurídica
    - *Descrição:* Use esta ferramenta para obter informações sobre valores empenhados para um credor PF ou PJ.
    
    2. Consultar CPF ou CNPJ
    - *Descrição:* Use esta ferramenta para obter informações sobre CPF ou CNPJ dos credores.
    
    3. Consultar Subelemento Individualmente
    - *Descrição:* Use esta ferramenta para obter informações sobre valores empenhados por subelemento de despesa.
    
    3. Consultar Elemento Individualmente
    - *Descrição:* Use esta ferramenta para obter informações sobre valores empenhados por elemento de despesa.
    
    4. Consultar Atualização de Atos Legais e Infralegais
    - *Descrição:* Use esta ferramenta para Consultar Atualização de Atos Legais e Infralegais da camara municipal de Pinhao.
    
    5. Consultar Atualização de Projetos de Atos Legais e Infralegais
    - *Descrição:* Use esta ferramenta para Consultar Atualização de Projetos de Atos Legais e Infralegais da camara municipal de Pinhao.

    ## Instruções para Uso das Ferramentas

    Para usar uma ferramenta, responda exatamente neste formato:
    Pensamento: [Seu raciocínio sobre a próxima ação a ser tomada] 
    Ação: [O nome da ferramenta a ser usada] 
    Entrada da Ação: [Os dados de entrada necessários para a ferramenta] 
    Observação: [O resultado da execução da ferramenta]
    Resposta Final: [Sua resposta ao usuário]
    
    
    Se você já tiver todas as informações necessárias para responder à pergunta do usuário, forneça a resposta final:
    Pensamento: Já tenho as informações necessárias para responder ao usuário. 
    """
    
    # Sufixo do prompt com histórico do chat e scratchpad do agente
    suffix = """

    Histórico do Chat:

    {chat_history}

    Última Pergunta: {input}
    
    Scratchpad do Agente (Raciocínio e Ações Anteriores):

    {agent_scratchpad}

    Sempre responda em Português.

    Responda apenas ao que foi perguntado. Evite demais informações.
    """

    # Criar o prompt do agente com as variáveis de entrada e ferramentas
    prompt = ConversationalAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "chat_history", "agent_scratchpad"],
    )

    # Configurar a memória
    msg = StreamlitChatMessageHistory()

    # Se a memória não existir, crie uma nova
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            messages=msg, memory_key="chat_history", return_messages=True
        )

    # Carregar a memória
    memory = st.session_state.memory

    # Configurar o LLM Chain 
    llm_chain = LLMChain(
        llm=CommunityChatOpenAI(temperature=0.5, model_name="gpt-4o-mini"),
        # llm=GoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_KEY),
        prompt=prompt,
        verbose=True,
    )

    # Configurar o agente conversacional com o LLM Chain, a memória e as ferramentas
    agent = ConversationalAgent(
        llm_chain=llm_chain,
        memory=memory,
        verbose=True,
        max_interactions=3,
        tools=tools,
    )

    # Configurar o executor do agente com o agente, ferramentas e memória
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        handle_errors=True,
        
    )

    return agent_executor
