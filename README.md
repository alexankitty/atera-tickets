# atera-tickets
quick and dirty script for mass submitting tickets to the Atera RMM platform with almost 0 effort

# Setup
Requires Python3.7 or later to be installed, grab it from https://www.python.org/downloads/  
Run `python -m pip install -r requirements.txt` to install the required libraries.
Open createtickets.py and change line 7 techEmail to a ticket number you have submitted previously (used to assign tickets to you)  

# Usage
Grab your API key from https://app.atera.com/new/admin/api and place it in a file called `apikey`  
Fill out a tickets.txt with tickets you want to submit, one ticket per line. Format should be as follows:  
```
companyname/emailstring ticket title and details
```
If the email matches it will create a ticket under that contact, if it does not, it'll warn you in the output.  
Once the script finishes, it will rewrite your tickets.txt with all of the failed ticket submissions.  
For simplicity, a batch and shell script are also included so you can run the script faster.
