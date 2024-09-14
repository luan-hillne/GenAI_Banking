import pandas as pd
import numpy as np
import json
from qdrant_client import QdrantClient, models
import tqdm
from fastembed.embedding import TextEmbedding
from fastembed.sparse.bm25 import Bm25
from fastembed.late_interaction import LateInteractionTextEmbedding
from qdrant_client import QdrantClient, models
from src.utils.load_db import load_dataset, create_client
from config_app.model_config import LoadConfig

APP_CONFIG = LoadConfig()
dataset = load_dataset(df=pd.read_excel(APP_CONFIG.csv_directory))

client = create_client(APP_CONFIG.url_qdrant, APP_CONFIG.api_key_qdrant, APP_CONFIG.qdrant_name, APP_CONFIG.batch_size)

dense_embedding_model = TextEmbedding(APP_CONFIG.dense_model)
dense_embeddings = list(dense_embedding_model.passage_embed(dataset[0]["text"]))
bm25_embedding_model = Bm25(APP_CONFIG.bm25_model)
bm25_embeddings = list(bm25_embedding_model.passage_embed(dataset[0]["text"]))
late_interaction_embedding_model = LateInteractionTextEmbedding(APP_CONFIG.colbert_embedding_model)
late_interaction_embeddings = list(late_interaction_embedding_model.passage_embed(dataset[0]["text"]))
    
def run_search(query_text: str, limit, threshold) -> str:
    query_dense_embedding = next(dense_embedding_model.query_embed([query_text]))
    query_bm25_embedding = next(bm25_embedding_model.query_embed([query_text]))
    late_query_vector = next(late_interaction_embedding_model.query_embed([query_text]))

    prefetch = [
        models.Prefetch(
            query=query_dense_embedding,
            using=APP_CONFIG.dense_model,
            limit=20,
        ),
        models.Prefetch(
            query=models.SparseVector(**query_bm25_embedding.as_object()),
            using="bm25",
            limit=20,
        ),
        models.Prefetch(
            query=late_query_vector,
            using="colbertv2.0",
            limit=20,
        ),
    ]
    results = client.query_points(
        APP_CONFIG.qdrant_name,
        prefetch=prefetch,
        query=models.FusionQuery(
            fusion=models.Fusion.RRF,
        ),
        with_payload=True,
        limit=limit,
    )

    script = ""
    for doc, score in results:
        for i in range(len(score)):
            if score[i].score > threshold:
            # print(score[i].payload)
                script += f"Example {i+1}:\n\nParagraph: {score[i].payload['text']}\n\nText_to_Rules: {score[i].payload['rules']}\n\n"
    return script