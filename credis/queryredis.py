from langchain_community.embeddings import XinferenceEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore


url = "redis://:Chen@2024@127.0.0.1:6379/0"

# 设置 Xinference Embeddings 配置
server_url = "http://127.0.0.1:9997"  # 本地 Xinference 服务地址
model_uid_jina = 'jina-embeddings-v2-base-zh'
#model_uid = "your_model_uid"  # 使用实际的 Falcon-Instruct 模型的 model_uid

# 初始化 Xinference Embeddings，传递本地服务的 URL 和模型 UID
embeddings = XinferenceEmbeddings(server_url=server_url, model_uid=model_uid_jina)
indexname = "cailiang_idx"

config = RedisConfig(
    index_name= indexname,
    redis_url=url,
    metadata_schema=[
        {"name": "category", "type": "tag"},
    ],
)

vector_store = RedisVectorStore(embeddings, config=config)

query = "2024年9月12日14时当事人张来，在台州市椒江区白云街道1223号，白云广场西侧户外售卖衣物，但未办理相关营业执照。"
results = vector_store.similarity_search(query, k=2)

print("Simple Similarity Search Results:")
for doc in results:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
    print()

# filter_condition = Tag("category") == "sci.space"
# # Maximum marginal relevance search with filter
# mmr_results = vector_store.max_marginal_relevance_search(
#     query, k=2, fetch_k=10, filter=filter_condition
# )

# print("Maximum Marginal Relevance Search Results:")
# for doc in mmr_results:
#     print(f"Content: {doc.page_content[:100]}...")
#     print(f"Metadata: {doc.metadata}")
#     print()