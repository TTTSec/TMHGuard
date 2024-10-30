import os
import json
import socket

def load_unwanted_ports_file():
    """
    Loads a JSON file containing unwanted ports and their descriptions.
    Returns:
        dict: A dictionary of unwanted ports with port numbers as keys and descriptions as values.
    """
    # Define the path to the unwanted ports JSON file
    port_file_path = os.path.join(os.path.dirname(__file__), "..", "port_scanner_files", "unwanted_ports.json")
    try:
        # Open and load the JSON file if it exists
        with open(port_file_path, 'r') as port_file:
            return json.load(port_file)
    except FileNotFoundError:
        # Error handling if the file is missing
        print("unwanted_ports.json file is not found. Make sure you pull from GitHub and place it into the 'port_scanner_files' folder.")
        return {}
    except json.JSONDecodeError:
        # Error handling for JSON parsing errors
        print("Error reading unwanted_ports.json file. Please check the file format.")
        return {}

def load_secure_port_guideline():
    """
    Loads a text file containing guidelines for secure port usage.
    Returns:
        str: The content of the secure port guideline file.
    """
    # Define the path to the secure port guideline text file
    port_guide_file_path = os.path.join(os.path.dirname(__file__), "..", "port_scanner_files", "secure_port_guideline.txt")

    try:
        # Open and read the text file if it exists
        with open(port_guide_file_path, 'r') as guide_file:
            content = guide_file.read()
            return content
    except FileNotFoundError:
        # Error handling if the file is missing
        print(f"Error: The file '{port_guide_file_path}' was not found.")
    except Exception as e:
        # Catch-all error handling for other potential issues
        print(f"An unexpected error occurred while loading secure port guidelines: {e}")

def port_scan():
    """
    Scans a predefined list of unwanted ports on the localhost to check if they are open.
    Returns:
        dict: A dictionary of open unwanted ports with port numbers as keys and descriptions as values.
    """
    # Set the target IP address for scanning
    host = "127.0.0.1"
    open_ports = {}

    # Load the unwanted ports and secure guidelines from the files
    unwanted_ports = load_unwanted_ports_file()
    guideline_file = load_secure_port_guideline()

    # Loop through each unwanted port to check if it's open
    for port in unwanted_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Set timeout for faster scanning (1 second)
            sock.settimeout(1.0)
            try:
                # Attempt to connect to the specified port on localhost
                result = sock.connect_ex((host, int(port)))
                if result == 0:  # If the port is open, result will be 0
                    open_ports[port] = unwanted_ports[port]
            except (socket.error, ValueError) as e:
                # Error handling for socket-related issues or invalid port numbers
                print(f"Error scanning port {port}: {e}")


    port_report_path = os.path.join(os.path.dirname(__file__), "..", "reports", "open_ports.txt")

    # Writing open ports report
    try:
        # Attempt to open the file in read mode
        with open(port_report_path, 'a') as report:
            for port in open_ports:
                report.write(f"Port {port} is open, {open_ports[port]}\n")
        print(
            "'open_ports.txt' report is done, also, do NOT forget to check out the secure port guideline in port_scanner_files directory\n")
    except FileNotFoundError:
        # Handle case where the file does not exist
        print(f"Error: The file '{port_report_path}' was not found.")

