class Student:
    def __init__(self,name,adm,dob):
        self.name=name
        self.admnNo=adm
        self.dob=dob

    def display(self):
        print("Name of the student:",self.name)
        print("Name of the student:",self.admnNo)
        print("Name of the student:",self.dob)

Students={}
while True:
    opt=int(input("1.Add Student or 2.Remove Student or 3.Search Student:"))
    if opt==1:
        print("SET STUDENT DETAILS:")
        name=input("Name:")
        adm=input("Admission Number:")
        dob=input("DOB:")

        Students[adm]=Student(name,adm,dob)
        print("Student Added Successfully")

    elif opt==2:
        dlt_adm=input("Enter the Admission number of student to be deleted:")
        std=Students.get(dlt_adm)
        if std:
            del Students[dlt_adm]
            print("Student Deleted Successfully")
        else:
            print('Unable to find student!')

    elif opt==3:
        find_adm=input("Enter the Admission number of student to search:")
        std=Students.get(find_adm)
        if std:
            std.display()
        else:
            print('Unable to find student!')
            
    else:
        print("Inavalid Choice!")

    ch=input("Do you want to continue[y/n]:")
    if ch=='n':
        break