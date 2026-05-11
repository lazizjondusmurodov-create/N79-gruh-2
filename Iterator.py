class Fibonacci:
    def __init__(self, limit):
        self.limit = limit
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.a > self.limit:
            raise StopIteration

        value = self.a
        self.a, self.b = self.b, self.a + self.b

        return value


fib = Fibonacci(20)

for son in fib:
    print(son)