from enum import Enum
import json
import sys

class Message:
    class MessageType(str, Enum):
        ANSWER = "ANSWER"
        QUESTION = "QUESTION"
        RESULT = "RESULT"
        QUIT = "QUIT"
        ERROR = "ERROR"
        NONE = "NONE"
        HELP = "HELP"
        STATUS = "STATUS"
        NAME = "NAME"
        ACKNOWLEDGMENT = "ACKNOWLEDGMENT"

    def __init__(self, msg_type, content, expected_response=MessageType.NONE):
        self.header = {
            "byteorder": sys.byteorder,
            "type": msg_type,
            "encoding": 'utf-8',
            "checksum": '',
            "length": len(content),
            "expected_response": expected_response,
        }
        self.content = content

    def serialize(self):
        return json.dumps({"header": self.header, "content": self.content}).encode('utf-8')

    @staticmethod
    def deserialize(data):
        message = json.loads(data.decode('utf-8'))
        return Message(message['header']['type'], message['content'], message['header']['expected_response'])