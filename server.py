import socketserver
import socket


class DBserver:
    def age(self,age):
        if age == "":
            return True
        if len(age) == 0:
            return True
        if not age.isdigit():
            return False
        age_number = int(age)
        if age_number < 0 or age_number > 120:
            return False
        return True
    

    def phonenumber(self, phone):
        if phone == "":
            return True
        phone = phone.strip()
        if len(phone) != 8:
            return False
        if phone[3] != "-":
            return False
        
        prefix_phone = phone[0] + phone[1] + phone[2]
            
        if not prefix_phone.isdigit():
            return False
        
        areanumber = int(prefix_phone)
        if (areanumber != 514 and areanumber != 426 and areanumber != 901 and areanumber != 394):
            return False
        i = 4
        while i< 8:

            if not phone[i].isdigit():
                return False
            i += 1
            
        return True

    def loadDatabase(self):
        print("Loading database...")
        database = {}
        try:
            with open("data.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    info = [part.strip() for part in line.split("|")]
                    if len(info) < 4:
                        print("DB read error: Record skipped [missing fields]: " + line.strip())
                        continue
                    raw_key = info[0]
                    if raw_key == "":
                        print("DB read error: Record skipped [null key field]: " + line.strip())
                        continue
                   
                    key = self.normalize_name(raw_key)
                    
                    if key in database:
                        print("DB read error: Record skipped [duplicate key]: " + line.strip())
                        continue
                    age = info[1]
                    address = info[2]
                    phone = info[3]
                    if not self.phonenumber(phone):
                        print("DB read error: Record skipped [invalid phone number]: " + line.strip())
                        continue
                    if not self.age(age):
                        print("DB read error: Record skipped [invalid age]: " + line.strip())
                        continue
                    database[key] = [age, address, phone]
        except FileNotFoundError:
            print("data.txt not found")
        self.db = database
        print("Database loaded successfully.")
        return database

    def normalize_name(self, name: str) -> str:
        if name is None:
            return ""
        return name.strip().capitalize()


db_server = DBserver()
finalDB = db_server.loadDatabase()


class MyTCPHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.db_server = DBserver()
    def handle(self):
        while True:
            data = self.request.recv(1024).decode().split(",")
            choice = data[0]
            name = data[1] if len(data) > 1 else ""
            age = data[2] if len(data) > 2 else ""
            address = data[3] if len(data) > 3 else ""
            phone = data[4] if len(data) > 4 else ""
            
            if choice == "1":
                norm = self.db_server.normalize_name(name)
                if norm in finalDB:
                    record = finalDB[norm]
                    response = f"{norm}|{record[0]}|{record[1]}|{record[2]}"
                else:
                    response = f"{name} not found in database."
                self.request.sendall(response.encode())
            
            elif choice == "2":
                if not self.db_server.age(age):
                    self.request.sendall(b"DB add error: Record contains invalid age: " + age.encode())
                    continue
                if not self.db_server.phonenumber(phone):
                    self.request.sendall(b"DB add error: Record contains invalid phone number: " + phone.encode())
                    continue
                norm = self.db_server.normalize_name(name)
                if norm in finalDB:
                    self.request.sendall(b"DB add error: Record with name " + norm.encode() + b" already exists.")
                    continue
                finalDB[norm] = [age, address, phone]
                response = f"{norm}|{age}|{address}|{phone} added to database."
                self.request.sendall(response.encode())
                print("Record added: " + finalDB[norm].__str__())
            
            elif choice == "3":
                norm = self.db_server.normalize_name(name)
                if finalDB.get(norm) is not None:
                    finalDB.pop(norm)
                    response = f"Server Response: {norm} deleted from database."
                else:
                    response = f"Server Response: {name} not found in database."
                self.request.sendall(response.encode())
            
            elif choice == "4":
                if not self.db_server.age(age):
                    self.request.sendall(b"Server Response: DB update error: attempt to update using invalid age: " + age.encode())
                    continue
                norm = self.db_server.normalize_name(name)
                if norm not in finalDB:
                    self.request.sendall(b"Server Response: DB update error: Record with name " + norm.encode() + b" does not exist.")
                    continue
                finalDB[norm][0] = age  
                response = f"Server Response: {norm} age updated to {age}."
                self.request.sendall(response.encode())
            
            elif choice == "5":
                norm = self.db_server.normalize_name(name)
                if norm not in finalDB:
                    self.request.sendall(b"Server Response: DB update error: Record with name " + norm.encode() + b" does not exist.")
                    continue
                finalDB[norm][1] = address  
                response = f"Server Response: {norm} address updated to {address}."
                self.request.sendall(response.encode())
            elif choice == "6":
                if not self.db_server.phonenumber(phone):
                    self.request.sendall(b"Server Response: DB update error: attempt to update using invalid phone number: " + phone.encode())
                    continue
                norm = self.db_server.normalize_name(name)
                if norm not in finalDB:
                    self.request.sendall(b"Server Response: DB update error: Record with name " + norm.encode() + b" does not exist.")
                    continue
                
                finalDB[norm][2] = phone  
                response = f"Server Response: {norm} phone number updated to {phone}."
                self.request.sendall(response.encode())
            
            elif choice == "7":
                sorted_names = sorted(finalDB.keys())
                report = f"{'Name':<10} {'Age':<3} {'Address':<20} {'Phone':<8}\n"
                report += "-" * 48 + "\n"
                for name in sorted_names:
                    record = finalDB[name]
                    name_str = str(name)[:10]
                    age_str = str(record[0])[:3] if len(record) > 0 else ""
                    addr_str = str(record[1])[:20] if len(record) > 1 else ""
                    phone_str = str(record[2])[:8] if len(record) > 2 else ""
                    report += f"{name_str:<10} {age_str:<3} {addr_str:<20} {phone_str:<8}\n"
                self.request.sendall(report.encode())
            
            elif choice == "8":
               self.request.sendall(b"Server Response: Connection closed.")
               break

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5001
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
        pipi = DBserver()
        pipi.loadDatabase()


            


