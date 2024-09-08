import argparse
import urllib.request
import logging
import datetime
import csv


# Logger Setup
def setup_logger():
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log')
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


# downloadData Function
def downloadData(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


# processData Function
def processData(file_content):
    personData = {}
    logger = setup_logger()
    reader = csv.reader(file_content.splitlines())

    for linenum, row in enumerate(reader, start=1):
        if len(row) != 3:
            continue

        id, name, birthday_str = row

        try:
            # Parse the birthday string into a datetime object
            birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y').date()
            personData[id] = (name, birthday)
        except ValueError:
            # Log the error if the date is invalid
            logger.error(f"Error processing line #{linenum} for ID #{id}")

    return personData


# displayPerson Function
def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that id")


# main Function
def main(url):
    try:
        # Download data
        csvData = downloadData(url)

        # Process data
        personData = processData(csvData)

        # User input loop
        while True:
            user_input = input("Enter ID to lookup (or <= 0 to exit): ")
            try:
                user_id = int(user_input)
                if user_id <= 0:
                    break
                displayPerson(str(user_id), personData)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a CSV file from a URL.")
    parser.add_argument("--url", help="URL to the CSV file", type=str, required=True)
    args = parser.parse_args()
    main(args.url)