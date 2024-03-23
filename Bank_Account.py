from datetime import datetime, timedelta
import pytz

class TimeZone:
    def __init__(self, time_zone, offset_hours):
        self.time_zone = time_zone
        self.offset = timedelta(hours=offset_hours)

class BankAccount:
    monthly_interest_rate = 0.5
    
    def __init__(self, account_number, first_name, last_name, timezone, starting_balance=0):
        self.account_number = account_number
        self._first_name = first_name  
        self._last_name = last_name    
        self._balance = starting_balance
        self.transaction_id = 0
        self.timezone = timezone
        
    @property
    def first_name(self):
        return self._first_name
        
    @first_name.setter
    def first_name(self, new_first_name):
        self._first_name = new_first_name
    
    @property
    def last_name(self):
        return self._last_name
        
    @last_name.setter
    def last_name(self, new_last_name):
        self._last_name = new_last_name    
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
     
    @property
    def balance(self):
        return self._balance  
    
    def confirm_number(self, transaction_code):
        self.transaction_id += 1  
        now_utc = datetime.now(pytz.utc)
        timestamp = now_utc.strftime('%Y%m%d%H%M%S%f')[:-3]
        confirmation_number = f"{transaction_code}-{self.account_number}-{timestamp}-{self.transaction_id}"
        return confirmation_number  
    
    def deposit(self, deposit_amount):
        if deposit_amount > 0:
            self._balance += deposit_amount
            confirmation_number = self.confirm_number('D')
            print(f"Your balance after deposit: {self._balance}, Transation ID: {self.transaction_id}" )
            return confirmation_number
        else:
            return self.confirm_number('X')
        
    def withdrawal(self, withdrawal_amount):
        if withdrawal_amount > 0 and self._balance >= withdrawal_amount:
            self._balance -= withdrawal_amount
            confirmation_number = self.confirm_number('W')
            print(f"Your balance after withdrawal: {self._balance}, Transation ID: {self.transaction_id}" )
            return confirmation_number
        else:
            return self.confirm_number('X')
            
    def calculate_interest(self):
        interest_amount = self._balance * (self.monthly_interest_rate / 100)
        self._balance += interest_amount
        confirmation_number = self.confirm_number('I')
        print(f"Your balance after deposit interest: {self._balance}, Transation ID: {self.transaction_id}" )
        return confirmation_number
        
    def transation_details(self, confirmation_code, preferred_timezone):
        parts = confirmation_code.split('-')
        transaction_code, account_number, timestamp, transaction_id = parts
        datetime_utc = datetime.strptime(timestamp, '%Y%m%d%H%M%S%f')
        localized_datetime = datetime_utc.astimezone(pytz.utc) + self.timezone.offset
        localized_datetime = localized_datetime.astimezone(preferred_timezone)
        return {
            "account_number": account_number,
            "transaction_code": transaction_code,
            "transaction_id": int(transaction_id),
            "time": localized_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "time_utc": datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
        }

tz = TimeZone("MST", 0)
account = BankAccount(15700, "Bob", "Smith", timezone=tz)
#account.first_name="Adam"
confirmation_number = account.deposit(50.00)
print("Confirmation number:", confirmation_number)

parsed_confirmation = account.transation_details(confirmation_number, pytz.timezone('Asia/Yerevan'))
print("Parsed confirmation:", parsed_confirmation)

interest_confirmation = account.calculate_interest()
print("Interest confirmation:", interest_confirmation)
