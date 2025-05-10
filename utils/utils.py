import streamlit as st
from utils.document_loader import file_web, file_pdf, file_csv, file_txt, file_youtube
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq



def page_config():
    st.set_page_config(
        page_title="Advanced AI Chatbot",
        page_icon="🤖",
        layout="wide"
    )


def introduction_markdown():
    st.markdown(
        """
        # 🤖 Advanced AI Chatbot with Web Scraping

        This intelligent chatbot application combines LangChain, web scraping capabilities, and a user-friendly Streamlit interface to deliver powerful, context-aware conversations.

        ## ✨ Features
        - **Smart Conversations**: Powered by LangChain for intelligent, contextual responses
        - **Web Scraping Integration**: Retrieve real-time information from websites
        - **Memory Management**: Remembers conversation context for more natural interactions
        - **Document Analysis**: Upload documents for the chatbot to analyze and discuss
        - **Real-time Responses**: Get immediate answers to your queries
        - **User-friendly Interface**: Clean, intuitive design for seamless interaction

        ## 🚀 How to Use
        1. **Start a Conversation**: Type your question in the chat input box
        2. **Web Research**: Use the "/search" command followed by a topic to scrape web data
        3. **Document Upload**: Click the upload button to analyze documents
        4. **Clear Context**: Reset the conversation with the "Clear Chat" button
        5. **Adjust Settings**: Customize bot behavior through the settings panel

        ## 🛠️ Technologies Used
        - **LangChain**: For advanced conversational capabilities and memory management
        - **Streamlit**: Powering our responsive and interactive user interface
        - **Beautiful Soup/Scrapy**: Enabling web scraping functionality
        - **Python**: Backend language for integration and logic
        - **Vector Databases**: For efficient information retrieval and context management

        ## 💡 Tips
        - Be specific with your questions for more accurate responses
        - Use web scraping for current events and real-time information
        - Upload relevant documents for more informed discussions
        - Try different prompting techniques to get the best results
        """
    )


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