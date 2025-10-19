n = int(input("Enter a number: "))

print("Even numbers are:")
for i in range(1, n + 1):
    if i % 2 == 1:
        print(i)