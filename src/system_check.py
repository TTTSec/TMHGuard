import os
import subprocess


def run_command(command, description, report_path):
    """Run a shell command, print its description, and log its output to the report."""
    print(f"Running: {description}")
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    # Append the output to the report file
    with open(report_path, "a") as report_file:
        report_file.write(f"--- {description} ---\n")
        if result.stdout:
            report_file.write(result.stdout)  # Log stdout to the report file
        if result.stderr:
            report_file.write(f"Error: {result.stderr}\n")  # Log stderr if there's an error
        report_file.write("\n")  # Add a newline for readability


def permission_main():
    # Define the report path and ensure the directory exists
    report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    os.makedirs(report_dir, exist_ok=True)  # Create the reports directory if it doesn’t exist
    report_path = os.path.join(report_dir, "lynis_custom_audit_report.txt")

    # Step 1: File Permissions and Ownership (Each test is isolated)
    run_command("sudo lynis audit system --tests FILE-7524", "Performing File Permissions Check with FILE-7524",
                report_path)
    run_command("sudo lynis audit system --tests FILE-6310", "Checking /tmp, /home, and /var Directory Permissions",
                report_path)

    # Step 2: User and Group Configuration (Isolated tests)
    run_command("sudo lynis audit system --tests AUTH-9204", "Checking users with UID 0", report_path)
    run_command("sudo lynis audit system --tests AUTH-9208", "Checking for non-unique accounts", report_path)
    run_command("sudo lynis audit system --tests AUTH-9212", "Testing group file", report_path)
    run_command("sudo lynis audit system --tests AUTH-9216", "Checking group and shadow group files", report_path)
    run_command("sudo lynis audit system --tests AUTH-9222", "Checking for non-unique groups", report_path)
    run_command("sudo lynis audit system --tests AUTH-9282", "Checking password-protected accounts without expiration",
                report_path)

    # Step 3: Kernel and Hardware Configuration (Isolated tests)
    run_command("sudo lynis audit system --tests KRNL-5622", "Determining Linux default run level", report_path)
    run_command("sudo lynis audit system --tests KRNL-5677", "Checking CPU options and support", report_path)
    run_command("sudo lynis audit system --tests KRNL-5695", "Determining Linux kernel version", report_path)
    run_command("sudo lynis audit system --tests KRNL-5726", "Checking loaded kernel modules", report_path)
    run_command("sudo lynis audit system --tests KRNL-5820", "Checking core dumps configuration", report_path)

    # Step 4: System Hardening and Security Controls (Isolated tests)
    run_command("sudo lynis audit system --tests HRDN-7220", "Checking if compilers are installed", report_path)
    run_command("sudo lynis audit system --tests HRDN-7230", "Checking for malware scanners", report_path)
    run_command("sudo lynis audit system --tests STRG-1846", "Checking if Firewire storage is disabled", report_path)
    run_command("sudo lynis audit system --tests STRG-1904", "Checking NFS RPC", report_path)

    # Step 5: Cryptography and TLS Configuration (Isolated tests)
    run_command("sudo lynis audit system --tests CRYP-7902", "Checking SSL certificate expiration", report_path)
    run_command("sudo lynis audit system --tests CRYP-7930", "Determining if LUKS encryption is used", report_path)
    run_command("sudo lynis audit system --tests CRYP-8002", "Gathering kernel entropy data", report_path)

    # Step 6: System Performance and Resource Usage (Isolated test)
    run_command("sudo lynis audit system --tests PROC-3602", "Checking /proc/meminfo for memory details", report_path)

    # Step 7: Summary and Recommendations (Isolated test)
    run_command("sudo lynis audit system --tests SUMMARY-8100", "Generating Summary and Recommendations", report_path)

    print(f"Audit completed. Check the lynis_custom_audit_report.txt for full information.\n")



