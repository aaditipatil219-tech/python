# class A:
#     def show(self):
#         print("this is function A")

# class B(A):
#     pass
# ref=B()
# ref.show()



# class BasicPlayer:
#     def __init__(self,username):
#         self.username=username
#     def walk(self):
#         print(f"{self.username} is moving forward.")
        
# class warrior(BasicPlayer):
#  def attack(self):
#   print(f"{self.username} swings a heavy sword")
# class paladin(warrior):
#  def heal(self):
#   print(f"{self.username} uses divine light to heal the party!")
  
# hero=paladin("Ravikishan")
# hero.walk()
# hero.attack()
# hero.heal()


class ImageContent:
    def apply_filter(self):
        print("Applying 'Vintage' filter to the image.")
        
class textContent:
    def check_grammar(self):
        print("Checking grammar for the text.")
        
class SocialMediaPost(ImageContent,textContent):
    def upload(self):
        def 