# atera-tickets
quick and dirty script for mass submitting tickets to the Atera RMM platform with almost 0 effort

# Usage
Grab your API key from https://app.atera.com/new/admin/api and place it in a file called `apikey`  
Fill out a tickets.txt with tickets you want to submit, one ticket per line. Format should be as follows:  
```
companyname/emailstring ticket title and details
```
If the email matches it will create a ticket under that contact, if it does not, it'll warn you in the output.  
Once the script finishes, it will rewrite your tickets.txt with all of the failed ticket submissions.  
