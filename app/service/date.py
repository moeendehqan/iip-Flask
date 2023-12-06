from persiantools.jdatetime import JalaliDate


class dateProject():

    def datetime_to_jalali_str(self,date):
        return str(JalaliDate.to_jalali(date.year,date.month,date.day))
