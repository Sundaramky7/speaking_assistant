# from SpeakAssistant import tackcommand
import subprocess
import psutil
import os
import colorama

#get all application names
def get_application_names():
    applications_folder = ['/System/Applications','/Applications','/System/Applications/Utilities']
    app_names = []
    
    # Iterate over all items in the /System/Applications/ and Applications directory . 
    for i in applications_folder:
        # print()
        for item in os.listdir(i):
            # Check if the item is a directory and ends with '.app' extension
            if item.endswith('.app') and os.path.isdir(os.path.join(i, item)):
                # Remove the '.app' extension and add to the list of application names
                app_name = item[:-4]  # Remove the '.app' extension
                app_names.append(app_name)




    # result = []
    # search_path='/'
    # filename='WhatsApp'
    # for root, dirs, files in os.walk(search_path):
    #     if filename in files:
    #         full_path = os.path.join(root, filename)
    #         result.append(full_path)

    # return result
    
    return app_names

#check if application exist
# def check_application_availability(app_name):
#     app_path = f"/Applications/{app_name}.app"
#     if os.path.exists(app_path):
#         print(f"The application '{app_name}' is installed.")
#         open_application(app_name)

#     else:
#         print(f"The application '{app_name}' is not installed.")

#open Application 
def open_application(app_name):
    try:
        subprocess.call(["open", "-a", app_name])
    except Exception as e:
        print(f"Error opening application '{app_name}': {str(e)}")



def close_application(app_name):
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        # Check if process name matches app_name
        if proc.info['name'] == app_name:
            print(f"・Closing ",f"{app_name}"+colorama.Fore.MAGENTA,f" (PID: {proc.info['pid']})")
            # Attempt to terminate the process
            try:
                proc.terminate()
            except psutil.NoSuchProcess:
                print(f"・Process"+colorama.Fore.RED+f" {app_name}"+colorama.Fore.RESET+" not found.")
            except psutil.AccessDenied:
                print(f"・Access denied to terminate "+colorama.Fore.YELLOW+"{app_name}"+colorama.Fore.RESET+".")
            else:
                print(colorama.Fore.MAGENTA+"・"+f"{app_name}"+colorama.Fore.RESET+" successfully closed.\n\n")
                return
    
    print(f"{app_name} is not currently running.")


def inisateSearch(query1,query):
        app_names = get_application_names() # gets all app names
        # print(app_names)
        #check for avibiltiy of application
        for app_name in app_names:
            app_Name = app_name.lower()
            if query in app_Name:
                print(colorama.Fore.GREEN+"\nApplications in folder:"+colorama.Fore.RESET)
                print(colorama.Fore.YELLOW+"-----------------------")
                if 'open' in query1.lower():
                    open_application(app_name)
                    # print("fsdsd")
                    print(colorama.Fore.BLUE,"・"+app_Name.capitalize(),colorama.Fore.RESET+"is opened.\n")
                    return
                elif 'close' in query1.lower():
                    # print("fsdsd")
                    close_application(app_name)
                    return
                # print('application is not in folder')
            # print(app_name)
def start(query1):
    if len(query1) > 4:
        # print(query1)
        if 'open' in query1:
            query = query1.split("open ")
            # print(query1," , ",query)
            # return query1 , query
            inisateSearch(query1,query[1])
            return
        elif 'close' in query1:
            query = query1.split("close ")
            # print(query1," , ",query)
            # return query1,query
            inisateSearch(query1,query[1])
            return
        elif 'show app' in query1:
            app_names = get_application_names();
            count=1
            print(colorama.Fore.GREEN+"Apps on your system:")
            print(colorama.Fore.YELLOW+"====================")
            for i in app_names:
                print(colorama.Fore.YELLOW+f"・"+colorama.Fore.RESET+i+colorama.Fore.GREEN+" "+colorama.Fore.RESET)
                count=count+1
            print("\n")
            return

# Test calls removed - these were causing unwanted output on import
# start("open terminal")
# start("close terminal")
# start("show app")
