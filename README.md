
# TMHGuard

**TMHGuard** is a comprehensive security auditing and vulnerability detection tool for Linux systems. It automates the detection of open ports, password security policies, system configurations, and software updates. This tool integrates with **Lynis** to run additional system hardening checks and create reports to assist administrators in maintaining system security.

## Features

- **Port Scanning**: Identifies open ports and compares them against known unwanted or risky ports.
- **Password Security Check**: Extracts and analyzes password hashes to determine if passwords use a secure hashing algorithm and are salted.
- **System Configuration Check**: Uses Lynis to check permissions, user configurations, kernel hardening, cryptographic settings, and compliance standards.
- **Update Detection**: Monitors installed packages and Python libraries for available updates and potential security vulnerabilities.

## Requirements

- **Python 3.6+**
- **Lynis**: Ensure Lynis is installed (`sudo apt install lynis` for Debian-based systems).
- **Required Python Packages**:
  - `requests`
  - `subprocess`
  - `json`
  - `colorama`
          
## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/TMHGuard.git
   cd TMHGuard
   ```

2. Make sure Lynis is installed:
   ```bash
   sudo apt install lynis
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main `TMHGuard.py` file to initiate a comprehensive audit:

```bash
sudo python3 TMHGuard.py
```

**Note**: Root privileges are required to access system files (e.g., `/etc/shadow`) and run Lynis commands effectively.

### Modules and Functionality

Each module in TMHGuard handles a specific aspect of the security audit:

1. **Password Checker** (`password_checker.py`)
   - Scans the `/etc/shadow` file to extract and analyze password hashes.
   - Determines if passwords use a secure hashing algorithm and are salted.
   - Generates a report (`password_hash_weakness_report.txt`) indicating the strength of the detected hashes.
   - Generates a report (`salted_or_not.txt`) indicating whether the hashes are salted or not.

2. **Port Scanner** (`port_scanner.py`)
   - Scans for open ports and checks them against a list of known unwanted or risky ports.
   - Uses `unwanted_ports.json` as a reference for ports that should be monitored.
   - Generates a report (`open_ports.txt`) with a summary of any open risky ports detected.

3. **System Configuration Check** (`system_check.py`)
   - Runs a Lynis system audit to verify configurations, permissions, and system hardening practices.
   - Reports include checks for cryptographic settings,kernel configurations, and etc.

4. **Update Detector** (`update_detector.py`)
   - Checks for system package updates using the APT package manager.
   - Scans for outdated Python packages installed via `pip`.
   - Queries the National Vulnerability Database (NVD) for known vulnerabilities based on software and their version you have installed. NOTE: PLEASE SPECIFI THEM IN THE (`is_there_a_cve.json`) UNDER THE (`software_to_check`) DIRECTORY.

## Reports

TMHGuard generates the following reports within the `reports/` directory:

- **password_hash_weakness_report.txt**: Details the strength of password hashes found in `/etc/shadow`, identifying potential weak hashing algorithms.
- **salted_or_not.txt**: Indicates whether password hashes are salted or not.
- **does_this_need_update.txt**: Summarizes outdated system packages and Python libraries.
- **cve_report.txt**: Lists known vulnerabilities for installed software, pulled from the NVD database.
- **Lynis Report**: Outputs Lynis-generated logs summarizing compliance and security recommendations.

## Lynis Integration

TMHGuard leverages Lynis to run system hardening and compliance checks. Lynis, an open-source security auditing tool, performs in-depth tests for various system security aspects, including:

- **File Permissions and Ownership**: Detects files with world-readable or world-writable permissions.
- **User and Group Configuration**: Verifies proper user access controls and identifies potential privilege escalation risks.
- **Kernel and Hardware Configuration**: Analyzes kernel settings, loaded modules, and hardening features like SELinux.
- **Cryptography and TLS Configuration**: Evaluates SSL/TLS settings for weak protocols and ciphers.

### License

**TMHGuard** is licensed under the MIT License, while **Lynis** is licensed under GPLv3. By including Lynis as an external dependency, this project respects Lynis's licensing requirements.

For more information, refer to the [Lynis GitHub page](https://github.com/CISOfy/lynis) and ensure compliance with its GPLv3 license if modifying or redistributing Lynis within this tool.

## Contributing

Contributions to TMHGuard are welcome. Please fork this repository and submit a pull request.

## Disclaimer

TMHGuard is designed to aid system administrators in securing Linux systems. While it provides valuable insights, it is not a substitute for professional security audits. Always back up important data before making configuration changes.

