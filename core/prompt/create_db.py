# extract data from url , save the vectore locally  with a uuid 
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import os
from langchain_community.vectorstores import FAISS
import uuid



class CreateData:

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'})
        
    
    def preprocess_text(self, raw_text):
        """
        Function to preprocess the raw HTML content by removing HTML tags and newlines.
        """
        # Parse the text using BeautifulSoup to remove HTML tags
        soup = bs4.BeautifulSoup(raw_text, "html.parser")
        cleaned_text = soup.get_text()  # Extract plain text from the HTML
        
        # Remove newline characters and extra spaces
        cleaned_text = cleaned_text.replace("\n", " ").strip()
        
        # Optional: Remove extra spaces (if you want to make the text more compact)
        cleaned_text = ' '.join(cleaned_text.split())

        return cleaned_text
    

    def extract_data(self, page_url):
        try:
            # Load the web page content
            loader = WebBaseLoader(web_paths=[page_url])
            docs = []
            
            for doc in loader.load():
                # Preprocess the document content
                cleaned_content = self.preprocess_text(doc.page_content)
                doc.page_content = cleaned_content  # Replace the original content with the cleaned version
                docs.append(doc)
                
            return docs

        except Exception as e:
            print(f"Error while extracting data from {page_url}: {e}")
            return []
        

    # generate embading for the same 
    def craete_fassidb(self , url , build_new=False):
        documents = self.extract_data(url)
        print(documents)
        unique_id = uuid.uuid4()
        db_path = f"fassi_db/{unique_id}/"
        # **Apply RecursiveCharacterTextSplitter**
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = text_splitter.split_documents(documents)


        if build_new or not os.path.exists(db_path):
            vectorstore = FAISS.from_documents(documents=split_docs, embedding=self.embeddings)
            vectorstore.save_local(db_path)

        self.db = FAISS.load_local(db_path, self.embeddings, allow_dangerous_deserialization=True)
        return str(unique_id) + '/'
    
    def retrive_similer_docs_using_fassi(self, question, path):
        # if not self.user_prompt_db:
        user_prompt_db = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
        
        retrieved_results = user_prompt_db.similarity_search(question, k=5)
        
        # Using '\n' to ensure proper formatting
        content = "\n\n".join(result.page_content for result in retrieved_results)
        
        return content

    

if __name__ == '__main__':
    print('done')
