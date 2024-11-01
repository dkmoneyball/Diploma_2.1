import random
import string

def generate_random_email():
    """Генерирует случайный email для тестов"""
    return f"{''.join(random.choices(string.ascii_letters, k=8))}@example.com"
