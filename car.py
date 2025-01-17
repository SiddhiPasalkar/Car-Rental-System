class Car:
    def __init__(self, car_id, make, model, availability, renter_name=None, return_date=None):

        self.car_id = car_id
        self.make = make
        self.model = model
        self.availability = availability
        self.renter_name = renter_name
        self.return_date = return_date

    def __str__(self):
        return (
            f"ID: {self.car_id}, Make: {self.make}, Model: {self.model}, "
            f"Available: {'Yes' if self.availability else 'No'}, "
            f"Renter: {self.renter_name if self.renter_name else 'N/A'}, "
            f"Return Date: {self.return_date if self.return_date else 'N/A'}"
        )
