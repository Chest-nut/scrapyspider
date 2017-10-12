# -*- coding:utf-8 -*-

from datetime import datetime

from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer


connections.create_connection(hosts=['localhost'], timeout=20)
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowcase'])

class JobboleArticleType(DocType):

    # 由于elasticsearch-dsl源码的bug，无法直接为suggest设置mapping
    # suggest = Completion(analyzer='ik_max_word')
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_id = Keyword()
    front_img_url = Keyword()
    front_img_path = Keyword()
    bookmark_nums = Integer()
    comment_nums = Integer()
    like_nums = Integer()

    class Meta():
        index = 'jobbole'
        doc_type = 'article'

if __name__ == '__main__':
    JobboleArticleType.init()