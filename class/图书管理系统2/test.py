class te:
    a=1;
    b=2;
    def tett(self):
        return 1
    def __str__(self):
        return f"{self.a},{self.b}"
a =te()
a=a.tett()
print(a)
