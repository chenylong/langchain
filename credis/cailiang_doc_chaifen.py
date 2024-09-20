import re
import json

text = """
第二章  餐厨垃圾
第一条 未经市容环境卫生主管部门依法许可从事餐厨垃圾收运、处置的应依据《浙江省餐厨垃圾管理办法》第二十七条“违反本办法第八条和第十三条第四项规定，单位或者个人擅自从事餐厨垃圾收运、处置活动的，由市容环卫行政主管部门责令限期改正；逾期不改正的，处以3000元以上10000元以下罚款；情节严重的，处以10000元以上30000元以下罚款”的规定予以处罚。
违法情节较轻，收运或者处置餐厨垃圾30公斤以下，对个人处3000元以上4000元以下罚款，对单位处5000元以上6000元以下罚款：
违法情节较重，有下列情形之一的，对个人处4000元以上5000元以下罚款，对单位处6000元以上10000元以下罚款：
（一）个人收运或者处置餐厨垃圾30公斤以上；
（二）单位收运或者处置餐厨垃圾50公斤以上。
违法情节严重，有下列情形之一的，处10000元以上30000元以下罚款：
（一）一年内再次发生违法行为；
（二）个人收运或者处置餐厨垃圾100公斤以上；
（三）单位收运或者处置餐厨垃圾100公斤以上。
第二条 餐厨垃圾产生单位自行就地处置餐厨垃圾未报送备案的应依据《浙江省餐厨垃圾管理办法》第三十一条“有下列行为之一的，由市容环卫行政主管部门责令限期改正；逾期不改正的，按以下规定处罚：违反本办法第九条第三款的规定，餐厨垃圾产生单位自行就地处置餐厨垃圾未报送备案的，处以1000元以上5000元以下罚款。”的规定予以处罚。
违法情节较轻，有下列情形之一的，处1000元以上2000元以下罚款：
（一）经营场所面积50平方米以下的；
（二）就地处置的餐厨垃圾量20公斤以下的。
违法情节较重，有下列情形之一的，处2000元以上3000元以下罚款：
（一）经营场所面积50-100平方米；
（二）就地处置的餐厨垃圾量20公斤以上50公斤以下的。
违法情节严重，有下列情形之一的，处3000元以上5000元以下罚款：
（一）经营场所面积100平方米以上；
（二）就地处置的餐厨垃圾量50公斤以上的；
（三）造成环境严重污染的；
（四）严重社会影响的其他情形的。
第三条 餐厨垃圾产生单位不执行餐厨垃圾交付收运确认制度或者未建立相应的记录台账的应依据《浙江省餐厨垃圾管理办法》第三十一条第二项“有下列行为之一的，由市容环卫行政主管部门责令限期改正；逾期不改正的，按以下规定处罚：（二）违反本办法第十一条第一款的规定，餐厨垃圾产生单位不执行餐厨垃圾交付收运确认制度或者未建立相应的记录台账的，处以1000元以上5000元以下罚款”的规定予以处罚。
第三章  测试
第一条 我始化一个测试数据，未经市容环境
"""
# 假设章节的标题和条目的正则表达式
chapter_pattern = re.compile(r'第[一二三四五六七八九十]+章')  # 匹配章节
article_pattern = re.compile(r'第[一二三四五六七八九十]+条')  # 匹配条目

def extract_articles_1(text):
    articles = {}
    current_chapter = None
    current_article = None
    current_content = []

    lines = text.splitlines()  # 按行拆分文本
    for line in lines:
        # 先检测章节
        chapter_match = chapter_pattern.match(line)
        if chapter_match:
            # 保存上一个条目
            if current_article:
                articles[f'{current_chapter} {current_article}'] = '\n'.join(current_content)
            # 更新当前章节
            current_chapter = chapter_match.group(0)
            current_article = None
            current_content = []
            continue
        
        # 检测条目
        article_match = article_pattern.match(line)
        if article_match:
            # 如果发现新条目，保存上一个条目的内容
            if current_article:
                articles[f'{current_chapter} {current_article}'] = '\n'.join(current_content)
            # 更新当前条目
            current_article = article_match.group(0)
            current_content = []
            continue
        
        # 如果没有匹配到章节或条目，当前行是条目的内容，继续累加
        if current_chapter and current_article:
            current_content.append(line)
    
    # 保存最后一个条目
    if current_article:
        articles[f'{current_chapter} {current_article}'] = '\n'.join(current_content)
    
    return articles
