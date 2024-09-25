import os
from dotenv import load_dotenv
import yaml
import shutil
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


class LoadConfig:
    def __init__(self) -> None:
        with open("./config_app/config.yml") as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)
        
        self.load_directories(app_config=app_config)
        self.load_llm_config(app_config=app_config)
        self.load_chunk_config(app_config=app_config)
        self.load_retriver_config(app_config=app_config)
        self.load_qdrant_config(app_config=app_config)
        self.load_parameter_config(app_config=app_config)
        
    def load_directories(self, app_config):
        self.csv_directory = (
            app_config['directories']['csv_directory']
        )
        
    def load_llm_config(self, app_config):
        # Load parameters llm from load_config.yml file 
        self.rag_model = app_config['llm_config']['rag_model']
        self.temperature_rag = app_config['llm_config']['temperature_rag']
        self.temperature_chat = app_config['llm_config']['temperature_chat']
        self.max_token = app_config['llm_config']['max_token']
        
    def load_retriver_config(self, app_config):
        self.vector_embed_size = app_config['retriever_config']['vector_embed_size']
        self.embedding_model = app_config['retriever_config']['embedding_model']
        self.top_k = app_config['retriever_config']['top_k']
        self.score_thres = app_config['retriever_config']['score_thres']

    def load_qdrant_config(self, app_config):
        self.qdrant_name = app_config['qdrant_config']['qdrant_name']
        self.dense_model = app_config['qdrant_config']['dense_embedding_model']
        self.bm25_model = app_config['qdrant_config']['bm25_embedding_model']
        self.colbert_embedding_model = app_config['qdrant_config']['colbert_embedding_model']
        self.url_qdrant = app_config['qdrant_config']['url_qdrant']
        self.api_key_qdrant = app_config['qdrant_config']['api_key_qdrant']
        self.batch_size = app_config['qdrant_config']['batch_size']
    
    def load_chunk_config(self, app_config):
        self.chunk_size = app_config['chunk_config']['chunk_size']
        self.chunk_overlap = app_config['chunk_config']['chunk_overlap']

    def load_parameter_config(self, app_config):
        self.max_trial = app_config['parameter_config']['max_trial']
        self.retrieval_top_k = 5
        self.threshold = 0.4

    