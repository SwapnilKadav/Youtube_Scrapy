import scrapy
from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    start_urls = ['https://www.youtube.com/watch?v=qWdyhFiyH0Y']
    
    
    def parse(self, response):
        
        title = response.css('title::text').extract_first()
        description = response.xpath("//meta[@name='keywords']/@content")[0].extract()
        try:
            transcrip = YouTubeTranscriptApi.get_transcript('qWdyhFiyH0Y')
        except Exception as e:
            print(e)
            transcrip = None
        print({'Title':title,'Description':description,'Transcript':transcrip},"++++++++++++++++++++++")
        # yield{}