import os
import socket 

HOST = "127.0.0.1" 
PORT = 5001

def namecheck():
        while True:
            name = input("Customer name: ")
            if name == "":
                print("You didn't enter a name.")
                continue
            if len(name) > 20:
                print("Name too long, retry.")
                continue
            if " " in name:
                print("No spaces allowed in the name.")
                continue
            if not name.isalpha():
                print("Please enter only letters. No numbers or special characters allowed.")
                continue
            break
        return name
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    choice = ""

    while choice != "8":
        print("Python DB menu")
        print("1. Find Customer")
        print("2. Add Customer")
        print("3. Delete Customer")
        print("4. Update Customer age")
        print("5. Update Customer address")
        print("6. Update Customer phone number")
        print("7. Print Report")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")
        
        if(choice == "1"):
            name = namecheck() 
            data = f"{choice},{name}"
            s.send(data.encode())
            response = s.recv(1024).decode()
            print("\nServer Response: " + response + "\n\n")


        elif(choice == "2"):
            name = namecheck()
            age = input("Customer age: ")
            address = input("Customer address: ")
            phone = input("Customer phone number: ")
            data = f"{choice},{name},{age},{address},{phone}"
            s.send(data.encode())
            response = s.recv(1024).decode()
            print("\nServer Response: " + response + "\n\n")
            

        elif(choice == "3"):
            name = namecheck() 
            data = f"{choice},{name}"
            s.send(data.encode())
            response = s.recv(1024).decode()
            print(response)

        elif(choice == "4"):
            name = namecheck()
            age = input("Customer age: ")
            data = f"{choice},{name},{age}"
            s.send(data.encode())
            response = s.recv(1024).decode()
            print(response)

        elif(choice == "5"):
            name = namecheck()
            address = input("Customer address: ")
            data = f"{choice},{name}, ,{address}"
            s.send(data.encode())
            response = s.recv(1024).decode()
            print(response)


        elif(choice == "6"):
            name = namecheck()
            phone = input("Customer phone number: ")
            data = f"{choice},{name}, , ,{phone}"
            s.send(data.encode())
            response = s.recv(1024).decode()
            print(response)
        
        elif(choice == "7"):
            s.send(choice.encode())
            response = s.recv(1024).decode()
            print("++\n++ DB Report\n++")
            print(response)


        elif(choice == "8"):
            s.send(choice.encode())
            print("Bye Bye!")
            

        input("Press Enter to continue...")
        os.system("cls" if os.name == "nt" else "clear")






       

    
      

    
