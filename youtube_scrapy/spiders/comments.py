from googleapiclient.discovery import build


class ExttractrComments():
    
    def __init__(self, video_id, api_key) -> None:
        self.video_id = video_id 
        self.api_key = api_key
        self.all_comments = []

        # build a youtube object using our api key
        self.yt_object = build('youtube', 'v3', developerKey=self.api_key)

        # get all comments and replies
        comments = self.get_comments(self.yt_object, self.video_id, '')
        self.comments = []
    
    def get_all_comments(self):
        return self.all_comments
        
        
    # recursive function to get all replies in a comment thread
    def get_replies(self, comment_id, token):
        replies_response = self.yt_object.comments().list(part = 'snippet', maxResults = 100, parentId = comment_id, pageToken = token).execute()

        for reply in replies_response['items']:
            self.all_comments.append(reply['snippet']['textDisplay'])

        if replies_response.get("nextPageToken"):
            return self.get_replies(comment_id, replies_response['nextPageToken'])
        else:
            return []


    # recursive function to get all comments
    def get_comments(self, youtube, video_id, next_view_token):

        # check for token
        if len(next_view_token.strip()) == 0:
            self.all_comments = []

        if next_view_token == '':
            # get the initial response
            comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 100, videoId = video_id, order = 'relevance').execute()
        else:
            # get the next page response
            comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 100, videoId = video_id, order='relevance', pageToken=next_view_token).execute()
        # loop through all top level comments
        for comment in comment_list['items']:
            # add comment to list
            self.all_comments.append([comment['snippet']['topLevelComment']['snippet']['textDisplay']])
            # get number of replies
            reply_count = comment['snippet']['totalReplyCount']
            all_replies = []
            # if replies greater than 0
            if reply_count > 0:
                # get first 100 replies
                replies_list = youtube.comments().list(part='snippet', maxResults=100, parentId=comment['id']).execute()
                for reply in replies_list['items']:
                    # add reply to list
                    all_replies.append(reply['snippet']['textDisplay'])

                # check for more replies
                while "nextPageToken" in replies_list:
                    token_reply = replies_list['nextPageToken']
                    # get next set of 100 replies
                    replies_list = youtube.comments().list(part = 'snippet', maxResults = 100, parentId = comment['id'], pageToken = token_reply).execute()
                    for reply in replies_list['items']:
                        # add reply to list
                        all_replies.append(reply['snippet']['textDisplay'])

            # add all replies to the comment
            self.all_comments[-1].append(all_replies)

        if "nextPageToken" in comment_list:
            return self.get_comments(youtube, video_id, comment_list['nextPageToken'])
        else:
            return []