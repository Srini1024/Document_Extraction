# import os 


# UPLOAD_DIR = 'uploads'
# a=os.listdir(UPLOAD_DIR)
# print(a)
 
from langchain_text_splitters import RecursiveCharacterTextSplitter
text = "This is a long document that needs to be chunked for processing."
print(f"len: {len(text)}")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=20, chunk_overlap=9)
texts = text_splitter.split_text(text)
 
 
 
# splitter = CharacterTextSplitter(
#     chunk_size=20,
#     chunk_overlap=5
# )
 
chunks = text_splitter.split_text(text)
print(chunks)