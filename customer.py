import os
from datetime import datetime, timedelta
from prettytable import PrettyTable

class Customer:
    def __init__(self, file_path="cars.txt"):
        self.file_path = file_path


    def view_available_cars(self):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                available_cars = []
                current_id = 1  # Start with ID 1 for numbering cars

                for line in lines:
                    fields = line.strip().split(',')
                    if len(fields) == 6:  # Regular car entry
                        car_id, make, model, availability, renter_name, return_date = fields
                        if availability.lower() == "true":  # Include only available cars
                            available_cars.append((car_id, make, model, return_date))
                    elif len(fields) == 5:  # Sell car on rent entry
                        make, model, availability, _, return_date = fields
                        if availability.lower() == "true":  # Include only available cars
                            available_cars.append((str(current_id), make, model, return_date))
                            current_id += 1  # Increment ID for next car

                # Display the table of all available cars
                if available_cars:
                    print("\nAvailable Cars:")
                    table = PrettyTable()
                    table.field_names = ["Car ID", "Make", "Model", "Return Date"]
                    for car in available_cars:
                        table.add_row(car)
                    print(table)
                else:
                    print("\nNo cars available.")

        except Exception as e:
            print(f"Error viewing available cars: {e}")



    def rent_car(self, _, renter_name):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()

            available_cars = []

            for idx, line in enumerate(lines):
                try:
                    car_id, make, model, availability, renter_name_in_file, return_date = line.strip().split(',')
                    if availability == "True":
                        available_cars.append({
                            'car_id': car_id,
                            'make': make,
                            'model': model,
                            'line_index': idx  
                        })
                except ValueError:
                    continue

            if available_cars:
                print("\nAvailable Cars for Rent:")
                for idx, car in enumerate(available_cars, 1):
                    print(f"{idx}. ID: {car['car_id']}, Make: {car['make']}, Model: {car['model']}")

                while True:
                    try:
                        selected_idx = int(input("Enter the number corresponding to the car you want to rent: ")) - 1
                        if 0 <= selected_idx < len(available_cars):
                            selected_car = available_cars[selected_idx]
                            break
                        else:
                            print("Invalid selection. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")

                print(f"\nYou selected Car ID: {selected_car['car_id']}, Make: {selected_car['make']}, Model: {selected_car['model']}")
                while True:
                    try:
                        duration_days = int(input("Enter the number of days you want to rent the car: "))
                        if duration_days > 0:
                            break
                        else:
                            print("Duration must be greater than 0. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")

                rent_per_day = 100  
                total_rent = rent_per_day * duration_days
                return_date = (datetime.now() + timedelta(days=duration_days)).strftime('%Y-%m-%d')

                print(f"\nTotal rent for {duration_days} days: {total_rent}")
                print(f"Return date: {return_date}")

                line_index = selected_car['line_index']
                lines[line_index] = f"{selected_car['car_id']},{selected_car['make']},{selected_car['model']},False,{renter_name},{return_date}\n"

                with open(self.file_path, "w") as file:
                    file.writelines(lines)

                print(f"\nCar ID {selected_car['car_id']} rented successfully to {renter_name}.")
            else:
                print("\nNo cars available for rent.")

        except Exception as e:
            print(f"Error renting a car: {e}")


    def return_car(self, car_id):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()

            car_found = False
            for idx, line in enumerate(lines):
                try:
                    car_data = line.strip().split(',')
                    if car_data[0] == car_id and car_data[3] == "False":
                        car_found = True
                        car_data[3] = "True"  
                        car_data[4] = "None"  
                        car_data[5] = "None"  
                        lines[idx] = ','.join(car_data) + '\n'
                        print(f"Car ID {car_id} has been returned successfully.")
                        break
                except ValueError:
                    continue

            if car_found:
                with open(self.file_path, "w") as file:
                    file.writelines(lines)
            else:
                print("Car not found or already returned.")
        except Exception as e:
            print(f"Error returning the car: {e}")

    def sell_car_on_rent(self):
        try:
            make = input("Enter Car Make: ").strip()
            model = input("Enter Car Model: ").strip()
            rent_price_per_day = input("Enter rent price per day: ").strip()
            duration_in_months = input("Enter duration in months: ").strip()

            # Calculate return date for the owner
            from datetime import datetime, timedelta
            current_date = datetime.now()
            return_date = current_date + timedelta(days=int(duration_in_months) * 30)
            return_date_str = return_date.strftime("%Y-%m-%d")

            # Add to the file
            with open(self.file_path, "a") as file:
                line = f"{make},{model},True,None,{return_date_str}\n"
                file.write(line)

            print(f"Your Car {make} added for rent. Collect it back by: {return_date_str}.")
        except Exception as e:
            print(f"Error selling car on rent: {e}")
