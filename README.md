# atera-tickets
quick and dirty script for mass submitting tickets to the Atera RMM platform with almost 0 effort

# Setup
Requires Python3.7 or later to be installed, grab it from https://www.python.org/downloads/
Run `python -m pip install -r requirements.txt` to install the required libraries.
Copy/rename config.example.json to config.json and put in ApiKey and TechEmail.
Using a virtual environment with `python -m venv .venv` is recommended but not required, due to the low quantity of libraries in use.

# Usage
> [!NOTE]
> You may use the legacy `ApiKey` config until 11/10/2026
Grab your API token from https://app.atera.com/new/admin/api and place it in Token in the config.example.json file and rename it to config.json

You will need a new token once a year as that is the current longest expiration period. Be sure to save your token somewhere safe as you will not be able to view it again in Atera.

> [!TIP]
> The following permissions for the token are required:
> Tickets: Read & Write
> Contacts: Read
> Customers: Read

Fill out a tickets.txt with tickets you want to submit, one ticket per line. Format should be as follows:
```
companyname/emailstring ticket title and details
```
If the email matches it will create a ticket under that contact, if it does not, it'll warn you in the output

Once the script finishes, it will rewrite your tickets.txt with all of the failed ticket submissions.

For simplicity, a batch and shell script are also included so you can run the script faster.

