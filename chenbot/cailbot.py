from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import XinferenceEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore

def main(tongyi_chat):
    messages = []

    # 设置 Xinference Embeddings 配置
    server_url = "http://127.0.0.1:9997"  # 本地 Xinference 服务地址
    model_uid_jina = 'jina-embeddings-v2-base-zh'
    #model_uid = "your_model_uid"  # 使用实际的 Falcon-Instruct 模型的 model_uid

    # 初始化 Xinference Embeddings，传递本地服务的 URL 和模型 UID
    embeddings = XinferenceEmbeddings(server_url=server_url, model_uid=model_uid_jina)

    # 连接到 Redis
    url = "redis://:Chen@2024@127.0.0.1:6379/0"
    indexname = "cailiang_hz"
    
    embeddings = XinferenceEmbeddings(server_url=server_url, model_uid=model_uid_jina)

    config = RedisConfig(
        index_name=indexname,
        redis_url=url,
        metadata_schema=[
            {"name": "category", "type": "tag"},
        ],
        )
    
    vector_store = RedisVectorStore(config=config, embeddings=embeddings)

    print("请你输入案情描述，我来推荐相关裁量信息。")

    v_result = ""

    while True:
        message = input('user:')

        #根据裁量信息，检索知识库，找出最匹配的内容

        similarDocs = vector_store.similarity_search(message, k=1)
        print("检索结果",similarDocs)

        summary_prompt = "".join([doc.page_content for doc in similarDocs])

        send_message = f"下面的推荐的材料信息({summary_prompt})是否相关，如果不相关，您可以完善案情描述，继续询问"
        print(send_message)
        message2 = input('user:')
        
        #判断用户说的内容，是正向还是负向

        messages = [
            ("system", "你是一名信息研判专家，你可以对用户的表述进行正向或负向的判断。 我之前询问了客户一个问题，现在需要你判断用户给出的是正面还是负面评价，输出结果：正向or负向 即可，其他内容不要输出"),
            ("human", message2),
        ]
        tyresult = tongyi_chat.invoke(messages)
        print("评价结果：" ,tyresult.content)
        
        if tyresult.content == "正向":
            v_result = summary_prompt
            break
        else:
            print("抱歉，未能为您匹配到合适的内容，请您重新输入案情描述")
            continue
    # 根据检索的结果，调用大模型，组装输出结果

    messages = [
        ("system", "请你对用户提供的裁量信息，进行总结，提炼出现场勘验要关注的关键信息，注意，不要臆造和联网，不要提供不靠谱的答案。"),
        ("human", v_result),
    ]
    tyresult = tongyi_chat.invoke(messages)
    prompt_result = tyresult.content
    print(prompt_result)
    return prompt_result

def createpromptinfo(text):
    # 根据勘验关键信息，生成勘验多轮对话提示词
    pass

if __name__ == "__main__":
    tongyi_chat = ChatTongyi(
    model="qwen-max",
    # top_p="...",
    # api_key="...",
    # other params...
        )
    
    main(tongyi_chat)