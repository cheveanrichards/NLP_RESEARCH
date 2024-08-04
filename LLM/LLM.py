import os
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.replicate import Replicate
from transformers import AutoTokenizer

class Recommender:
    def __init__(self, api_token):
        self.model = None
        self.index = None
        self.query_engine = None
        self.set_api_token(api_token)

    def set_model(self, model_name, temperature=0.4, top_p=.1, max_new_tokens=300):
        Settings.llm = Replicate(
            model=model_name,
            temperature=temperature,
            additional_kwargs={"top_p": top_p, "max_new_tokens": max_new_tokens},
        )
        
        # Set tokenizer to match LLM
        if "llama-2-7b-chat" in model_name:
            Settings.tokenizer = AutoTokenizer.from_pretrained(
                "NousResearch/Llama-2-7b-chat-hf"
            )
        
        # Set the embed model
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        
        self.model = model_name

    def load_data(self, path):
        documents = SimpleDirectoryReader(path).load_data()
        self.index = VectorStoreIndex.from_documents(documents)

    def create_query_engine(self):
        if not self.index:
            raise ValueError("Index not created. Use load_data() method first.")
        self.query_engine = self.index.as_query_engine()

    def get_index(self):
        if not self.index:
            raise ValueError("Index not created. Use load_data() method first.")
        return self.index

    def set_api_token(self, token):
        os.environ["REPLICATE_API_TOKEN"] = token

    def query(self, question):
        if not self.query_engine:
            raise ValueError("Query engine not created. Use create_query_engine() method first.")
        return self.query_engine.query(question)