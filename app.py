import streamlit as st
from agent import load_agent, StreamlitCallbackHandler, StreamlitChatMessageHistory, ConversationBufferMemory


# Configuração da página do Streamlit
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="wide",
)

# Função para carregar o conteúdo de um arquivo Markdown
def load_markdown_file(file_path):
    """
    Função para carregar o conteúdo de um arquivo Markdown.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Arquivo de instruções não encontrado."


# Função principal que inicia o aplicativo
def run(prompt=None):
    st.title("Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    tab1, tab2, tab3= st.tabs(["🛠️ Instalação e Questões Técnicas","📖 Instruções de Uso", "🤖 Chatbot", ])

    # Aba de instruções
    with tab2:
        # Carregar o conteúdo do arquivo de instruções
        markdown_content = load_markdown_file("data\Instrucoes_chat_bot.txt")    # Altere para "instrucoes.md" se renomeou o arquivo
        
        # Exibir o conteúdo formatado
        st.markdown(markdown_content, unsafe_allow_html=True)

    # Aba de chatbot
    with tab3:
        st.write("Aqui você pode ver o histórico de conversas.")
        column_novo, column_mostrar_chat = st.columns([0.1, 0.9])

        # Cria um container para exibir o chat
        conteiner_chat = st.container()
        
        # Limita o número de mensagens no histórico
        while len(st.session_state.messages) > 10:
            st.session_state.messages.pop(0)
        
        # Adiciona uma nova mensagem ao histórico
        with column_novo:
            if st.button("Novo", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chat_messages = []
                msg = StreamlitChatMessageHistory()
                st.session_state.memory = ConversationBufferMemory(
                        messages=msg, memory_key="chat_history", return_messages=True
                    )

        # Mostra o histórico de conversas
        with column_mostrar_chat:
            if st.button("Mostrar Histórico das Conversas", use_container_width=True):
                with conteiner_chat:
                    for message in st.session_state.chat_messages:
                        with st.chat_message(message["role"]):
                            st.write(message["content"].replace("R$ ", "R\$ "))
        
        # FAZ O STREAMLIT FICAR ATUALIZANDO O CHAT
        if prompt:
            with conteiner_chat:
                for message in st.session_state.chat_messages:
                    with st.chat_message(message["role"]):
                        st.write(message["content"].replace("R$ ", "R\$ "))

        # Cria um container para exibir o chat
            with st.chat_message("assistant"):
                st_callback = StreamlitCallbackHandler(st.container())
                agent_chain = load_agent(prompt)
                response  = agent_chain.invoke(
                    {"input": prompt},
                    {"callbacks": [st_callback]},
                )
                response_output = (response["output"].
                                replace("R$ ", "R\$ ")
                                .replace(".\n```", "")
                                .replace("```", "")
                                .replace("*", "\*").strip())                
                st.toast(response_output.replace("\n```",''), icon="🤖")
                st.markdown(response_output)
                st.session_state.chat_messages.append({"role": "assistant", "content": response_output})

    # Aba de instruções de instalção e questões técnicas
    with tab1:
        readme = load_markdown_file("README.md")
        st.markdown(readme, unsafe_allow_html=True)

if __name__ == "__main__":
    # Inicializa o histórico de mensagens
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # Exibe o chatbot
    # Se o usuário inserir um prompt, o chatbot responderá
    if prompt := st.chat_input("🤖: O que você deseja consultar?", key="chat_input"):
        
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Exibe uma mensagem de carregamento
        st.toast("Pensando...".strip(), icon="🤖")
        
        # Inicia o chatbot com o prompt inserido
        run(prompt)
    else:
        # Exibe o chatbot sem um prompt
        run()    
