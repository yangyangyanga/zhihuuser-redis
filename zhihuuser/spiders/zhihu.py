# -*- coding: utf-8 -*
from scrapy import Spider, Request
from zhihuuser.items import ZhihuuserItem
import json

class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['http://www.zhihu.com/']

    # 起始用户名
    start_user = 'excited-vczh'
    # 用户详情页接口
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    # user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # 关注者列表页接口
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # 粉丝列表页接口
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    '''
    第一个大V用户的详细信息请求还有他的粉丝和关注列表请求
    '''
    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20), callback=self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20), callback=self.parse_followers)

    '''
    获取用户基本信息
    '''
    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuuserItem()
        # print("item.fields: ", item.fields)
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        print(item['url_token'])
        yield item
        # 递归遍历正在爬取的用户的关注和粉丝列表
        yield Request(self.follows_url.format(user=result.get('url_token'), include=self.follows_query, offset=0, limit=20), callback=self.parse_follows)
        yield Request(self.followers_url.format(user=result.get('url_token'), include=self.followers_query, offset=0, limit=20), callback=self.parse_followers)

    '''
    递归获取用户关注列表, 进行翻页功能
    '''
    def parse_follows(self, response):
        results = json.loads(response.text)
        # 遍历循环获取每一个关注者url_token，从而解析用户基本信息
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        # 判断是否有下一页，有的话获取下一页的url
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_url = results.get('paging').get('next')
            yield Request(next_url, callback=self.parse_follows)

    '''
    递归获取用户粉丝列表， 进行翻页功能
    '''
    def parse_followers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_url = results.get('paging').get('next')
            yield Request(next_url, callback=self.parse_followers)