import argparse
import logging
import random
import sys
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Breaks relationships between data points to prevent re-identification."
    )

    parser.add_argument(
        "--city",
        type=str,
        required=True,
        help="The city to reassign addresses within.",
    )

    parser.add_argument(
        "--num_records",
        type=int,
        required=True,
        help="The number of records to generate and reassign.",
    )

    parser.add_argument(
        "--output_file",
        type=str,
        required=True,
        help="The file to write the anonymized data to (CSV format).",
    )

    # Example CLI arguments (can be extended based on specific requirements)
    parser.add_argument(
        "--seed",
        type=int,
        default=None,  # Allow Faker to use its own random seed if none provided
        help="Optional seed for Faker's random number generator for reproducibility.",
    )


    return parser

def generate_fake_data(num_records, city, seed=None):
    """
    Generates fake data for the specified city, including names and addresses.

    Args:
        num_records (int): The number of fake data records to generate.
        city (str): The city to generate data for.
        seed (int, optional): Seed for Faker's random number generator. Defaults to None.

    Returns:
        list: A list of tuples, where each tuple contains (name, original_address).
    """
    fake = Faker()

    if seed is not None:
        Faker.seed(seed)  # Seed the Faker instance for reproducible results

    data = []
    for _ in range(num_records):
        name = fake.name()
        address = fake.address()
        # Attempt to ensure the address appears relevant to the specified city
        # Note: Faker might still generate addresses outside the city, but this increases the likelihood.
        if city.lower() not in address.lower(): #add city to address if it's not there
             address = address + ", " + city
        data.append((name, address))
    return data

def reassign_addresses(data):
    """
    Reassigns addresses randomly to the provided data points.

    Args:
        data (list): A list of tuples, where each tuple contains (name, original_address).

    Returns:
        list: A list of tuples, where each tuple contains (name, reassigned_address).
    """
    addresses = [address for _, address in data]
    random.shuffle(addresses)  # Shuffle the addresses in place
    reassigned_data = []
    for i, (name, _) in enumerate(data):
        reassigned_data.append((name, addresses[i]))
    return reassigned_data

def write_data_to_csv(data, output_file):
    """
    Writes the provided data to a CSV file.

    Args:
        data (list): A list of tuples to write to the CSV file.
        output_file (str): The path to the output CSV file.
    """
    try:
        with open(output_file, "w", newline="") as csvfile:
            import csv
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Address"])  # Write header row
            writer.writerows(data)  # Write data rows
        logging.info(f"Data written to {output_file}")
    except Exception as e:
        logging.error(f"Error writing to file {output_file}: {e}")
        raise

def validate_input(args):
    """
    Validates the input arguments.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Raises:
        ValueError: If any of the input arguments are invalid.
    """
    if not isinstance(args.city, str) or not args.city:
        raise ValueError("City must be a non-empty string.")

    if not isinstance(args.num_records, int) or args.num_records <= 0:
        raise ValueError("Number of records must be a positive integer.")

    if not isinstance(args.output_file, str) or not args.output_file:
        raise ValueError("Output file must be a non-empty string.")

    if args.seed is not None and not isinstance(args.seed, int):
        raise ValueError("Seed must be an integer.")


def main():
    """
    Main function to execute the data relationship breaker.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        validate_input(args)
        logging.info("Starting data relationship breaker...")
        logging.info(f"City: {args.city}, Number of Records: {args.num_records}, Output File: {args.output_file}")
        if args.seed is not None:
            logging.info(f"Using seed {args.seed} for Faker's random number generator.")

        # Generate fake data
        data = generate_fake_data(args.num_records, args.city, args.seed)

        # Reassign addresses
        reassigned_data = reassign_addresses(data)

        # Write the reassigned data to a CSV file
        write_data_to_csv(reassigned_data, args.output_file)

        logging.info("Data relationship breaking completed successfully.")

    except ValueError as e:
        logging.error(f"Input validation error: {e}")
        sys.exit(1)  # Exit with an error code
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit with an error code


if __name__ == "__main__":
    main()