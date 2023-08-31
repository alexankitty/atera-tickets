import requests
## Script Vars
apifile = open("apikey")
ticketFilePath = "tickets.txt"
apikey = apifile.read()
## Used to get the technician contact ID
techTicket = 23367

#Globals
headers = {
    "Accept": "application/json",
    "X-API-KEY": apikey}
## API Endpoints
ateraAPIv3 = "https://app.atera.com/api/v3/"
ticketsURL = ateraAPIv3 + "tickets"
contactsURL = ateraAPIv3 + "contacts"

### Functions

### Function
### Parameters: filePath
### Reads tickets from txt file and parses out customer in first word, and ticket title in the rest.
def readTickets(filePath):
    ### todo: write function
    with open(filePath, "r") as f:
        tickets = f.readlines()
    return tickets

def submitTickets(tickets):
    techId = getTechIdFromTicket(techTicket)
    failedTickets = [None] * 0
    for ticket in tickets:
        words = ticket.split(" ")
        itr = 0
        customer = ""
        title = ""
        for word in words:
            if itr == 0:
                customer = word
                itr += 1
            else:
                title = title + word + " "
                itr += 1
        resultFailure = createTicket(customer, title, techId)
        if resultFailure:
            failedTickets.append(ticket)
    return failedTickets

def writeFailedTickets(filePath, tickets):
    with open(filePath, 'w') as f:
        for ticket in tickets:
            f.write(f"{ticket}\n")

### Function
### Parameters: customer name, ticket title, tech id
### Creates and returns a response for the Atera API to create a ticket.
def createTicket(customerName, ticketTitle, techId):
    endUserId = getEndUserId(customerName)
    if not endUserId:
        print(f"{response.status_code}: Failed to create ticket '{ticketTitle}, user {customerName} not found.'")
        return 1
    data = {
        "TicketTitle": ticketTitle,
        "Description": ticketTitle,
        "TicketPriority": "Low",
        "TicketImpact": "NoImpact",
        "TicketStatus": "Open",
        "TicketType": "Incident",
        "EndUserID": endUserId,
        "TechnicianContactID": techId
    }
    response = apiPost(ticketsURL, data)
    if response.status_code != requests.codes.created:
        print(f"{response.status_code}: Failed to create ticket '{ticketTitle}'")
        return 1
    print(f"Created ticket {response.json()['ActionID']} for {ticketTitle}.")
    return 0

### Function
### Parameters: email search query
### Checks the API for a matching user email and selects the first one.
def getEndUserId(search):
    url = contactsURL + f"?itemsInPage=1&searchOptions.email={search}"
    response = apiGet(url)
    items = response.json()['items']
    if len(items):
        return items[0]['EndUserID']
    return 0

### Function
### Parameters: ticket number
### Gets and returns the tech contact ID from a ticket the tech has made.
def getTechIdFromTicket(ticket):
    response = apiGet(ticketsURL + f"/{ticket}")
    return response.json()['TechnicianContactID']

### Function
### Parameters: endpointURL
### Gets the response from an endpoint url
def apiGet(url):
    response = requests.get(url, headers=headers)
    if response.status_code >= 400:
        print(f"{response.status_code}: Request failure to {url}")
    return response

### Function
### Parameters: endpointURL jsonFormattedData
### Posts a json formatted message to an API Endpoint URL
def apiPost(url, data):
    response = requests.post(url, headers=headers, json=data)
    if response.status_code >= 400:
        print(f"{response.status_code}: Request failure to {url}")
    return response


### Main script function
def main():
    tickets = readTickets(ticketFilePath)
    failedTickets = submitTickets(tickets)
    writeFailedTickets(ticketFilePath, failedTickets)

### make it run
main()