def getkanyaninfobytext(text):

    # 定义正则表达式匹配章名、条目和内容
    chapter_pattern = re.compile(r'(第[一二三四五六七八九十]+章)\s+(\S+)')
    article_pattern = re.compile(r'(第[一二三四五六七八九十]+条)\s+(.+)')

    # chapter_pattern = re.compile(r'第[一二三四五六七八九十]+章')  # 匹配章节
    # article_pattern = re.compile(r'第[一二三四五六七八九十]+条')  # 匹配条目

    # 用于存储最终的JSON
    result = {}
    chapter_id = 1
    current_chapter = None
    current_article = None
    article_content = []
    # 遍历每行文本
    for line in text.splitlines():
        # 匹配章
        chapter_match = chapter_pattern.match(line)
        if chapter_match:
            current_chapter = {
                "章序号": chapter_match.group(1),
                "章名": chapter_match.group(2)
            }
            result[chapter_id] = current_chapter
            chapter_id += 1
            continue

        # 匹配条目
        article_match = article_pattern.match(line)
        if article_match :
            # 匹配到之后，保存上一个内容
            if current_article:
                current_chapter[current_article] = '\n'.join(article_content)
            current_article = article_match.group(0)
            article_content = []
            continue

        if not article_match and not current_chapter:
            article_content.append(line)

    if current_article:
        current_chapter[current_article] = '\n'.join(article_content)

    # 输出JSON格式
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return json_result

def json2difykg(json_data):
    # 解析JSON并生成标题和内容
    for chapter_id, chapter_content in json_data.items():
        chapter_number = chapter_content.get("章序号")
        chapter_name = chapter_content.get("章名")

        for key, value in chapter_content.items():
            if "条" in key:  # 过滤出条目的内容
                title = f"{chapter_number} {chapter_name} {key}"  # 标题
                content = value  # 内容

                # 打印生成的标题和内容
                print(f"标题: {title}")
                print(f"内容: {content}")
                print("-" * 50)  # 分割线

def extract_articles(text):
    articles = {}
    current_chapter = None
    current_article = None
    current_content = []
    chapter_pattern = re.compile(r'第[一二三四五六七八九十]+章')  # 匹配章节
    article_pattern = re.compile(r'第[一二三四五六七八九十]+条')  # 匹配条目

    lines = text.splitlines()  # 按行拆分文本
    for line in lines:
        # 先检测章节
        chapter_match = chapter_pattern.match(line)
        if chapter_match:
            # 保存上一个条目
            if current_article:
                articles[f'{current_chapter} {current_article}'] = '\n'.join(current_content)
            # 更新当前章节
            current_chapter = line
            current_article = None
            current_content = []
            continue
        
        # 检测条目
        article_match = article_pattern.match(line)
        
        if article_match:
    
            # 如果发现新条目，保存上一个条目的内容
            if current_article:
                articles[f'{current_chapter} {current_article}'] = '\n'.join(current_content)
            # 更新当前条目
            current_article = line
            current_content = []
            continue
        
        # 如果没有匹配到章节或条目，当前行是条目的内容，继续累加
        if current_chapter and current_article:
            current_content.append(line)
    
    # 保存最后一个条目
    if current_article:
        articles[f'{current_chapter} {current_article}'] = '\n'.join(current_content)
    
    return articles

if __name__ == '__main__':
    json_result = getkanyaninfobytext(text)
    print(json_result)
    print("-------------------")
    print(type(json_result))
    print("-------------------")
    json_result = json.loads(json_result)
    json2difykg(json_result)