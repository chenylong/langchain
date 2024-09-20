import os
from langchain.text_splitter import CharacterTextSplitter
#import json
from credis.getdocinfo import read_docx
from credis.cailiang_doc_chaifen import extract_articles
from credis.getkeyword import getkeywordbytext
#import redis
#from langchain.embeddings import XinferenceEmbeddings
from langchain_community.embeddings import XinferenceEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
import re
def main():

    # 设置 Xinference Embeddings 配置
    server_url = "http://127.0.0.1:9997"  # 本地 Xinference 服务地址
    model_uid_jina = 'jina-embeddings-v2-base-zh'
    #model_uid = "your_model_uid"  # 使用实际的 Falcon-Instruct 模型的 model_uid

    # 初始化 Xinference Embeddings，传递本地服务的 URL 和模型 UID
    embeddings = XinferenceEmbeddings(server_url=server_url, model_uid=model_uid_jina)

    # 连接到 Redis
    url = "redis://:Chen@2024@127.0.0.1:6379/0"
    indexname = "cailiang_hz"

    #获取当前文件目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 指定文件路径
    file_path = current_dir+'/doc/裁量规则.docx'
    # 读取文档内容
    content = read_docx(file_path)
    articles = extract_articles(content)
    content_list = []
    category_list = []
    pattern_zhang = re.compile(r'第[一二三四五六七八九十]+章.*?第[一二三四五六七八九十]+条') 
    docid = 0
    for title, content in articles.items():
        docid = docid + 1
        content = title + "\n"+content + "\n****\n"
        # category = 截取content 第X条的内容

        # match_title = re.search(pattern_zhang, content)
        # if match_title:
        #     category = match_title.group()
        # else:
        #     category = "其他"
        # print(category)

        category = getkeywordbytext(content)
        #判断category是否为空，为空则设置为其他
        if category == "" or category is None:
            category = "其他"
        else:
            category = category.strip()
            category = category.replace("</result>", "")
            category = category.replace("<result>", "")
        print("第"+str(docid)+"个，结果:",category)
        content_list.append(content)
        category_list.append(category)

    embeddings = XinferenceEmbeddings(server_url=server_url, model_uid=model_uid_jina)

    config = RedisConfig(
        index_name=indexname,
        redis_url=url,
        metadata_schema=[
            {"name": "category", "type": "tag"},
        ],
    )

    vector_store = RedisVectorStore(embeddings, config=config)
    metadata = [
    {"category": text } for text in category_list
    ]

    ids = vector_store.add_texts(content_list, metadata)
    print(ids[0:10])


if __name__ == "__main__":
    main()