from company.models import Company, CompanyUser
from ticket.models import Ticket, TicketQueue
from django.contrib.auth.models import User 
# from datetime import datetime
import datetime
import pytz
import random as rd

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
    now = datetime.datetime.now(pytz.UTC)
    print('current time:', now)
    for tq in ticket_queue:
        if (tq.ended_at < now):
            print(tq, 'dont care')
        else: 
            print(tq, 'found valid ticket queue')
            # try to generate ticket for all user of this company    
    return 

def createTicket(company):
    now = datetime.datetime.now(pytz.UTC)
    users_company_list = CompanyUser.objects.all().filter(id=company.pk)
    for uc in users_company_list:
        # print(uc, uc.user, uc.user.id)
        created_tk = Ticket.objects.create(status='actv', user=User.objects.get(pk=uc.user.id), valid_till=now+datetime.timedelta(minutes=company.valid_duration))
        print('created_tk:', created_tk)

def createTicketQueue(company: Company):
    random_mins = rd.randint(0, company.check_every)
    now = datetime.datetime.now(pytz.UTC)
    t = datetime.datetime(now.year, now.month, now.day, company.start_time-7)
    started_at = t + datetime.timedelta(minutes=random_mins)

    created_tq = TicketQueue.objects.create(status='init', started_at=started_at, 
    ended_at=started_at + datetime.timedelta(minutes=company.valid_duration), company=company)
    print('created_tq:', created_tq)

def createTicketQueueWStartedAt(company: Company, started_at):
    created_tq = TicketQueue.objects.create(status='init', started_at=started_at, 
    ended_at=started_at + datetime.timedelta(minutes=company.valid_duration), company=company)
    print('created_tq-WStartedAt:', created_tq)

def findNextTicketQueue(latest_started_at, duration, start_time):
    # time_start = datetime.time(hour=9-7) # -7 unit in UCT
    time_start = start_time - 7
    started_at_hour = latest_started_at.hour
    
    sum_result = time_start
    duration_in_hour = duration//60
    while sum_result <= started_at_hour:
        sum_result += duration_in_hour
    # print(sum_result, '{}:{}:00'.format(sum_result, rd.randint(0, duration)))
    if sum_result >= 24 - duration_in_hour:
        return False
    
    now = datetime.datetime.now(pytz.UTC)
    t = datetime.datetime(now.year, now.month, now.day, sum_result)
    rd_mins = rd.randint(0, duration)
    # print("rd_mins:", rd_mins)
    next_started_at = t + datetime.timedelta(minutes=rd_mins)
    print(next_started_at)
    print('...')
    return next_started_at

def generateTicketQueue():
    companys = Company.objects.all()

    now = datetime.datetime.now(pytz.UTC)
    today = '{}-{}-{}'.format(now.year, now.month, now.day)
    print('(0)', companys)
    for company in companys:

        if company.start_time - 7 < now.hour < company.end_time - 7:
            ticket_queues = TicketQueue.objects.all().filter(
                started_at__gte=now, status='init', company=company.pk)
            print('(1)', ticket_queues)
            
            if len(ticket_queues) > 0:
                if now.hour == ticket_queues[-1].started_at.hour: 
                    createTicket(company)
                    ticket_queues[-1].status = 'done'
                    ticket_queues[-1].save()
            
            elif len(ticket_queues) == 0:
                ticket_queues_done = TicketQueue.objects.all().filter(
                started_at__gte=now, status='done', company=company.pk)
                print('(2)', ticket_queues_done)
                
                if len(ticket_queues_done) == 0:
                    createTicketQueue(company)

                elif len(ticket_queues_done) > 0:
                    tq = ticket_queues_done[-1] # latest one
                    next_started_at = findNextTicketQueue(tq.started_at, company.check_every, company.start_time)
                    createTicketQueueWStartedAt(company, next_started_at)
        else:
            print('now@{} not in the company time f{} t{}'.format(now, company.start_time, company.end_time))

                


# def generateTicketQueue():
#     print('schedule job @{}'.format(datetime.datetime.now()))
#     # check ticketQueue of today

#     # get each company configs
#     companys = Company.objects.all()    

#     #get ticket queue
#     now = datetime.datetime.now(pytz.UTC)
#     # today = datetime.date.today()
#     today = '{}-{}-{}'.format(now.year, now.month, now.day)
#     ticket_queues_today = TicketQueue.objects.all().filter(started_at__gte=now, status='init')
#     print(len(ticket_queues_today), ticket_queues_today)

#     if len(ticket_queues_today) == 0:
#         # create ticket queue
#         for company in companys:
#             startTime = company.start_time
#             rd_minute = rd.randint(0, company.check_every)
#         return


#     for tq in ticket_queues_today:
#         end_at = tq.ended_at
#         company = companys.get(code=tq.company)

#         rd_minute = rd.randint(0, company.check_every)
#         # rd_hour = rd.randint(company.start_time)

#         # users in this company
#         user_company_list = CompanyUser.objects.all().filter(id=company.pk)
#         print(user_company_list)
#         # check if now < end
#         print(now, end_at)
#         if now < tq.ended_at and tq.status == 'init':
#             # create ticket for all user in this company
#             for uc in user_company_list:
#                 # print(uc, uc.user, uc.user.id)
#                 Ticket.objects.create(status='actv', user=User.objects.get(pk=uc.user.id), valid_till=now+datetime.timedelta(minutes=company.valid_duration))
#             tq.status = 'done'
#             tq.save()
#     return