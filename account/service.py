from company.models import Company, CompanyUser
from ticket.models import Ticket, TicketQueue
from datetime import datetime
import pytz

def getTicketQueue(company):
    ticket_queue = TicketQueue.objects.filter(company=company)
    print('ticket_queue', ticket_queue)
    return ticket_queue

def allActiveTicket(user):
    company_user = CompanyUser.objects.get(user=user.id)
    company = Company.objects.get(code=company_user.company)
    ticket_queue = getTicketQueue(company)

    # compare datetime in UTC
    # date variable in the database save in UTC
    # thus ended_at is in UTC
    now = datetime.now(pytz.UTC)
    print('current time:', now)
    for tq in ticket_queue:
        if (tq.ended_at < now):
            print(tq, 'dont care')
        else: 
            print(tq, 'found valid ticket queue')
            # try to generate ticket for all user of this company    
    return 