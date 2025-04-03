from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams , PointStruct

texts = [
    "This is a test sentence",
    "This is another test sentence",
]

model = SentenceTransformer('all-MiniLM-L6-v2')

emmbeddings = model.encode(texts, show_progress_bar=True)

points = [
    PointStruct(id= i + 1, 
    vector=emmbedding.tolist())
    for i, emmbedding in enumerate(emmbeddings)
]

# print("Embedding shape:", emmbedding.shape)
# print("Embedding:", emmbedding)

client = QdrantClient(url="http://localhost:6333")


# client.create_collection(
#     collection_name="test_collection",
#     vectors_config=VectorParams(
#         size=384,
#         distance=Distance.DOT
# ))

client.upsert("test_collection",points=points)
                         

