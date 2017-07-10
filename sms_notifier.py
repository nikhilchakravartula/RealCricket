from twilio.rest import Client


class TwilioNotify:
    def __init__(self):
        self.sid = "AC9b9a8796947ec25dabae719b753b1b21"
        self.token = "f1c48eead2214a60676ea6516d9fddbb"
        self.client = Client(self.sid, self.token)
        self.twilio_number = "+16193892249"

    def sendMessage(self,number, message):
        self.client.messages.create( to = number, from_ = self.twilio_number, body=message)
