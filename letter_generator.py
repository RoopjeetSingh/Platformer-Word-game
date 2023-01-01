# import letter
import random

letter_lis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
random_letters = random.choices(letter_lis,
                                weights=(
                                    43.31, 10.56, 23.13, 17.25, 56.88, 9.24, 12.59, 15.31, 38.45, 1, 5.61, 27.98, 15.36,
                                    33.92, 36.51, 16.14, 1, 38.64, 29.23, 35.43, 18.51, 5.13, 6.57, 1.48, 9.06, 1.39),
                                k=10)
print(random_letters)
