from datetime import datetime
import calendar

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november',
          'december']

def get_month(want_index = False, want_lowercase = True, month = None, need_2digit = False):
    '''return the month. if no parameters, returns lowercase like 'january'

    else if want_index is true, return the index of the month (january is 0)
    else if want_lowercase is False, return month in proper case
    '''
    the_month = get_month_number(month)
    if need_2digit and len(str(the_month)) == 1:
        return "0" + str(the_month)
    if want_index:
        return the_month
    else:
        curr_month = MONTHS[the_month - 1]
        if want_lowercase:
            return curr_month
        else:
            return str.capitalize(curr_month)

def get_month_number(month = None):
    '''return index of current month, or the specified month. January is 1'''
    if month:
        month = str.lower(month)
        return MONTHS.index(month) + 1
    else:
        return datetime.today().month

def get_day_of_month(day = None, need_2digit = False):
    '''return an int containing the day of the month (example April 19 -> 19)'''
    if not day:
        day = datetime.today().day
    if need_2digit and len(str(day)) == 1:
        return "0" + str(day)
    else:
        return day

def get_year():
    '''return current year. kind of want to make this break on purpose,
    figure out if it's still around to get fixed in 2012
    '''
    # return 2011
    return datetime.today().year

def get_day_of_week(want_index=False, want_lowercase=True, month = None,
                    day = None):
    '''return the day of week. if no parameters, returns lowercase like 'monday'

    else if want_index is true, return the index of the (monday is 0)
    else if want_lowercase is False, return day in proper case
    '''
    year = get_year()
    month = get_month(want_index = True, month =  month)
    day_of_month = get_day_of_month(day)
    day_week_index = calendar.weekday(year, month, day_of_month)
    if want_index:
        return day_week_index
    else:
        days = ['monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday']
        curr_day = days[day_week_index]
        if want_lowercase:
            return curr_day
        else:
            return str.capitalize(curr_day)

def get_hour():
    return datetime.today().hour

def get_minute():
    return datetime.today().minute

#print get_month()
#print get_month(want_index=True)
#print get_month(want_lowercase=False)

#print get_day_of_week()
#print get_day_of_week(want_index=True)
#print get_day_of_week(want_lowercase=False, month="january", day=5)
