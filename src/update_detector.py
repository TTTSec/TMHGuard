import json
import subprocess
import os
import requests

# Define paths for output files
output_file = os.path.join(os.path.dirname(__file__), "..", "reports", "does_this_need_update.txt")
cve_report = os.path.join(os.path.dirname(__file__), "..", "reports", "cve_report.txt")


def check_package_manager_updates():
    """
    Checks for available updates via the package manager (APT).
    Parses and writes a list of upgradable packages to the output file.
    """
    try:
        # Run the apt command to list upgradable packages
        result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True, check=True)

        # Parse the output and format it
        packages = parse_package_manager_output(result.stdout)

        # Write the parsed result to the output file with a header
        with open(output_file, "w") as output:
            output.write("=== Package Manager Updates Report ===\n")
            for pkg in packages:
                output.write(
                    f"Package: {pkg['package']}\nCurrent Version: {pkg['current_version']}\nNew Version: {pkg['new_version']}\n\n")
            output.write("=== End of Package Manager Updates Report ===\n\n")
        print("Please check the does_this_need_update.txt report for full info.\n")
    except subprocess.CalledProcessError as e:
        print("Error checking package manager updates:", e)


def parse_package_manager_output(output):
    """
    Parses the output from `apt list --upgradable` to extract package names and versions.

    Args:
        output (str): Raw command output from the package manager.

    Returns:
        list of dict: Parsed information about packages.
    """
    packages = []
    for line in output.splitlines():
        if "upgradable from" in line:
            parts = line.split()
            pkg_name = parts[0].split("/")[0]
            new_version = parts[1]
            current_version = parts[-1] if "from:" in parts else "Unknown"
            packages.append({"package": pkg_name, "current_version": current_version, "new_version": new_version})
    return packages


def check_python_package_updates():
    """
    Checks for outdated Python packages using pip.
    Parses and writes a list of outdated packages to the output file.
    """
    try:
        # Run pip command to list outdated packages in JSON format
        result = subprocess.run(["pip", "list", "--outdated", "--format=json"], capture_output=True, text=True,
                                check=True)

        # Parse JSON output
        packages = json.loads(result.stdout)

        # Write the parsed result to the output file with a header
        with open(output_file, "a") as output:
            output.write("=== Python Package Updates Report ===\n")
            for pkg in packages:
                output.write(
                    f"Package: {pkg['name']}\nCurrent Version: {pkg['version']}\nNew Version: {pkg['latest_version']}\n\n")
            output.write("=== End of Python Package Updates Report ===\n\n")
        print("Please check the does_this_need_update.txt report for full info.\n")
    except subprocess.CalledProcessError as e:
        print("Error checking Python package updates:", e)


def check_cve_updates(software, version):
    """
    Queries the National Vulnerability Database (NVD) API for known vulnerabilities
    related to a specific software and version. Writes vulnerabilities to a report file.

    Args:
        software (str): Name of the software to check for vulnerabilities.
        version (str): Version of the software to check for vulnerabilities.
    """
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "keywordSearch": f"{software} {version}",  # Search by software name and version
        "resultsPerPage": 20  # Limit results per page for API efficiency
    }

    try:
        # Make an HTTP GET request to the NVD API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for non-200 status codes
        try:
            data = response.json()
            # In API v2.0, CVEs are found under 'vulnerabilities'
            outdated_vulns = data.get('vulnerabilities', [])

            # Write each CVE found to the CVE report file
            with open(cve_report, "a") as report:
                for item in outdated_vulns:
                    # Extract CVE ID and description if available
                    cve_id = item.get('cve', {}).get('id', "Unknown CVE ID")
                    description = item.get('cve', {}).get('descriptions', [{}])[0].get('value',
                                                                                       "No description available")
                    report.write(f"CVE: {cve_id}\n")
                    report.write(f"Description: {description}\n\n")

            print(f"{len(outdated_vulns)} vulnerabilities found for {software} {version}.")
        print("Please check the cve_report.txt report for full information.\n")
        except ValueError as e:
            # Handle JSON decoding errors
            print("Error decoding JSON from CVE API:", e, "\n")


    except requests.RequestException as e:
        # Catch all request-related errors (e.g., connection errors)
        print("Failed to retrieve CVE data from NVD API:", e, "\n")



# Main function

def check_cve_main():

    cve_file = os.path.join(os.path.dirname(__file__), "..", "software_to_check", "is_there_a_cve.json")
    with open(cve_file, 'r') as cve:
        software_loaded = json.load(cve)
        for software in software_loaded:
           check_cve_updates(software, software_loaded[software])
    print("\n")
