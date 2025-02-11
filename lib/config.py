SERVICE_ACCOUNT_FILE_PATH: str = "lib/privateKey.json"  # Filepath to private key
SUPER_ADMIN: str = (
    "noreply@nabla.no"  # Email of admin to be impersonated. Used as true from email.
)
ROOT_DOMAIN: str = "nabla.no"  # Domain name of the soc website

# Check config is set and stop script during import
if SERVICE_ACCOUNT_FILE_PATH == "" or SUPER_ADMIN == "":
    print("Error: configs not set.")
    if SERVICE_ACCOUNT_FILE_PATH == "":
        print("\tPlease add a filepath the key to the service account to config.py")
    if SUPER_ADMIN == "":
        print("\tPlease add the email of a superuser to config.py")
    print("\tFor more information, please see README.md")
    print("Exiting script.")
    from sys import exit

    exit()
