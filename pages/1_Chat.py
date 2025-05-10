import streamlit as st

from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from utils.utils import page_config
from utils.document_loader import file_web, file_pdf, file_csv, file_txt, file_youtube
from utils.prompt import load_system_prompt


MEMORY = ConversationBufferMemory()
MEMORY.chat_memory.add_ai_message("Hi you. My name is **Insonia**, how can I help you today? You can type '/help' to see the available commands.")

FILE_TYPES_ACCEPTED = {
    'Site': {
        'label' : 'Web Page',
        'function' : file_web,
        'input' : lambda tab: tab.text_input("Enter the URL of the site", placeholder="https://example.com")
    },
    'PDF': {
        'label' : 'PDF Document',
        'function' : file_pdf,
        'input' : lambda tab: tab.file_uploader("Upload a PDF file", type='pdf')
    },
    'CSV': {
        'label' : 'CSV Document',
        'function' : file_csv,
        'input' : lambda tab: tab.file_uploader("Upload a CSV file", type='csv')
    },
    'TXT': {
        'label' : 'Text Document',
        'function' : file_txt,
        'input' : lambda tab: tab.file_uploader("Upload a TXT file", type='txt')
    },
    'Youtube': {
        'label' : 'Youtube Video',
        'function' : file_youtube,
        'input' : lambda tab: tab.text_input("Enter the URL of the Youtube video", placeholder="https://youtube.com/watch?v=example")
    },
}

LLM_PROVIDERS_TYPES = {
    'OpenAI': {
        'models': ['gpt-4.1-nano','gpt-4o-mini'],
        'llm_model': ChatOpenAI
    },
    'Groq': {
        'models': ['gemma2-9b-it','llama-3.3-70b-versatile','llama-3.1-8b-instant','llama-guard-3-8b','llama3-8b-8192'],
        'llm_model': ChatGroq
    },
}


def load_llm(provider, model, api_key, file_type_choosed, data):
    llm_config_load = LLM_PROVIDERS_TYPES[provider]['llm_model'](model=model, api_key=api_key)

    system_message = load_system_prompt(file_type_choosed, data)

    template = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
    ])

    chain = template | llm_config_load

    st.session_state['chain'] = chain
    

def chat():
    
    ia = st.session_state.get('chain', None)
    if ia is None:
        st.error("Please load a model in the sidebar")
        st.stop()
    
    memory = st.session_state.get("memory", MEMORY) # Initialize messages
    
    for message in memory.buffer_as_messages:
        chat = st.chat_message(message.type)
        chat.markdown(message.content)
        
    input_user = st.chat_input("Type a message")
    if input_user:
        memory.chat_memory.add_user_message(input_user)
        
        chat = st.chat_message('human')
        chat.markdown(input_user)
        
        chat = st.chat_message('ai')
        answer = chat.write_stream(ia.stream({'input': input_user, 'chat_history': memory.buffer_as_messages}))
        
        memory.chat_memory.add_ai_message(answer)
        
        st.session_state["memory"] = memory


def file_type_settings(file_type, tab1):
    
    if file_type in FILE_TYPES_ACCEPTED:
        input_data = FILE_TYPES_ACCEPTED[file_type]['input'](tab1)
        return input_data
    else:
        st.warning("Please select a valid file type")
        return None

def upload_file(file_type_choosed, input_data):
    if input_data:
        data = FILE_TYPES_ACCEPTED[file_type_choosed]['function'](input_data)
        try:
            return data
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")
            return None
    else:
        st.info("Nenhum dado fornecido.")
        return None

def side_bar():
    tab1, tab2 = st.sidebar.tabs(['File Upload', 'Model Settings'])
    
    file_type_choosed = tab1.selectbox("Select a type of file", list(FILE_TYPES_ACCEPTED))
    input_data = file_type_settings(file_type_choosed, tab1)


    btn_load = tab1.button("Load File", use_container_width=True)
    if btn_load:
        data = upload_file(file_type_choosed, input_data)
        print(data)

    
    provider_choosed = tab2.selectbox("Select a Provider", LLM_PROVIDERS_TYPES.keys())
    model_choosed = tab2.selectbox("Select a Model", LLM_PROVIDERS_TYPES[provider_choosed]['models'])
    
    api_key= tab2.text_input("Enter your API key", type="password", placeholder="sk-...", value=st.session_state.get(f'api_key_{provider_choosed}', ''))
    
    st.session_state[f'api_key_{provider_choosed}'] = api_key
    
    if tab2.button("Load LLM", use_container_width=True):
        load_llm(provider_choosed, model_choosed, api_key, file_type_choosed, data)

    

def main():
    page_config()
    side_bar()   
    chat()
    
    
        
        
    
if __name__ == "__main__":
    main()