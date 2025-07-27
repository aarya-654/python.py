MAX = 100  # Maximum size of stack

class Stack:
    def __init__(self):
        self.stack = [None] * MAX
        self.top = -1

    def push(self, value):
        if self.top == MAX - 1:
            print("Stack Overflow")
        else:
            self.top += 1
            self.stack[self.top] = value
            print(f"Pushed {value} into stack")

    def pop(self):
        if self.top == -1:
            print("Stack Underflow")
        else:
            popped = self.stack[self.top]
            self.top -= 1
            print(f"Popped element: {popped}")

    def peek(self):
        if self.top == -1:
            print("Stack is empty")
        else:
            print(f"Top element: {self.stack[self.top]}")

    def display(self):
        if self.top == -1:
            print("Stack is empty")
        else:
            print("Stack elements are:")
            for i in range(self.top, -1, -1):
                print(self.stack[i])

# Driver Code
s = Stack()
s.push(10)
s.push(20)
s.push(30)
s.display()
s.peek()
s.pop()
s.display()

# Print name and roll number
print("\nName: Arundhati Shinde")
print("Roll No: DS-103")
