import time
from datetime import datetime

def date2iso(complete_date):
    """
    Method that format a string date in a date with format ISO 8601
    :param complete_date: Date string in format "YYYY-MM-DD HH24:MI:SS"
    :return: Iso date in format  ISO 8601: YYYY-MM-DDThh:mm:ss.sTZD
    """
    strdate = complete_date.strftime("%Y-%m-%dT%H:%M:%S.000")
    minute = (time.localtime().tm_gmtoff / 60) % 60
    hour = ((time.localtime().tm_gmtoff / 60) - minute) / 60
    utcoffset = "%.2d%.2d" %(hour, minute)
    if utcoffset[0] != '-':
        utcoffset = '+' + utcoffset
    return strdate + utcoffset


def returndatetime(datestring):
    """
    Method that return four formats of datetime.
    :param datestring:  Date string in format "YYYY-MM-DD HH24:MI:SS"
    :return: List with four formats of date. "%Y%m%d", "%Y%m%d%H%M%S", "%Y-%m-%d %H:%M:%S" and ISO8601
    """
    if datestring is None:
        date_ymd = datetime.today().strftime("%Y%m%d")
        date_ymdhms = datetime.today().strftime("%Y%m%d%H%M%S")
        date_complete = datetime.strptime(datetime.today().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
        data_iso9061 = date2iso(datetime.today())
        return date_ymd, date_ymdhms, date_complete, data_iso9061
    else:
        try:
            datestring = datetime.strptime(datestring ,'%Y-%m-%d %H:%M:%S')
            date_ymd = datestring.strftime("%Y%m%d")
            date_ymdhms = datestring.strftime("%Y%m%d%H%M%S")
            date_complete = datetime.strptime(datestring.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            data_iso9061 = date2iso(datestring)
            return date_ymd, date_ymdhms, date_complete, data_iso9061
        except Exception as e:
            return None, None, None, None