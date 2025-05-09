from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, CSVLoader, PyPDFLoader, TextLoader
import tempfile

def file_web(url):
    loader = WebBaseLoader(url)
    data = loader.load()
    return data

def file_youtube(url):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False, language="pt")
    data = loader.load()
    return data

def file_csv(file):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    
    loader = CSVLoader(file)
    data = loader.load()
    return data

def file_pdf(file):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    loader = PyPDFLoader(file)
    data = loader.load()
    return data

def file_txt(file):
    loader = TextLoader(file)
    data = loader.load()
    return data
    