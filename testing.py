class First:
    a = "Two"

class Test(First):
    # a = "One"

    def p(self):
        print(self.a)

new = Test()
new.p()