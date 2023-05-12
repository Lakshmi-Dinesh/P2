import csv


class BikeShop:
    def __init__(self):
        self.inv_file = 'inventory.csv'
        self.inv_list = []
        self.row = 0
        self.cost = 0
        self.promo = 1
        self.rev_file = 'revenue.txt'
        try:
            self.read_inventory()
        except FileNotFoundError:
            print("Inventory file not found")
        except Exception as e:
            print(e)

    def read_inventory(self):
        with open(self.inv_file, mode='r') as file:
            csv_file = csv.DictReader(file)
            for lines in csv_file:
                self.inv_list.append(lines)
        print("Inventory Initialized")

    def check_inventory(self, r_type, n):
        print("Checking inventory...")
        for item in self.inv_list:
            if item['TYPE'] == r_type:
                self.row = self.inv_list.index(item)
                avl = int(item['AVL'])
                return True if avl >= n else False

    def set_promo(self):
        self.promo = 0.3

    def rent_bike(self, n):
        self.cost = int(self.inv_list[self.row]['RATE']) * n * self.promo
        self.update_inventory(n)
        self.update_revenue()
        print(f"Rented {n} bike(s) on {self.inv_list[self.row]['TYPE']} basis.")
        print(f"You will be charged CAD {self.cost}")

    def update_inventory(self, n):
        out = int(self.inv_list[self.row]['OUT'])
        avl = int(self.inv_list[self.row]['AVL'])
        avl -= n
        out += n
        self.inv_list[self.row]['OUT'] = str(out)
        self.inv_list[self.row]['AVL'] = str(avl)
        try:
            self.update_inv_file()
        except Exception as e:
            print(e)
            print("Error updating Inventory File!Stop and rerun!")

    def update_inv_file(self):
        header = ['TYPE', 'TOTAL', 'OUT', 'AVL', 'RATE']
        with open(self.inv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            writer.writerows(self.inv_list)
        print("Inventory updated")

    def update_revenue(self):
        with open(self.rev_file, 'a+') as file_obj:
            file_obj.write(str(self.cost) + '\n')
        print("Revenue updated")

    def calc_rev(self):
        tot = 0
        with open(self.rev_file, 'r') as file_obj:
            for line in file_obj.readlines():
                tot += float(line.strip())
        print(f"Total store revenue = {round(tot, 2)}CAD")

    def print_options(self):
        self.promo = 1
        print("""
        Bike Rental Shop
            1. Display available bikes
            2. Rent a bike
            3. Return bikes
            4. Display shop revenue
            5. Exit
        """)
        self.process_input()

    def process_input(self):
        try:
            sel = int(input("Enter your choice(1-5): "))
        except TypeError:
            print("Only numbers are to be entered. Retry!")
            self.print_options()
        except Exception as e:
            print(e)
            print("Incorrect entry! Try again!")
            self.print_options()

        if sel not in range(1, 6):
            print("Entry not in range! Retry")
            self.print_options()
        if sel == 1:
            self.display_avl()
        elif sel == 2:
            try:
                self.rent_options()
            except Exception as e:
                print(e)
                print("Error!Please enter a number only!")
                self.rent_options()
        elif sel == 3:
            try:
                n = int(input("How many bikes would you like to return: "))
                self.ret_bikes(n)
            except Exception as e:
                print(e)
                print("Error! Please enter a non negative or non zero number only!")
                self.print_options()
        elif sel == 4:
            self.calc_rev()
        else:
            return
        self.print_options()

    def display_avl(self):
        print("Bikes in stock")
        for item in self.inv_list:
            print(f"{item['TYPE'].title()}\t{item['AVL']}")

    def get_n(self, start):
        try:
            n = int(input("How many bikes would you like to rent?: "))
            if start == 1 and n < 1:
                print("Number of bikes should be > 0")
                n = self.get_n(1)
            elif start == 3 and n not in range(3, 6):
                print("With Family rental pick 3-5 bikes only")
                n = self.get_n(3)
            return n
        except TypeError:
            print("Please enter only numbers")
            self.get_n(start)
        except Exception as e:
            print(e)
            print("Error! You need to enter a number only!")
            self.get_n(start)

    def rent_options(self):
        n = self.get_n(1)
        r_type = input("What type of rental would you like? "
                       "(hourly, daily, weekly, or family): ").lower().strip()
        if 'family' in r_type:
            if n not in range(3, 6):
                print("With Family rental pick 3-5 bikes only!")
                n = self.get_n(3)
            self.set_promo()
            r_type = input("What type of Family-rental would you like? "
                           "(hourly, daily, weekly): ").lower().strip()
        r_type = self.process_r_type(r_type)
        if self.check_inventory(r_type, n):
            self.rent_bike(n)
        else:
            print(f"Sorry, we don't have {n} bikes available in stock for {r_type} rental.\n"
                  f"Try again with a lesser number")
            self.rent_options()

    @staticmethod
    def process_r_type(r_type):
        if 'hourly' in r_type:
            return 'hourly'
        elif 'daily' in r_type:
            return 'daily'
        else:
            return 'weekly'

    def ret_bikes(self, n):
        out = int(self.inv_list[self.row]['OUT'])
        if n > out:
            n = int(input(f"Incorrect entry: Total Borrowed bikes = {out}\n"
                          "Please check and re-enter number of bikes to return: "))
            self.ret_bikes(n)
        self.update_inventory(n * -1)
        print(f"{n} bikes returned! Inventory updated!\n")
        self.display_avl()


shop = BikeShop()
shop.print_options()
