import scrapy
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_scrapy.spiders.comments import ExttractrComments
from youtube_scrapy.items import YoutubeScrapyItem
class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    start_urls = ['https://www.youtube.com/watch?v=qWdyhFiyH0Y']
    
    
    def parse(self, response):
        data = YoutubeScrapyItem()
        data['URL'] = self.start_urls
        data['Title'] = []
        data['Comments']= []
        data['Reply'] = []
        data['Description'] = []
        data['Start'] = []
        data['Duration'] = []
        data['Text'] = []
        data['Title'] = response.css('title::text').extract_first()
        data['Description'] = response.xpath("//meta[@name='keywords']/@content")[0].extract()
        extract_comments = ExttractrComments(video_id="qWdyhFiyH0Y", api_key='AIzaSyB3dQPOVpQl7EC0LgwFcgYLUGKexNcyEig')   
        all_comments = extract_comments.get_all_comments() 
        for comment, replie in all_comments:
            data['Comments'].append(comment)
            data['Reply'].append(replie if len(replie)>0 else None )
        try:
            transcrip = YouTubeTranscriptApi.get_transcript('qWdyhFiyH0Y')
            for itms in transcrip:
                data['Text'].append(itms['text'])
                data['Start'].append(itms['start'])
                data['Duration'].append(itms['duration'])
        except Exception as e:
            print(e)
            data['Text'] = None
            data['Start'] = None
            data['Duration'] = None
        yield data