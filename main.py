from youtube_scrapy.spiders.youtube import YoutubeSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import schedule
import time
import requests
import re


def main():

    def job():
        channel_url = []
        url =[]
        creator_name = ['CodeBeauty', 'JennyslecturesCSIT','CodeWithHarry']
        for name in creator_name:
            channel_url.append('https://www.youtube.com/@{}'.format(name))
        for channel in channel_url: 
            html = requests.get(channel + "/videos").text
            video_id = re.search('(?<={"videoId":").*?(?="})',html).group().split('"')
            url.append('https://www.youtube.com/watch?v={}'.format(video_id[0]))
            
        YoutubeSpider.start_urls = url
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(YoutubeSpider)
        process.start()

    schedule.every().day.at("20:08").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == '__main__':
    main()