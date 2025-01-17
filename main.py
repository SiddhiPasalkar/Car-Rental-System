from customer import Customer
from system_owner import SystemOwner


def system_owner_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username == "admin" and password == "password":
        print("Login successful!")
        return True
    else:
        print("Invalid credentials.")
        return False


def main():
    print("***Welcome to the Car Rental System!***")
    owner = SystemOwner("cars.txt")  
    customer = Customer("cars.txt") 

    while True:
        print("\nMain Menu:")
        print("1. System Owner")
        print("2. Customer")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            if not system_owner_login():  
                continue 

            while True:
                print("\nSystem Owner Menu:")
                print("1. Add a car")
                print("2. Remove car")
                print("3. View all cars")
                print("4. Search cars by make")
                print("5. List rented cars")
                print("6. Update car availability")
                print("7. Logout")
                owner_choice = input("Enter your choice: ").strip()

                if owner_choice == "1":
                    owner.add_car() 
                elif owner_choice == "2":
                    owner.remove_car() 
                elif owner_choice == "3":
                    owner.view_cars() 
                elif owner_choice == "4":
                    car_make = input("Enter car make to search: ").strip()
                    owner.search_cars_by_name(car_make)  
                elif owner_choice == "5":
                    owner.list_rented_cars() 
                elif owner_choice == "6":
                    owner.update_car_availability()  
                elif owner_choice == "7":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "2": 
            while True:
                print("\nCustomer Menu:")
                print("1. View available cars")
                print("2. Rent a car")
                print("3. Return a rented car")
                print("4. Sell car on rent")  
                print("5. Go back")
                customer_choice = input("Enter your choice: ").strip()

                if customer_choice == "1":
                    customer.view_available_cars()  
                elif customer_choice == "2":
                    renter_name = input("Enter your name: ").strip()
                    customer.rent_car(None, renter_name)  
                elif customer_choice == "3":
                    car_id = input("Enter Car ID to return: ").strip()
                    customer.return_car(car_id) 
                elif customer_choice == "4":
                    customer.sell_car_on_rent() 
                    owner.assign_ids_to_sell_cars()
                elif customer_choice == "5":
                    print("Returning to the main menu...")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "3": 
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()