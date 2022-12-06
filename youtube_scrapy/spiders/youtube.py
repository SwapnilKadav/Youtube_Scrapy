import scrapy
from urllib.parse import urlparse
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_scrapy.spiders.comments import ExttractrComments
from youtube_scrapy.items import YoutubeScrapyItem
class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    start_urls = []
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        data = YoutubeScrapyItem()
        url_data = urlparse(response.url)
        video_id = url_data.query[2::]
        print(video_id,"+++++++++++++++++++++++++++++++++++++++")
        data['Comments'] =[]
        data['Transcript'] =[]
        data['URL'] = response.url
        data['Title'] = YouTube(response.url).title
        data['Description'] = YouTube(response.url).description
        extract_comments = ExttractrComments(video_id=video_id, api_key='AIzaSyB3dQPOVpQl7EC0LgwFcgYLUGKexNcyEig')   
        all_comments = extract_comments.get_all_comments() 
        for comment, replie in all_comments:
            data['Comments'].append({'Comments':comment, 'Reply':replie})
        try:
            transcrip = YouTubeTranscriptApi.get_transcript(video_id=video_id)
            for itms in transcrip:
                data['Transcript'].append(itms)
        except Exception as e:
            data['Transcript'] = 'Could not retrieve a transcript for the video {} This is most likely caused by:\n\nSubtitles are disabled for this video\n\nIf you are sure that the described cause is not responsible for this error and that a transcript should be retrievable,'.format(response.url)
        yield data