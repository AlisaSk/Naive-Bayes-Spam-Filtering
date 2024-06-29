import os
import re
from email.message import Message
import email
 
class Corpus:
    def __init__(self, path):
        self.path = path
 
    def emails(self):
        for filename in os.listdir(self.path):
            if filename == "!truth.txt":
                continue
            file_path = os.path.join(self.path, filename)
            file_content = self.readfile(file_path)
            yield filename, file_content
          
          
    # this function is used to extract and process words from the body of an email file
    def readfile(self, file_path):
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                msg = email.message_from_file(f)
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                            break
                    else:
                        body = ""
                else:
                    body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')
 
                formatted_content = body.lower()
                words = re.findall("[a-z0-9]+", formatted_content)
 
        # Catching the decoding error
        except Exception as e:
            with open(file_path, mode="rt", encoding="utf-8") as f:
                content = f.read()
                formatted_content = content.lower()
                words =  re.findall("[a-z0-9]+", formatted_content)
 
        return words