class A:
    def abc(self):
        for i in range(100):
            if i == 0:
                print(5)
        a = self.abc()
        self.abc()
        b = 'password'
        a['1'] = b
        return a

