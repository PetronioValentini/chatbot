from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, CSVLoader, PyPDFLoader, TextLoader
import tempfile
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import streamlit as st

def file_web(url):
    loader = WebBaseLoader(url)
    data = loader.load()
    return data

def file_youtube(url):
    if not url:
        st.warning("Please provide a valid YouTube URL.")
        return None

    try:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=False, language="pt")
        data = loader.load()
        return data
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        st.error(f"Transcript not available: {str(e)}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while loading YouTube data: {str(e)}")
        return None

def file_csv(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name
    
    loader = CSVLoader(temp_file_path)
    data = loader.load()
    return data

def file_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)
    data = loader.load()
    return data

def file_txt(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name
    loader = TextLoader(temp_file_path)
    data = loader.load()
    return data
    