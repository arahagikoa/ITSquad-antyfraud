import random
import string

def generate_policy_number(insurer):
    if insurer == 'PZU':
        prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
        number = ''.join(random.choices(string.digits, k=10))
        return prefix + number
    elif insurer == 'Allianz':
        prefix = 'PL-'
        number = '-'.join([''.join(random.choices(string.digits, k=4)) for _ in range(3)])
        return prefix + number
    elif insurer == 'Warta':
        return ''.join(random.choices(string.digits, k=10))
    else:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def generate_unique_policy_numbers(count, insurer):
    policies = set()
    while len(policies) < count:
        policy_number = generate_policy_number(insurer)
        policies.add(policy_number)
    return list(policies)

if __name__ == "__main__":
    num_policies = 786
    insurer = 'PZU'  # Możesz zmienić na 'Allianz' lub 'Warta'
    policies = generate_unique_policy_numbers(num_policies, insurer)
    
    with open('policy_numbers.txt', 'w') as f:
        for policy in policies:
            f.write(policy + '\n')
    
    print(f"{num_policies} unique policy numbers for {insurer} have been generated and saved to 'policy_numbers.txt'.")
