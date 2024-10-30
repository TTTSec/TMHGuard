import os
import json
import re


def linux_hash_pass_detector_extractor():
    """
    Extracts usernames and password hashing algorithms from /etc/shadow based on known prefixes.

    Returns:
        dict: A dictionary mapping usernames to their detected hash algorithms and the actual hash.
    """
    hash_file_path = os.path.join(os.path.dirname(__file__), "..", "weak_password_files", "common_hash_algorithms.json")
    hash_algorithms = {}

    # Load hash algorithms from JSON file
    try:
        if not os.path.exists(hash_file_path):
            print("common_hash_algorithms.json file is not found. Ensure it's in the weak_password_files folder.")
            return {}

        with open(hash_file_path, 'r') as hash_file:
            hash_algorithms = json.load(hash_file)
    except json.JSONDecodeError:
        print("Error reading common_hash_algorithms.json: Invalid JSON format.")
        return {}

    shadow_file = "/etc/shadow"
    users_and_algorithm = {}

    # Read /etc/shadow file to detect hashing algorithms
    try:
        with open(shadow_file, 'r') as file:
            for line in file:
                parts = line.split(':')
                if len(parts) < 2:
                    continue  # Skip malformed lines

                username = parts[0]
                password_hash = parts[1]

                # Detect hash algorithm by prefix
                for prefix, algorithm in hash_algorithms.items():
                    if password_hash.startswith(prefix):
                        users_and_algorithm[username] = {"algorithm": algorithm, "hash": password_hash}
                        break
            return users_and_algorithm

    except FileNotFoundError:
        print("Error: /etc/shadow file not found.")
    except PermissionError:
        print("Error: Permission denied when trying to read /etc/shadow. Run as root or with sudo.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


def hash_strength_reporter(users_and_algorithm):
    """
    Creates a report on the strength of detected password hashes.

    Parameters:
        users_and_algorithm (dict): A dictionary of usernames and their hash algorithms.
    """
    hash_strengths = {}
    hash_file_path = os.path.join(os.path.dirname(__file__), "..", "weak_password_files", "hash_strengths.json")
    weak_pass_hash_report = os.path.join(os.path.dirname(__file__), "..", "reports",
                                         "password_hash_weakness_report.txt")

    # Load hash strengths from JSON file
    try:
        if not os.path.exists(hash_file_path):
            print("hash_strengths.json file is not found. Ensure it's in the weak_password_files folder.")
            return

        with open(hash_file_path, 'r') as hash_file:
            hash_strengths = json.load(hash_file)
    except json.JSONDecodeError:
        print("Error reading hash_strengths.json: Invalid JSON format.")
        return

    # Write the strength report to file
    try:
        os.makedirs(os.path.dirname(weak_pass_hash_report), exist_ok=True)
        with open(weak_pass_hash_report, 'w') as weak_hash:
            for user, data in users_and_algorithm.items():
                algorithm = data['algorithm']
                strength = hash_strengths.get(algorithm, "Unknown or unsupported algorithm")
                weak_hash.write(f"Username: {user} - Hash Algorithm: {algorithm} - Strength: {strength}\n\n")
    except Exception as e:
        print(f"An error occurred while writing the report: {e}")


def check_salted_passwords():
    """
    Checks if passwords in /etc/shadow are salted and writes the results to a report.

    Uses regex to determine if the hash is salted and outputs results to 'salted_or_not.txt'.
    """
    output_file = os.path.join(os.path.dirname(__file__), "..", "reports", "salted_or_not.txt")
    shadow_file = "/etc/shadow"
    # Regular expression to match salted hash patterns in /etc/shadow
    salt_pattern = re.compile(r"^\$[a-zA-Z0-9]+\$[^$]+\$[^$]+$")

    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(shadow_file, 'r') as file, open(output_file, 'w') as output:
            for line in file:
                parts = line.split(':')
                username = parts[0]
                password_hash = parts[1]
                # Check if password hash follows the salted pattern
                if salt_pattern.match(password_hash):
                    status = "Salted"
                else:
                    status = "Not salted"

                # Write the result to the output file
                output.write(f"User: {username} - Password Status: {status}\n")

    except FileNotFoundError:
        print(f"Error: {shadow_file} not found.")
    except PermissionError:
        print("Permission denied. Run the script with elevated privileges.")
    except Exception as e:
        print(f"An error occurred: {e}")


def password_check():
    """
    Runs a full password check process, including hash detection, strength reporting,
    and salting status. Outputs reports for each check.
    """
    users_and_algorithms = linux_hash_pass_detector_extractor()

    if users_and_algorithms:
        hash_strength_reporter(users_and_algorithms)
        print("Check the 'password_hash_weakness_report.txt' for hash strength information.\n")
    else:
        print("No hash algorithms detected or an error occurred.\n")

    check_salted_passwords()
    print("Check the 'salted_or_not.txt' to verify if hashes in your system are salted.\n")
