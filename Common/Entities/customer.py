class Customer:
    def __init__(self, id, first_name, last_name, phone, national_code):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.national_code = national_code

    @classmethod
    def create_with_tuple(cls, data):
        customer = cls(data[0], data[1], data[2], data[3], data[4])
        return customer