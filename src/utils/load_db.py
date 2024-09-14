import pandas as pd
import tqdm
from qdrant_client import QdrantClient, models
from fastembed.embedding import TextEmbedding
from fastembed.sparse.bm25 import Bm25
from fastembed.late_interaction import LateInteractionTextEmbedding
from config_app.model_config import LoadConfig

# Load configuration
APP_CONFIG = LoadConfig()
# Load dataset
df = pd.read_excel(APP_CONFIG.csv_directory)

# Function to prepare the dataset
def load_dataset(df):
    return [
        {
            "_id": index + 1,
            "text": row['text'],
            "rules": row['rules']
        }
        for index, row in df.iterrows()
    ]

# Initialize embeddings
dense_embedding_model = TextEmbedding(APP_CONFIG.dense_model)
bm25_embedding_model = Bm25(APP_CONFIG.bm25_model)
late_interaction_embedding_model = LateInteractionTextEmbedding(APP_CONFIG.colbert_embedding_model)

# Generate initial embeddings for vector size
dataset = load_dataset(df)
dense_embeddings = list(dense_embedding_model.passage_embed(dataset[0]["text"]))
late_interaction_embeddings = list(late_interaction_embedding_model.passage_embed(dataset[0]["text"]))

# Batching generator function
def batch_generator(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

def create_client(url, api_key, qdrant_name, batch_size):
    client = QdrantClient(url=url, api_key=api_key)
    
    # Create collection with vector configurations
    try:
        client.create_collection(
            qdrant_name,
            vectors_config={
                "BAAI/bge-base-en-v1.5": models.VectorParams(
                    size=len(dense_embeddings[0]),
                    distance=models.Distance.COSINE,
                ),
                "colbertv2.0": models.VectorParams(
                    size=len(late_interaction_embeddings[0][0]),
                    distance=models.Distance.COSINE,
                    multivector_config=models.MultiVectorConfig(
                        comparator=models.MultiVectorComparator.MAX_SIM,
                    )
                ),
            },
            sparse_vectors_config={
                "bm25": models.SparseVectorParams(
                    modifier=models.Modifier.IDF,
                )
            }
        )
        for batch in tqdm.tqdm(batch_generator(dataset, batch_size), total=len(dataset) // batch_size):
          ids = [str(doc['_id']) for doc in batch]
          texts = [doc['text'] for doc in batch]
          rules = [doc['rules'] for doc in batch]

          dense_embeddings = list(dense_embedding_model.passage_embed(texts))
          bm25_embeddings = list(bm25_embedding_model.passage_embed(texts))
          late_interaction_embeddings = list(late_interaction_embedding_model.passage_embed(texts))

          points = [
              models.PointStruct(
                  id=int(ids[i]),
                  vector={
                      "BAAI/bge-base-en-v1.5": dense_embeddings[i].tolist(),
                      "bm25": bm25_embeddings[i].as_object(),
                      "colbertv2.0": late_interaction_embeddings[i].tolist(),
                  },
                  payload={
                      "_id": ids[i],
                      "text": texts[i],
                      "rules": rules[i]
                  }
              )
              for i in range(len(ids))
          ]
        print("Data upload completed successfully.")
        client.upload_points(qdrant_name, points=points, batch_size=batch_size)
        
    except Exception as e:
        print("Collection creation failed or already exists:", e)
    
    return client

# Load client and upload data
# client = create_client(config_app['qdrant_config']['url'], config_app['qdrant_config']['api_key'])
# upload_batches(client, batch_size)
