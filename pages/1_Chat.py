import streamlit as st

from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq 

from utils.utils import page_config
from utils.document_loader import file_web, file_pdf, file_csv, file_txt, file_youtube





MEMORY = ConversationBufferMemory()
MEMORY.chat_memory.add_ai_message("Hi you. My name is **Insonia**, how can I help you today? You can type '/help' to see the available commands.")

FILE_TYPES_ACCEPTED = {
    'Site': {
        'label' : 'Web Page',
        'function' : file_web
    },
    'PDF': {
        'label' : 'PDF Document',
        'function' : file_pdf
    },
    'CSV': {
        'label' : 'CSV Document',
        'function' : file_csv
    },
    'TXT': {
        'label' : 'Text Document',
        'function' : file_txt
    },
    'Youtube': {
        'label' : 'Youtube Video',
        'function' : file_youtube
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


def load_llm(provider, model, api_key, file):
    llm_config_load = LLM_PROVIDERS_TYPES[provider]['llm_model'](model=model, api_key=api_key)
    st.session_state['llm_config'] = llm_config_load
    

def chat():
    
    ia = st.session_state.get('llm_config')
    
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
        answer = chat.write_stream(ia.stream(input_user))
        
        memory.chat_memory.add_ai_message(answer)
        
        st.session_state["memory"] = memory


def file_uploaded_settings(file_type, tab1):
    
    data = None
    
    if file_type == 'Site':
        url = tab1.text_input("Enter the URL of the site", placeholder="https://example.com")
        if url:
            data = file_web(url)
    elif file_type == 'PDF':
        file = tab1.file_uploader("Upload a PDF file", type='pdf')
        if file:
            data = file_pdf(file)
    elif file_type == 'CSV':
        file = tab1.file_uploader("Upload a CSV file", type='csv')
        if file:
            data = file_csv(file)
    elif file_type == 'TXT':
        file = tab1.file_uploader("Upload a TXT file", type='txt')
        if file:
            data = file_txt(file)
    elif file_type == 'Youtube':
        url = tab1.text_input("Enter the URL of the Youtube video", placeholder="https://youtube.com/watch?v=example")
        if url:
            data = file_youtube(url)
    else:
        st.warning("Please select a file type")
    return data



def side_bar():
    tab1, tab2 = st.sidebar.tabs(['File Upload', 'Model Settings'])
    
    file_type_choosed = tab1.selectbox("Select a type of file", FILE_TYPES_ACCEPTED)
    file = file_uploaded_settings(file_type_choosed, tab1)
    print(file)
    
    provider_choosed = tab2.selectbox("Select a Provider", LLM_PROVIDERS_TYPES.keys())
    model_choosed = tab2.selectbox("Select a Model", LLM_PROVIDERS_TYPES[provider_choosed]['models'])
    
    api_key= tab2.text_input("Enter your API key", type="password", placeholder="sk-...", value=st.session_state.get(f'api_key_{provider_choosed}', ''))
    
    st.session_state[f'api_key_{provider_choosed}'] = api_key
    
    if tab2.button("Load LLM", use_container_width=True):
        load_llm(provider_choosed, model_choosed, api_key, file)

    

def main():
    page_config()   
    chat()
    side_bar()
    
    
        
        
    
if __name__ == "__main__":
    main()