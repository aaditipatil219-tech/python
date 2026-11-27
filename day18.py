class A:
    def show(self):
        print("this is function A")

class B(A):
    pass
ref=B()
ref.show()