import time
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from openai import RateLimitError

class RecipeQuerySystem:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.api_key = api_key
        self.llm = OpenAI(api_key=self.api_key)
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.rag_chain = None
        self.last_query_time = 0
        self.rate_limit_delay = 1  # 1 second delay between queries

    def create_documents(self, recipes):
        documents = []
        for recipe in recipes:
            text = f"Title: {recipe['title']}\nIngredients: {recipe['ingredients']}\nInstructions: {recipe['instructions']}"
            documents.append(Document(page_content=text, metadata=recipe))
        return documents

    def setup_rag_chain(self, recipes):
        documents = self.create_documents(recipes)
        split_docs = self.text_splitter.split_documents(documents)
        vector_store = FAISS.from_documents(split_docs, self.embeddings)
        retriever = vector_store.as_retriever()
        self.rag_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=retriever)

    def query_recipe(self, prompt):
        if not self.rag_chain:
            raise ValueError("RAG chain not set up. Please call setup_rag_chain() first.")
        
        # Implement rate limiting
        current_time = time.time()
        time_since_last_query = current_time - self.last_query_time
        if time_since_last_query < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_query)
        
        response = self.rag_chain.run(prompt)
        self.last_query_time = time.time()
        return response
    
api_key = "sk-None-uAcHNDlaauMkL9wTAqGHT3BlbkFJgekPKq3Re7YMkY55hWlM"
recipe_system = RecipeQuerySystem(api_key)

# Set up the system with your recipes
recipes = [
    {
        "title": "Spaghetti Carbonara",
        "ingredients": "400g spaghetti, 200g pancetta, 4 large eggs, 100g Pecorino cheese, 100g Parmesan, Black pepper",
        "instructions": "1. Cook spaghetti in salted water. 2. Fry pancetta until crispy. 3. Beat eggs with grated cheeses. 4. Drain pasta, mix with pancetta, then quickly stir in egg mixture. 5. Season with black pepper and serve."
    },
    # Add more recipes here...
]
recipe_system.setup_rag_chain(recipes)

try:
    response = recipe_system.query_recipe("How do I make Spaghetti Carbonara?")
    print(response)
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    print("Please wait a moment before trying again.")