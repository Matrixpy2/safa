from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self, student_id=None):
        self.student_id = student_id
        self.accept()
    def disconnect(self, close_code):
        pass
    def receive(self , text_data):
        self.send(text_data)