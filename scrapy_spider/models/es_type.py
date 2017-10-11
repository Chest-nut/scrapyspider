# -*- coding:utf-8 -*-

from datetime import datetime

from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'], timeout=20)

class JobboleArticleType(DocType):

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