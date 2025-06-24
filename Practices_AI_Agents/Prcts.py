# class BankAccount:
#     def __init__(self, balance=0 ):
#         self.balance = balance
#     def deposit(self, amount):
#         self.balance += amount
#     def withdraw(self, amount):
#         if amount > self.balance:
#             print("❌ Insufficient funds! Withdrawal denied.")
#         else:
#             self.balance -= amount  
#     def transfer(self , amount, other_account):
#         if amount > self.balance:
#             print("❌ Insufficient funds! Transfer denied.")
#         else:
#             self.balance -= amount
#             other_account.deposit(amount)
#             print(f"✅ Transferred {amount} to the other account.")

                
#     def get_balance(self):
#         if self.balance < 0:
#             print("Insufficient funds")
#             return 0
#         return self.balance 

# class SavingsAccount(BankAccount):
#     def withdraw(self, amount):
#         fee = 10
#         total_amount = amount + fee
#         self.balance -= total_amount
#     def apply_khancha(self , rate):    
#         intrest = self.balance * rate /100
#         self.balance += intrest
#     def warner(self):
#         if self.balance < 100:
#             print("❗ Warning: Your balance is below the minimum required amount of 100.")
#         else:
#             print("✅ Your balance is sufficient.")
              
# # 💳 Test Case
# account = SavingsAccount(1000)
# account.deposit(500)         # Balance = 1500
# account.withdraw(200)        # Deduct 210
# account.apply_khancha(5)     # 5% Interest on current balance
# account.warner()
# print("📘 Final Balance:", account.get_balance())




# def log_decorator(func):
#     def wrapper():
#         print("ye ye start hua bharwa function")
#         func()
#         print("ye ye end hua bharwa function")
#     return wrapper


# @log_decorator
# def bharwa():
#     print("ye ye bharwa function hai")

# bharwa()    



# even_squares = [i**2 for i in range(11) if i % 2 == 0]
# print("Even squares:", even_squares)



# nums = [1, 2, 3, 4, 5, 6]

# my_dict={i: i**2 for i in nums if i % 2 == 0}
# print(my_dict)


# import threading

# def greetings():
#     print("Hello World| From Thread")

# thread1 = threading.Thread(target=greetings)
# thread2 = threading.Thread(target=greetings)
# thread1.start()
# thread2.start()



# from multiprocessing import Process

# def hi_everyone():
#     print("Hello World | From Process")

# p1 = Process(target=hi_everyone)    
# p2 = Process(target=hi_everyone)


# p1.start()
# p2.start()

# def greet(name: str) -> int:
#     print("Hello", name)

# greet("Asharib")

# class A:
#     def __str__(self):
#         return "__str__ called"

# a = A()
# print(a)


# import copy
# original = [[1, 2], [3, 4]]
# clone = copy.deepcopy(original)
# clone[0][0] = 99
# print(original[0][0])



class runner:
