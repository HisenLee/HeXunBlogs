# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from scrapy.http import Request
from HeXunBlogs.items import HexunblogsItem

class HexunSpider(scrapy.Spider):
    name = 'hexun'
    allowed_domains = ['hexun.com']
    # 待爬取用户的id
    uid = "lizhiya518"

    # 首次爬取行为  使用scrapy.http.Request
    def start_requests(self):
        # yield类似于return 但返回的是generator
        yield Request("http://" + str(self.uid) + ".blog.hexun.com/p1/default.html",
                      headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"})

    def parse(self, response):
        item = HexunblogsItem()
        item['articleName'] = response.xpath("//span[@class='ArticleTitleText']/a/text()").extract()
        item['articleUrl'] = response.xpath("//span[@class='ArticleTitleText']/a/@href").extract()
        # 因为点击数和评论数是js动态获取的，源码中没有，但经过分析，可以拿到获取点击数/评论数的网页地址
        pattern1 = '<script type=\"text\/javascript\" src=\"http:\/\/click.tool.hexun.com\/linkclick.aspx\?blogid=.*?\"><\/script>'
        tmp_des_address = re.findall(pattern1, str(response.body))[0]
        pattern2 = '.*<script type=\"text\/javascript\" src=\"(.*)\"><\/script>.*'
        desAddr = re.findall(pattern2, tmp_des_address)[0]
        req = urllib.request.Request(desAddr)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0")
        desHtml = urllib.request.urlopen(req, timeout=60).read()
        pattern_click = "click\d*?','(\d*?)'"
        item['articleClicks'] = re.compile(pattern_click).findall(str(desHtml))
        pattern_comment = "comment\d*?','(\d*?)'"
        item['articleComments'] = re.compile(pattern_comment).findall(str(desHtml))
        yield item

        # 获取总页数
        pattern_pagecount = "blog.hexun.com/p(.*?)/"
        pagedata = re.compile(pattern_pagecount).findall(str(response.body))
        if(len(pagedata)>=2):
            totalurl = pagedata[-2]
        else:
            totalurl = 1
        print("一共" + str(totalurl) + "页")
        for index in range(2, int(totalurl)+1):
            nexturl = "http://" + str(self.uid) + ".blog.hexun.com/p"+str(index)+"/default.html"
            yield Request(nexturl,
                      headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"})