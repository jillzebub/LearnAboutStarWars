# Imported modules - no need for any special installation
import requests
import random
import string

print("\nWelcome to A New Hope: Learn about Star Wars!")  # Welcome message


# I have learned a little about data cleaning as some characters in this API don't have traditional values
def clean_value(key, value):
    if value.lower() in ["n/a", "unknown", "none"]:  # Only change data with the specified values
        cleaned_data = {
            'gender': 'droid or other creature of unknown gender',
            'height': 'many',  # Not entirely happy with this as it still has 'cm' in the text output
            'birth_year': 'an unknown year',
            'hair_color': 'no',  # Again, may not always be accurate
            'eye_color': 'no'
        }
        return cleaned_data.get(key, value)  # Store the data for later use
    else:
        return value


# Function to be called later
def get_character():
    character_id = input("\nEnter a number from 1-83: ")

    url = 'https://www.swapi.tech/api/people/{}/'.format(character_id)  # Access the API - no key needed
    response = requests.get(url)  # Calls info
    people = response.json()  #

    if 'result' in people:
        result = people['result']

        # The API seems to have changed its structure since I previously used it and now the dictionaries are nested
        name = people['properties'].get('name')  # So I have used .get() to delve into it
        print(f"\nCharacter number {character_id} is called {name}.")

        jedi_name = generate_jediname(name)  # Call the nested function and store the returned value

        more_stats = result.get('properties', {})

        with open("StarWarsCharacters.txt", "a") as jedi:
            jedi.write(f"The chosen character was number {character_id}, {name}.\n"
                       f"This Jedi was assigned the name {jedi_name}\n")  # Write initial info to a file

        return more_stats, jedi_name  # Return both more_stats and jedi_name

    # Error handling
    else:
        print(f"Holy happabore! It looks like character number {character_id} isn't firing on all thrusters!")


# Use string slicing and random module to assign a Jedi nickname to the user
def generate_jediname(name):
    if len(name) >= 10:
        jedi_name = list(name)
        random.shuffle(jedi_name)  # Shuffle the characters into a random order ready for slicing
        jedi_name = ''.join(jedi_name[:6])  # Slice the first 6 characters from the shuffled list
    else:
        additional_chars = 10 - len(name)
        # Import random letters and numbers to build a Jedi nickname
        random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(additional_chars))
        jedi_name = list(name + random_chars)
        random.shuffle(jedi_name)
        jedi_name = ''.join(jedi_name[:6])

    print(f"\nThis character has given you the Jedi nickname: {jedi_name}")  # Print to console
    return jedi_name  # Return the Jedi name


def more_info(more_stats):
    cleaned_stats = {key: clean_value(key, value) for key, value in more_stats.items()}  # Make the output cleaner

    learn_more = input("Would you like to know more? Y/N: ").lower()  # Formatting helps with error handling

    # Error handling
    while learn_more not in ["y", "n"]:
        print(f"\nHold your equinoids! That wasn't expected! Try again, young padawan...\n{learn_more}")
        learn_more = input("Would you like to know more? Y/N: ").lower()

    # Output information about the character
    if learn_more == "y":
        print(f"\nR'iia's shorts! Would you look at all this information:\n"
              f"They are a {cleaned_stats['height']}cm tall {cleaned_stats['gender']} \n"
              f"with {cleaned_stats['hair_color']} hair and {cleaned_stats['eye_color']} eyes, \n"
              f"born in {cleaned_stats['birth_year']}.\n")
        with open("StarWarsCharacters.txt", "a") as jedi:  # Appends the extra detail to the file created earlier
            jedi.write(f"The user chose to find out more.\nTheir stats are:\n")
            for key, value in cleaned_stats.items():  # Iterate over each item in the dictionary
                jedi.write(f"{key}: {value}\n")  # Format so that each stat is on a new line
            jedi.write("\n")

    elif learn_more == "n":
        print(f"\nWell, don't get your processors in a twist, Gorg-face...")
        with open("StarWarsCharacters.txt", "a") as jedi:
            jedi.write("The Jedi was not strong in the Force.\n\n")


# more_stats is a dictionary but if I removed jedi_name it is treated as a tuple... not sure why?
more_stats, jedi_name = get_character()
more_info(more_stats)

new_character = input("Would you like to learn about another character? Y/N: ").lower()

# Error handling
while new_character not in ["y", "n"]:
    print(f"\nDon't futz around! Try again, furball! {new_character}")
    new_character = input("Would you like to learn about a new character? Y/N: ").lower()

# This could go on a while...
while new_character == "y":
    more_stats, jedi_name = get_character()  # Receive both more_stats and jedi_name
    more_info(more_stats)

if new_character == "n":
    print("May the Force be with you!")
