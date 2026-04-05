from datetime import date
import os

# ==========================================
# Config
# ==========================================

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.yaml")

# ==========================================
# Global Variables 
# ==========================================

all_clients : list["Client"] = []
all_jobs : list["Job"] = []
all_invoices : list["Invoice"] = []

# ==========================================
# For Classes
# ==========================================

# Class: Client
class Client:
    def __init__(self, client_id : str, name : str, phone : str, address : str):
        self.client_id: str = client_id #client id [Cxxx where xxx is 5-digit number]
        self.name : str = name
        self.phone : str = phone
        self.address : str = address

    @staticmethod
    def find_client(cid: str) -> "Client | None":
        '''Find client object by client id'''
        return next((c for c in all_clients if c.client_id.upper() == cid.upper()), None)

    @staticmethod
    def generate_client_id():
        '''generate new client id [Cxxx where xxx is 5-digit number]'''
        num = 0
        for c in all_clients:
            num = max(num, int(c.client_id[-5:])) # remove 'C' and convert to int
        return f"C{num + 1:05d}"

# Class: Invoice
class Invoice:
    
    def __init__(self, invoice_id : str, amount : float, job_id : str, issue_date=None, payment_date=None, notes=""):
        self.invoice_id : str = invoice_id #invoice id [INV-yyyy-xxxxx where yyyy is year and xxxxx is 5-digit number]
        self.amount : float = amount
        self.job_id : str = job_id
        self.issue_date : date = issue_date if issue_date else date.today()
        self.payment_date : date = payment_date
        self.is_paid : bool = payment_date is not None
        self.notes : str = notes

    @staticmethod
    def find_invoice(inv_id: str) -> "Invoice | None":  
        '''return invoice object by invoice id'''
        return next((i for i in all_invoices if i.invoice_id.upper() == inv_id.upper()), None)

    @staticmethod
    def generate_invoice_id() -> str: 
        '''generate new invoice id'''
        current_year = date.today().year
        num = 0
        for inv in all_invoices:
            num = max(num, int(inv.invoice_id[-5:])) # take last 5 characters and convert to int
        return f"INV-{current_year}-{num + 1:05d}"
    
    @property
    def job(self) -> "Job | None":
        '''return the job object associated with this invoice'''
        return Job.find_job(self.job_id)

    @property
    def client(self) -> "Client | None":
        '''return the client object associated with this invoice'''
        job = Job.find_job(self.job_id)
        return Client.find_client(job.client_id) if job else None

    @property
    def status_label(self) -> str:
        '''for display the status of payment'''
        if self.is_paid:
            return f"PAID on {self.payment_date}"
        return "UNPAID"

    def mark_as_paid(self, payment_date=None):
        '''mark the invoice is paid and set the payment date'''
        self.is_paid      = True
        self.payment_date = payment_date if payment_date else date.today()

# Class: Job
class Job:
    def __init__(self, job_id : str, description : str, contract_total : float, client_id : str):
        self.job_id : str = job_id #job id [Jxxx where xxx is 3-digit number]
        self.description : str = description
        self.contract_total : float = contract_total
        self.client_id : str = client_id

    @staticmethod
    def find_job(jid: str) -> "Job | None":
        '''find job object by job id'''
        return next((j for j in all_jobs if j.job_id.upper() == jid.upper()), None)

    @staticmethod
    def generate_job_id() -> str:
        '''generate new job id'''
        num = 0
        for j in all_jobs:
            num = max(num, int(j.job_id[-5:])) # remove 'J' and convert to int
        return f"J{num + 1:05d}"
    
    @property
    def client(self) -> "Client | None":
        '''return the client object associated with this job'''
        return Client.find_client(self.client_id)

    def get_invoices(self) -> list[Invoice]:
        '''get all invoices related to this job'''
        return [inv for inv in all_invoices if inv.job_id == self.job_id]

    def get_paid_total(self) -> float:
        '''return the total amount of paid invoices'''
        return sum(inv.amount for inv in self.get_invoices() if inv.is_paid)

    def get_billed_total(self) -> float:
        '''return the total amount of all invoices'''
        return sum(inv.amount for inv in self.get_invoices())

    def get_outstanding_balance(self) -> float:
        '''return the outstanding balance (i.e. contract total - paid total)'''
        return self.contract_total - self.get_paid_total()
