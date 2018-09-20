from scrapy import cmdline

# 运行爬虫hexun.py  通过调用cmdline.execute,再在main.py设置在Run->Edit Configurations里，就可以实现在编辑器中进行debug scrapy
cmdline.execute("scrapy crawl hexun".split())