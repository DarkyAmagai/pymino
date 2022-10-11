from time import time

class PrepareMessage:
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.message = self.base_message

    @property
    def base_message(self):
        return {
            "type": 0,
            "content": self.content if hasattr(self, "content") else None,
            "clientRefId": int(time() / 10 % 1000000000),
            "timestamp": int(time() * 1000)
            }

    @property
    def sticker_message(self):
        self.message["type"] = 3
        self.message["stickerId"] = self.stickerId
        return self.message
        
    @property
    def image_message(self):
        self.message["mediaType"] = 100
        self.message["mediaUploadValue"] = self.image
        self.message["mediaUploadValueContentType"] = "image/jpg"
        self.message["mediaUhqEnabled"] = True
        return self.message

    @property
    def gif_message(self):
        self.message["mediaType"] = 100
        self.message["mediaUploadValue"] = self.gif
        self.message["mediaUploadValueContentType"] = "image/gif"
        self.message["mediaUhqEnabled"] = True
        return self.message

    @property
    def audio_message(self):
        self.message["type"] = 2
        self.message["mediaType"] = 110
        self.message["mediaUploadValue"] = self.audio
        return self.message
            
    @property
    def reply_message(self):
        self.message["replyMessageId"] = self.replyMessageId
        return self.message
    
    @property
    def embed_message(self):
        self.message["attachedObject"] = self.attachedObject
        return self.message

    @property
    def mention_message(self):
        self.message["extensions"] = {"mentionedArray": self.mentionedArray}
        return self.message

    @property
    def link_snippet_message(self):
        self.message["extensions"] = {"linkSnippetList": [self.linkSnippetList]}
        return self.message
