class car:
    def __init__(self):
        self.brand='Lamborghini'
        self.colour='yellow'
        self.cost=8.70
    def start_engine(self):
        print(self.brand,'Engine is starting...')
        
    def start_gear(self):
        print(self.brand,'Shifting gear...')
        
    def accelerate(self):
        print(self.brand,'car is accelerating...')
        
c1 = car()
print(c1.brand)
print(c1.colour)
print(c1.cost)
c1.start_engine()
c1.start_gear()
c1.accelerate()
    