import streamlit as st
from agent import load_agent, StreamlitCallbackHandler, StreamlitChatMessageHistory, ConversationBufferMemory


# Configuração da página do Streamlit
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="wide",
)

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

    with tab2:
        # Carregar o conteúdo do arquivo de instruções
        markdown_content = load_markdown_file("data\Instrucoes_chat_bot.txt")    # Altere para "instrucoes.md" se renomeou o arquivo
        
        # Exibir o conteúdo formatado
        st.markdown(markdown_content, unsafe_allow_html=True)


    with tab3:
        st.write("Aqui você pode ver o histórico de conversas.")
        column_novo, column_mostrar_chat = st.columns([0.1, 0.9])

        conteiner_chat = st.container()
        
        while len(st.session_state.messages) > 10:
            st.session_state.messages.pop(0)
        
        with column_novo:
            if st.button("Novo", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chat_messages = []
                msg = StreamlitChatMessageHistory()
                st.session_state.memory = ConversationBufferMemory(
                        messages=msg, memory_key="chat_history", return_messages=True
                    )

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

    with tab1:
        readme = load_markdown_file("README.md")
        st.markdown(readme, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    if prompt := st.chat_input("🤖: O que você deseja consultar?", key="chat_input"):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.toast("Pensando...".strip(), icon="🤖")
        run(prompt)
    else:
        run()    
