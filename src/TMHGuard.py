from colorama import Fore, Style

from port_scanner import port_scan
from password_checker import password_check
from update_detector import check_package_manager_updates, check_cve_main, check_python_package_updates
from permission_check import permission_main

def print_title():

    title = '''
                 ______   __    __     __  __     ______     __  __     ______     ______     _____    
                /\__  _\ /\ "-./  \   /\ \_\ \   /\  ___\   /\ \/\ \   /\  __ \   /\  == \   /\  __-.  
                \/_/\ \/ \ \ \-./\ \  \ \  __ \  \ \ \__ \  \ \ \_\ \  \ \  __ \  \ \  __<   \ \ \/\ \ 
                   \ \_\  \ \_\ \ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \____- 
                    \/_/   \/_/  \/_/   \/_/\/_/   \/_____/   \/_____/   \/_/\/_/   \/_/ /_/   \/____/ 
                                                    By TheMuslimHacker                                                                     
    '''
    print(Fore.MAGENTA + Style.BRIGHT + title + Style.RESET_ALL)


print_title()

#Checking open ports and generating a report
print("\n\nWriting the report on open ports...\n\n")
port_scan()


#Checking Password Strengths and generating a report
print("Writing the report on password strengths...\n\n")
password_check()


#Checking for packeges that need updating
print("Writing the report on packages that need updating...\n\n")
check_package_manager_updates()
check_python_package_updates()

#Checking for knows CVEs of used software on the system
print("Writing the report on CVEs identified...\n\n")
check_cve_main()

#Doing a system report
print("Writing the report on the system...\n\n")
permission_main()

print("All done:)")

