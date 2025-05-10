from utils.document_loader import file_web, file_pdf, file_csv, file_txt, file_youtube

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