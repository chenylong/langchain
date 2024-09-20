from docx import Document
import os
def read_docx(file_path):
    # 创建Document对象
    doc = Document(file_path)
    # 初始化一个空字符串用于存储文本内容
    text = ''
    # 遍历文档中的每个段落
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'  # 将段落文本添加到text变量中，并换行
    return text

if __name__ == '__main__':

    #获取当前文件目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 指定文件路径
    file_path = current_dir+'/doc/裁量规则.docx'

    # 读取文档内容
    content = read_docx(file_path)

    # 输出文档内容
    print(content)