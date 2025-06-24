# class Laptop:
#     def __init__(self, gen , Core):
#         self.Core = Core
#         self.gen = gen

#     def input_info(self):
#         name = input("Whats The name of your computer")
#         print(f"Your Laptop Name is {name} and Gen is {self.gen} and icore is {self.Core} ")
    

# lap = Laptop(5 , 5)  
# lap2 = Laptop(2 , 3 )        


# lap.input_info()
# lap2.input_info()


# 2

# class Book:
#     def __init__(self , author , title , pages):
#         self.Author= author
#         self.Title=title
#         self.Pages=pages

#     def summary_printer(self):
#         print(f" Book Is Start :::::::::TITLE:{self.Title} Story:{self.Pages} Okay Thanks You For Reading Best Regards AUTHOR:{self.Author}:::::")    


# author_info = input("Please Enters The Authors Name : ")

# pages_info = input("Please Enters The Pages Content : ")

# Title_info = input("Please Enters The Title : ")
# book1 = Book(Title_info,pages_info,author_info)        
# book1.summary_printer()


# 3 

# class Students:
    
#     def __init__(self , name , rollno , course):
#         self.name =name
#         self.rollno=rollno
#         self.course=course

#     def add_course(self):
#         new_one = input(f"{self.name}, enter the new course name: ")
#         self.course.append(new_one)
 

#     def Show_Course(self):
#         print(self.course)    
    

# name_inp= input("Please Enter Your Name :: ")
# rollno_inp = input("Please Enter Your Roll Number :: ")
# course_inp = input("Please Enter Your courses :: ")

# # Students.add_course()
# # Students.add_course()
# course_list = course_inp.split(",")


# st1 = Students(name_inp,rollno_inp,course_list)
# st2 = Students(name_inp,rollno_inp,course_list)

# st1.add_course()
# st1.add_course()
# st1.Show_Course()
# from abc import ABC, abstractmethod
# class shape:
#     @abstractmethod
#     def area(self):
#         pass
#     def pakistan(self):
#        pass

# class Circle(shape):
#     def __init__(self, radius):
#         self.radius = radius 

#     def area(self):
#         return 3.14 * self.radius * self.radius

# class square(shape):
#     def __init__(self, side):
#         self.side = side

#     def area(self):
#         return self.side * self.side    


# sq = square(4)

# GolAnda= Circle(5)
# print(GolAnda.area())


# class DatabaseConnection:
#     def __init__(self , db_name):
#         self.db_name = db_name
#         print(f"Connected to {self.db_name} database.")
#     def run_query(self , query):
#         print(f"Running query: {query} on {self.db_name} database.")
          
#     def __del__(self):
#         print(f"Disconnected from {self.db_name} database.")      


# db1 = DatabaseConnection("MySQL")
# db1.run_query("SELECT * FROM users")
# del db1

from abc import ABC, abstractmethod

# class Vehicle(ABC):
#     @abstractmethod
#     def move(self):
#         pass

# v = Vehicle()



# class Employee:
   

    
#     def fulltime_employee(self):
#         salary_f = input("Please enter the Full time employee salary")
#         print(f"full time employee salary  is  {salary_f}")    

#     def parttime_employee(self):
#         salary_p = input("Please enter the Part Time employye salary")  
#         print(f"Parttime employe salary is {salary_p}")  





         

