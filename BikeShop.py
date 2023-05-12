import csv


class BikeShop:
    def __init__(self):
        self.inv_file = 'inventory.csv'
        self.inv_list = [{}]
        self.row = 0
        self.cost = 0
        self.promo = 1
        self.rev_file = 'revenue.txt'
        try:
            self.read_inventory()
        except FileNotFoundError:
            print("Inventory file not found")

    def read_inventory(self):
        with open(self.inv_file, mode='r') as file:
            csv_file = csv.DictReader(file)
            self.inv_list = list(csv_file)  # Convert the reader object to a list
        print("Inventory Initialized")

    def check_inventory(self, r_type, n):
        print("Checking inventory...")
        for item in self.inv_list:
            if item['TYPE'] == r_type:
                self.row = self.inv_list.index(item)
                avl = int(item['AVL'])
                return avl >= n

    def set_promo(self):
        self.promo = 0.7

    def rent_bike(self, n):
        self.cost = int(self.inv_list[self.row]['RATE']) * n * self.promo
        self.update_inventory(n, self.row)
        print(f"Rented {n} bike(s) on {self.inv_list[self.row]['TYPE']} basis.")
        print(f"You will be charged CAD {self.cost} {self.inv_list[self.row]['TYPE']} (*without promo)")
        mul = int(input("How many (days/hours/weeks) would you like to rent for?: "))
        self.cost *= mul
        self.cost *= self.promo
        self.cost = round(self.cost, 2)
        print(f"Total cost for rental (after applying promotions if any) = CAD {self.cost}\n")
        self.update_revenue()
        self.display_avl()

    def update_inventory(self, n, row):
        out = int(self.inv_list[row]['OUT'])
        avl = int(self.inv_list[row]['AVL'])
        avl -= n
        out += n
        self.inv_list[row]['OUT'] = str(out)
        self.inv_list[row]['AVL'] = str(avl)
        try:
            self.update_inv_file()
        except Exception as e:
            print(e)
            print("Error updating Inventory File! Stop and rerun!")

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
            for line in file_obj:
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

    def process_input(self):
        while True:
            try:
                sel = int(input("Enter your choice(1-5): "))
            except ValueError:
                print("Only numbers are to be entered. Retry!")
                continue

            if sel not in range(1, 6):
                print("Entry not in range! Retry")
                continue

            if sel == 1:
                self.display_avl()
            elif sel == 2:
                try:
                    self.rent_options()
                except ValueError:
                    print("Error! Please enter a number only!")
                    continue
            elif sel == 3:
                try:
                    n = int(input("How many bikes would you like to return: "))
                    r_type = input("What type of rental would you like to return? (hourly, daily, weekly)")
                    self.ret_bikes(n, r_type)
                except ValueError:
                    print("Error! Please enter a non-negative or non-zero number of bikes and one of the words "
                          "hourly/daily/weekly for rental type!")
                    continue
            elif sel == 4:
                self.calc_rev()
            else:
                break
            self.print_options()

    def display_avl(self):
        print("Bikes in stock")
        for item in self.inv_list:
            print(f"{item['TYPE'].title()}\t{item['AVL']}")

    @staticmethod
    def get_n(start):
        while True:
            try:
                n = int(input("How many bikes would you like to rent?: "))
                if start == 1 and n < 1:
                    print("Number of bikes should be > 0")
                    continue
                elif start == 3 and n not in range(3, 6):
                    print("With Family rental pick 3-5 bikes only")
                    continue
                return n
            except ValueError:
                print("Please enter only numbers")

    def rent_options(self):
        while True:
            try:
                n = self.get_n(1)
                r_type = input("What type of rental would you like? "
                               "(hourly, daily, weekly, or family): ").lower().strip()

                if r_type not in ('hourly', 'daily', 'weekly', 'family'):
                    print("Invalid entry!")
                    continue

                if 'family' in r_type:
                    if n not in range(3, 6):
                        print("With Family rental pick 3-5 bikes only!")
                        continue
                    self.set_promo()
                    r_type = input("What type of Family-rental would you like? "
                                   "(hourly, daily, weekly): ").lower().strip()

                    if r_type not in ('hourly', 'daily', 'weekly'):
                        print("Invalid entry! Try again")
                        continue

                r_type = self.process_r_type(r_type)

                if self.check_inventory(r_type, n):
                    self.rent_bike(n)
                else:
                    print(f"Sorry, we don't have {n} bikes available in stock for {r_type} rental.\n"
                          f"Try again with a lesser number")
                    continue
                break
            except ValueError:
                print("Error! Please enter a valid choice.")

    @staticmethod
    def process_r_type(r_type):
        if 'hourly' in r_type:
            return 'hourly'
        elif 'daily' in r_type:
            return 'daily'
        else:
            return 'weekly'

    def ret_bikes(self, n, r_type):
        row = 0
        for item in self.inv_list:
            if item['TYPE'] == r_type:
                row = self.inv_list.index(item)
        out = int(self.inv_list[row]['OUT'])
        if n > out:
            print(f"Incorrect entry: Total Borrowed bikes = {out}")
            return
        self.update_inventory(n * -1, row)
        print(f"{n} bike(s) returned!\n")
        self.display_avl()


shop = BikeShop()
shop.print_options()
shop.process_input()
