import json
import sys

class Message:
    def __init__(self, msg_type, content):
        self.header = {
            "byteorder": sys.byteorder,
            "type": msg_type,
            "encoding": 'utf-8',
            "checksum": '',
            "length": len(content)
        }
        self.content = content

    def serialize(self):
        return json.dumps({"header": self.header, "content": self.content}).encode('utf-8')

    @staticmethod
    def deserialize(data):
        message = json.loads(data.decode('utf-8'))
        return Message(message['header']['type'], message['content'])