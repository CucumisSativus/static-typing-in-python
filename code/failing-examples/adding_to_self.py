class Vicious:
    def just_method(self) -> None:
        self.member = 1
    
    def another_method(self) -> None:
        self.member = 's'

v = Vicious()
v.just_method()
v.member + 's'