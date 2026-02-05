import requests
from joblib import Parallel, delayed
## Script Vars
apifile = open("apikey")
ticketFilePath = "tickets.txt"
apikey = apifile.read()
## Used to get the technician ID
techEmail = "alexandra@techsupportevolved.com"
jobs = 5

#Globals
headers = {
    "Accept": "application/json",
    "X-API-KEY": apikey}
## API Endpoints
ateraAPIv3 = "https://app.atera.com/api/v3/"
ticketsURL = ateraAPIv3 + "tickets"
contactsURL = ateraAPIv3 + "contacts"

### Functions
def readTickets(filePath: str) -> list:
    with open(filePath, "r") as f:
        tickets = f.readlines()
    return tickets

def submitTickets(tickets: list) -> list:
    failedTickets = []
    results = Parallel(n_jobs=jobs)(delayed(postTicket)(ticket) for ticket in tickets)
    for ticket, resultFailure in zip(tickets, results):
        if resultFailure:
            failedTickets.append(ticket)
    return failedTickets

def writeFailedTickets(filePath: str, tickets: list):
    with open(filePath, 'w') as f:
        for ticket in tickets:
            f.write(f"{ticket}\n")

def createTicket(customerName: str, ticketTitle: str) -> int:
    endUser = getEndUser(customerName)
    if not endUser:
        print(f"Failed to create ticket '{ticketTitle}', user {customerName} not found.")
        return 1
    endUserId = endUser['EndUserID']
    endUserCompany = endUser['CustomerName']

    data = {
        "TicketTitle": ticketTitle,
        "Description": ticketTitle,
        "EndUserID": endUserId,
        "TechnicianEmail": techEmail
    }
    response = apiPost(ticketsURL, data)
    if response.status_code != requests.codes.created:
        print(response)
        print(f"{response.status_code}: Failed to create ticket '{ticketTitle}.'")
        return 1
    print(f"Created ticket {response.json()['ActionID']} for {ticketTitle} ({endUserCompany}).")
    return 0

def getEndUser(search: str) -> dict:
    url = contactsURL + f"?itemsInPage=1&searchOptions.email={search}"
    response = apiGet(url)
    items = response.json()['items']
    if len(items):
        return items[0]
    return 0

def apiGet(url: str) -> requests.Response:
    response = requests.get(url, headers=headers)
    if response.status_code >= 400:
        print(f"{response.status_code}: Request failure to {url}")
    return response

def apiPost(url: str, data: dict)-> requests.Response:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code >= 400:
        print(f"{response.status_code}: Request failure to {url}. {response.content}")
    return response

def parseTicket(ticket: str) -> tuple:
    words = ticket.split(" ")
    itr = 0
    customer = ""
    title = ""
    for word in words:
        word = word.splitlines()[0] #drop new line
        if itr == 0:
            customer = word
            itr += 1
        elif itr == 1:
            title = word
            itr += 1
        else:
            title = title + " " + word
            itr += 1
    return (customer, title)

def postTicket(ticket: str) -> int:
    customer, title = parseTicket(ticket)
    resultFailure = createTicket(customer, title)
    if resultFailure:
        return ticket
    return 0


### Main script function
if __name__ == "__main__":
    tickets = readTickets(ticketFilePath)
    failedTickets = submitTickets(tickets)
    writeFailedTickets(ticketFilePath, failedTickets)
