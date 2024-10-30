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
print(Fore.BLUE + Style.BRIGHT + "\n\nWriting the report on open ports...\n\n" + Style.RESET_ALL)
port_scan()


#Checking Password Strengths and generating a report
print(Fore.BLUE + Style.BRIGHT + "Writing the report on password strengths...\n\n" + Style.RESET_ALL)
password_check()


#Checking for packeges that need updating
print(Fore.BLUE + Style.BRIGHT + "Writing the report on packages that need updating...\n\n" + Style.RESET_ALL)
check_package_manager_updates()
check_python_package_updates()

#Checking for knows CVEs of used software on the system
print(Fore.BLUE + Style.BRIGHT + "Writing the report on CVEs identified...\n\n" + Style.RESET_ALL)
check_cve_main()

#Doing a system report
print(Fore.BLUE + Style.BRIGHT + "Writing the report on the system...\n\n" + Style.RESET_ALL)
permission_main()

print(Fore.GREEN + Style.BRIGHT + "All done:)" + Style.RESET_ALL)

