import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail

from offices.models import Profile, Event, Project, OfficialDays

class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True)
        projects = Project.objects.filter(is_active=True)
        today = datetime.date.today()
        todays_year = datetime.date.today().year
        holidays_list = OfficialDays.objects.filter(year=todays_year)
        weekday = today.weekday()
        event_users_for_today = []
        super_users_emails = []
        if weekday > 4:
            pass
        else:
            for user in users:
                if user.is_superuser:
                    super_users_emails.append(user.email) 
                
            if today in holidays_list:
                pass
            else:
                events = Event.objects.filter(status='accepted') 
                for event in events:
                    date_generated = [event.start_date + datetime.timedelta(days=x) for x in range(0, (event.end_date - event.start_date).days+1)]
                    if today in date_generated:
                        event_users_for_today.append(f'{event.user_fk.first_name} {event.user_fk.last_name}')
                val =  { 
                        'event_users_for_today': event_users_for_today,
                        }
                            
                msg_html = render_to_string('offices/emails/each_day_mail.html',val)
                send_mail(
                                f'Persons who will be absent today',
                                f'''These people will be absent today:
                                Event Start date: 
                                Event Start date: 
                                Event Description: 
                                To login to the app please use the following link ''',
                                'denissham89@gmail.com',
                                super_users_emails,
                                html_message=msg_html,
                                fail_silently=False,
                            )
                return event_users_for_today
    
