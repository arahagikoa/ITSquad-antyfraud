import random
import string

def generate_plate():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=4))
    return letters + numbers

def generate_unique_plates(count):
    plates = set()
    while len(plates) < count:
        plate = generate_plate()
        plates.add(plate)
    return list(plates)

if __name__ == "__main__":
    num_plates = 766
    plates = generate_unique_plates(num_plates)
    
    with open('car_registration_plates.txt', 'w') as f:
        for plate in plates:
            f.write(plate + '\n')
    
    print(f"{num_plates} unique car registration plates have been generated and saved to 'car_registration_plates.txt'.")
