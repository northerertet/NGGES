#!/bin/bash

LENGTH=14

# Generate one random character from each required set
one_upper=$(tr -dc 'A-Z' < /dev/urandom | head -c 1)
one_lower=$(tr -dc 'a-z' < /dev/urandom | head -c 1)
one_digit=$(tr -dc '0-9' < /dev/urandom | head -c 1)
one_symbol=$(tr -dc '!@#$%^&*()_+-=[]{}|' < /dev/urandom | head -c 1)

# Generate the rest of the password from a combined pool of all characters
all_chars='A-Za-z0-9!@#$%^&*()_+-=[]{}|'
rest_length=$((LENGTH - 4))
rest_of_pass=$(tr -dc "$all_chars" < /dev/urandom | head -c "$rest_length")

# Combine the guaranteed characters with the rest of the password
combined_pass="${one_upper}${one_lower}${one_digit}${one_symbol}${rest_of_pass}"

# Shuffle the combined password to randomize the character order
shuffled_pass=$(echo "$combined_pass" | grep -o . | shuf | tr -d '\n')

echo "Generated Password: $shuffled_pass"