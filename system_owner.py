import os
from car import Car
from prettytable import PrettyTable


class SystemOwner:
    def __init__(self, file_path="cars.txt"):
        
        self.file_path = file_path
        self.cars = []
        self.load_cars_from_file()


    def load_cars_from_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                pass
        else:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    try:
                        car_id, make, model, availability, renter_name, return_date = line.strip().split(',')
                        availability = availability == "True"
                        renter_name = renter_name if renter_name != "None" else None
                        return_date = return_date if return_date != "None" else None
                        self.cars.append(Car(car_id, make, model, availability, renter_name, return_date))
                    except ValueError:
                        continue 


    def save_cars_to_file(self):
        with open(self.file_path, 'w') as file:
            for car in self.cars:
                line = f"{car.car_id},{car.make},{car.model},{car.availability},{car.renter_name},{car.return_date}\n"
                file.write(line)


    def add_car(self):
        car_id = input("Enter Car ID: ").strip()
        make = input("Enter Car Make: ").strip()
        model = input("Enter Car Model: ").strip()
        availability_input = input("Is the car available? (yes/no): ").strip().lower()
        availability = availability_input == "yes"

        for car in self.cars:
            if car.car_id == car_id:
                print("A car with this ID already exists. Please try again with a different ID.")
                return

        new_car = Car(car_id, make, model, availability)
        self.cars.append(new_car)
        self.save_cars_to_file()
        print(f"Car added successfully: {new_car}")


    def remove_car(self):
        car_id = input("Enter the Car ID to remove: ").strip()
        for car in self.cars:
            if car.car_id == car_id:
                self.cars.remove(car)
                self.save_cars_to_file()
                print(f"Car with ID {car_id} has been removed successfully.")
                return
        print("Car not found. Please check the ID and try again.")


    def update_car_availability(self):
        car_id = input("Enter the Car ID to update availability: ").strip()
        for car in self.cars:
            if car.car_id == car_id:
                availability_input = input("Is the car available? (yes/no): ").strip().lower()
                car.availability = availability_input == "yes"
                car.renter_name = None if car.availability else car.renter_name
                car.return_date = None if car.availability else car.return_date
                self.save_cars_to_file()
                print(f"Car availability updated successfully: {car}")
                return
        print("Car not found. Please check the ID and try again.")


    def list_rented_cars(self):
        rented_cars = [car for car in self.cars if not car.availability]
        if rented_cars:
            table = PrettyTable()
            table.field_names = ["Car ID", "Make", "Model", "Renter Name", "Return Date"]

            for car in rented_cars:
                table.add_row([car.car_id, car.make, car.model, car.renter_name, car.return_date])

            print("Rented cars:")
            print(table)
        else:
            print("No cars are currently rented.")


    def search_cars_by_name(self, car_make):
        car_make = car_make.strip().lower()
        matches = [car for car in self.cars if car.make.lower() == car_make]

        if matches:
            print(f"Cars matching '{car_make}':")
            for car in matches:
                print(f"ID: {car.car_id}, Model: {car.model}, Available: {'Yes' if car.availability else 'No'}")
        else:
            print(f"No cars found with make '{car_make}'.")



    def view_cars(self):
        if not self.cars:
            print("No cars available.")
        else:
            print("\nCars in the system:")
            table = PrettyTable()
            table.field_names = ["Car ID", "Make", "Model", "Availability", "Renter Name", "Return Date"]

            for car in self.cars:
                table.add_row([car.car_id, car.make, car.model, car.availability, car.renter_name, car.return_date])

            print(table)


    def assign_ids_to_sell_cars(self):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()

            updated_lines = []
            current_id = max(
                int(line.split(",")[0]) for line in lines if line.split(",")[0].isdigit()
            ) + 1  # Start with the next available ID

            for line in lines:
                fields = line.strip().split(',')
                if len(fields) == 6:  # Regular car entry
                    updated_lines.append(line.strip())
                elif len(fields) == 5:  # Sell car on rent entry
                    # Assign an ID to sell car on rent
                    updated_line = f"{current_id},{fields[0]},{fields[1]},{fields[2]},{fields[3]},{fields[4]}"
                    updated_lines.append(updated_line)
                    current_id += 1

            # Write the updated lines back to the file
            with open(self.file_path, "w") as file:
                for line in updated_lines:
                    file.write(line + "\n")

            print("Assigned IDs to sell cars and updated the file successfully.")

        except Exception as e:
            print(f"Error assigning IDs to sell cars: {e}")
