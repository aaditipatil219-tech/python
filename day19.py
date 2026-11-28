class Messenger:
    def send_message(self):
        print('Text message is sent')
    def receive_message(self):
        print('Text message is received')
class InternalMessenger(Messenger):
    pass
class WhatsappMessenger(Messenger):
    def send_message(self):
        print('text,photo,video message is sent')
    def receive_message(self):
        print('text,photo,video message is received')
    def set_dp(self):
        print('profile picture is set')
    def set_status(self):
        print('status is set')
        
Im=InternalMessenger()
Im.send_message()
Im.receive_message()
Wp=WhatsappMessenger()
Wp.send_message()
Wp.receive_message()
Wp.set_dp()
Wp.set_status()