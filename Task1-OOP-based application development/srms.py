import yaml
import os
from datetime import date

# ==========================================
# Config
# ==========================================

DATA_FILE = "data.yaml"

# ==========================================
# YAML I/O
# ==========================================

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data if data else {"clients": [], "jobs": []}

def save_data(clients, jobs):
    data = {
        "clients": [client_to_dict(c) for c in clients],
        "jobs":    [job_to_dict(j)    for j in jobs],
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

# ==========================================
# Serialization
# ==========================================

def client_to_dict(c):
    return {
        "client_id": c.client_id,
        "name":      c.name,
        "phone":     c.phone,
        "address":   c.address,
    }

def invoice_to_dict(inv):
    return {
        "invoice_id":   inv.invoice_id,
        "amount":       inv.amount,
        "issue_date":   inv.issue_date.isoformat(),
        "payment_date": inv.payment_date.isoformat() if inv.payment_date else None,
        "is_paid":      inv.is_paid,
    }

def job_to_dict(j):
    return {
        "job_id":         j.job_id,
        "description":    j.description,
        "contract_total": j.contract_total,
        "client_id":      j.client.client_id,
        "invoices":       [invoice_to_dict(inv) for inv in j.invoice_list],
    }

# ==========================================
# Deserialization
# ==========================================

def dict_to_client(d):
    return Client(d["client_id"], str(d["name"]), str(d["phone"]), d["address"])

def dict_to_invoice(d):
    issue_date   = date.fromisoformat(str(d["issue_date"]))
    payment_date = date.fromisoformat(str(d["payment_date"])) if d.get("payment_date") else None
    return Invoice(d["invoice_id"], float(d["amount"]), issue_date, payment_date)

def dict_to_job(d, clients):
    client = next((c for c in clients if c.client_id == d["client_id"]), None)
    job = Job(d["job_id"], d["description"], float(d["contract_total"]), client)
    for inv_dict in d.get("invoices", []):
        job.add_invoice(dict_to_invoice(inv_dict))
    return job

# ==========================================
# Class: Client
# ==========================================

class Client:
    def __init__(self, client_id, name, phone, address):
        self.client_id = client_id
        self.name      = name
        self.phone     = phone
        self.address   = address

    def __str__(self):
        return (f"ID: {self.client_id:<5} | Name: {self.name:<20} | "
                f"Phone: {self.phone:<12} | Addr: {self.address}")

# ==========================================
# Class: Invoice
# ==========================================

class Invoice:
    def __init__(self, invoice_id, amount, issue_date=None, payment_date=None):
        self.invoice_id   = invoice_id
        self.amount       = amount
        self.issue_date   = issue_date if issue_date else date.today()
        self.payment_date = payment_date
        self.is_paid      = payment_date is not None

    def mark_as_paid(self):
        self.is_paid      = True
        self.payment_date = date.today()

    def __str__(self):
        status = f"[PAID: {self.payment_date}]" if self.is_paid else "[UNPAID]"
        return (f"   -> Inv#: {self.invoice_id:<16} | "
                f"Amt: ${self.amount:>12,.2f} | "
                f"Issued: {self.issue_date} | {status}")

# ==========================================
# Class: Job
# ==========================================

class Job:
    def __init__(self, job_id, description, contract_total, client):
        self.job_id         = job_id
        self.description    = description
        self.contract_total = contract_total
        self.client         = client
        self.invoice_list   = []

    def add_invoice(self, inv):
        self.invoice_list.append(inv)

    def get_paid_total(self):
        return sum(inv.amount for inv in self.invoice_list if inv.is_paid)

    def get_billed_total(self):
        return sum(inv.amount for inv in self.invoice_list)

    def get_outstanding_balance(self):
        return self.contract_total - self.get_paid_total()

    def print_job_details(self):
        print("=" * 49)
        print(f"JOB ID: {self.job_id}")
        print(f"Client: {self.client.name} (ID: {self.client.client_id})")
        print(f"Desc:   {self.description}")
        print("-" * 49)
        print(f"Contract Total:  ${self.contract_total:>12,.2f}")
        print(f"Total Billed:    ${self.get_billed_total():>12,.2f}")
        print(f"Total Paid:      ${self.get_paid_total():>12,.2f}")
        print(f"OUTSTANDING FEE: ${self.get_outstanding_balance():>12,.2f}")
        print("-" * 49)
        print("Invoice History:")
        if not self.invoice_list:
            print("   (No invoices issued yet)")
        else:
            for inv in self.invoice_list:
                print(inv)
        print("=" * 49 + "\n")

# ==========================================
# Global State
# ==========================================

all_clients = []
all_jobs    = []

# ==========================================
# Utilities
# ==========================================

def find_client(cid):
    return next((c for c in all_clients if c.client_id.upper() == cid.upper()), None)

def find_job(jid):
    return next((j for j in all_jobs if j.job_id.upper() == jid.upper()), None)

def press_enter():
    input("\nPress Enter to continue...")

def generate_invoice_id():
    current_year = date.today().year
    count = sum(
        1 for j in all_jobs
          for inv in j.invoice_list
          if inv.issue_date.year == current_year
    )
    return f"INV-{current_year}-{count + 1:03d}"

# ==========================================
# CLIENT MENU
# ==========================================

def create_new_client():
    print("\n--- Create New Client ---")
    new_id = f"C{len(all_clients) + 1:03d}"
    print(f"Auto-Generated ID: {new_id}")
    name  = input("Enter Name: ").strip()
    phone = input("Enter Phone: ").strip()
    addr  = input("Enter Address: ").strip()
    all_clients.append(Client(new_id, name, phone, addr))
    save_data(all_clients, all_jobs)
    print("Success: Client added.")

def edit_client_detail():
    cid = input("\nEnter Client ID to edit (e.g. C001): ").strip()
    c   = find_client(cid)
    if not c:
        print("Error: Client not found.")
        return
    print(f"Current Info: {c}")
    name = input("Enter New Name (Enter to skip): ").strip()
    if name:
        c.name = name
        print("Name updated.")
    phone = input("Enter New Phone (Enter to skip): ").strip()
    if phone:
        c.phone = phone
        print("Phone updated.")
    addr = input("Enter New Address (Enter to skip): ").strip()
    if addr:
        c.address = addr
        print("Address updated.")
    save_data(all_clients, all_jobs)
    print("Success: Client updated.")

def list_all_clients():
    print("\n--- Client List ---")
    if not all_clients:
        print("No clients found.")
    else:
        for c in all_clients:
            print(c)

# ==========================================
# JOB MENU
# ==========================================

def create_new_job():
    print("\n--- Create New Job ---")
    cid    = input("Enter Existing Client ID (e.g. C001): ").strip()
    client = find_client(cid)
    if not client:
        print("Error: Client not found.")
        return
    new_job_id = f"J{len(all_jobs) + 1:04d}"
    desc       = input("Enter Job Description: ").strip()
    try:
        price = float(input("Enter Total Contract Price: ").strip())
    except ValueError:
        print("Error: Invalid number.")
        return
    all_jobs.append(Job(new_job_id, desc, price, client))
    save_data(all_clients, all_jobs)
    print(f"Success: Job created with ID: {new_job_id}")

def edit_job_detail():
    jid = input("\nEnter Job ID to edit: ").strip()
    job = find_job(jid)
    if not job:
        print("Error: Job not found.")
        return
    desc = input("Enter New Description (Enter to skip): ").strip()
    if desc:
        job.description = desc
        print("Description updated.")
    price_str = input("Enter New Contract Price (Enter to skip): ").strip()
    if price_str:
        try:
            job.contract_total = float(price_str)
            print("Contract Price updated.")
        except ValueError:
            print("Invalid number.")
    save_data(all_clients, all_jobs)
    print("Success: Job updated.")

def list_specific_job():
    jid = input("\nEnter Job ID to view details: ").strip()
    job = find_job(jid)
    if job:
        job.print_job_details()
    else:
        print("Error: Job not found.")

def list_all_jobs():
    print("\n--- Job List & Financial Summary ---")
    if not all_jobs:
        print("No jobs in system.")
        return
    sep = "-" * 122
    print(sep)
    print(f"{'JOB ID':<10} | {'DESCRIPTION':<30} | {'CLIENT':<20} | "
          f"{'CONTRACT TOTAL':>15} | {'PAID TOTAL':>15} | {'OUTSTANDING FEE':>15}")
    print(sep)
    total_contract = total_paid = total_outstanding = 0.0
    for j in all_jobs:
        desc  = (j.description[:28] + "..") if len(j.description) > 28 else j.description
        cname = (j.client.name[:18]  + "..") if len(j.client.name)  > 18 else j.client.name
        print(f"{j.job_id:<10} | {desc:<30} | {cname:<20} | "
              f"${j.contract_total:>13,.2f} | "
              f"${j.get_paid_total():>13,.2f} | "
              f"${j.get_outstanding_balance():>13,.2f}")
        total_contract    += j.contract_total
        total_paid        += j.get_paid_total()
        total_outstanding += j.get_outstanding_balance()
    print(sep)
    print(f"{'Total:':<66} | ${total_contract:>13,.2f} | ${total_paid:>13,.2f} | ${total_outstanding:>13,.2f}")

# ==========================================
# INVOICE & PAYMENT
# ==========================================

def issue_invoice():
    jid = input("\nEnter Job ID to invoice: ").strip()
    job = find_job(jid)
    if not job:
        print("Error: Job not found.")
        return
    try:
        amount = float(input("Enter Amount: ").strip())
    except ValueError:
        print("Error: Invalid amount.")
        return
    if job.get_billed_total() + amount > job.contract_total:
        print("WARNING: Exceeds Contract Total!")
    date_str = input("Enter Issue Date (YYYY-MM-DD) [Press Enter for Today]: ").strip()
    if date_str:
        try:
            issue_date = date.fromisoformat(date_str)
        except ValueError:
            print("Invalid date format. Using TODAY.")
            issue_date = date.today()
    else:
        issue_date = date.today()
    inv = Invoice(generate_invoice_id(), amount, issue_date, None)
    job.add_invoice(inv)
    save_data(all_clients, all_jobs)
    print(f"Success: Invoice issued ID: {inv.invoice_id} on {inv.issue_date}")

def record_payment():
    inv_id = input("Enter Invoice ID to pay: ").strip()
    found  = False
    for j in all_jobs:
        for inv in j.invoice_list:
            if inv.invoice_id.upper() == inv_id.upper():
                print(f"Invoice for Job: {j.job_id} - {j.description} | Client: {j.client.name}")
                if inv.is_paid:
                    print("Error: Already paid.")
                else:
                    inv.mark_as_paid()
                    save_data(all_clients, all_jobs)
                    print("Success: Payment recorded.")
                found = True
                break
        if found:
            break
    if not found:
        print("Error: Invoice ID not found.")

# ==========================================
# REPORTING
# ==========================================

def generate_total_summary():
    try:
        target_year = int(input("Enter Year (e.g. 2025): ").strip())
    except ValueError:
        print("Invalid input.")
        return
    month_income = [0.0] * 12
    total_income = 0.0
    for job in all_jobs:
        for inv in job.invoice_list:
            d = inv.payment_date
            if d and d.year == target_year:
                month_income[d.month - 1] += inv.amount
                total_income              += inv.amount
    print(f"\n--- Yearly Income Report: {target_year} ---")
    for m in range(12):
        print(f"{m + 1:02d}/{target_year}      $ {month_income[m]:>15,.2f}")
    print("-" * 40)
    print(f"{'Total :':<13} ${total_income:>16,.2f}")

def generate_client_summary():
    try:
        target_year = int(input("Enter Year (e.g. 2025): ").strip())
    except ValueError:
        print("Invalid input.")
        return
    print(f"\n>>> Breakdown by Client for {target_year}:")
    grand_total = 0.0
    for client in all_clients:
        client_total = sum(
            inv.amount
            for job in all_jobs if job.client is client
            for inv in job.invoice_list
            if inv.is_paid and inv.payment_date and inv.payment_date.year == target_year
        )
        if client_total > 0:
            print(f" - {client.name:<20}: ${client_total:>15,.2f}")
            grand_total += client_total
    print("   " + "-" * 40)
    print(f"   TOTAL REVENUE:        ${grand_total:>15,.2f}")

# ==========================================
# MAIN
# ==========================================

def main():
    global all_clients, all_jobs

    if not os.path.exists(DATA_FILE):
        print(f"ERROR: '{DATA_FILE}' not found.")
        print("Please place data.yaml in the same folder and restart.")
        return

    print(f"Loading data from {DATA_FILE}...")
    raw         = load_data()
    all_clients = [dict_to_client(d) for d in raw.get("clients", [])]
    all_jobs    = [dict_to_job(d, all_clients) for d in raw.get("jobs", [])]
    print(f"Loaded {len(all_clients)} clients, {len(all_jobs)} jobs.\n")

    running = True
    while running:
        print("\n=========================================")
        print("   SERVICE RECORD MANAGEMENT SYSTEM")
        print("=========================================")
        print("   [ CLIENTS ]")
        print("   1. Create New Client")
        print("   2. Edit Client Details")
        print("   3. List All Clients")
        print("-----------------------------------------")
        print("   [ JOBS & INVOICING ]")
        print("   4. Create New Job")
        print("   5. Edit Job Details")
        print("   6. Show Specific Job Details")
        print("   7. List All Jobs (Summary)")
        print("   8. Issue Invoice")
        print("   9. Record Payment to Invoice")
        print("-----------------------------------------")
        print("   [ REPORTS ]")
        print("   10. Yearly Income (Total)")
        print("   11. Yearly Income (By Client)")
        print("-----------------------------------------")
        print("   0. EXIT")
        print("=========================================")
        choice = input(">> Select Option: ").strip()

        actions = {
            "1":  create_new_client,
            "2":  edit_client_detail,
            "3":  list_all_clients,
            "4":  create_new_job,
            "5":  edit_job_detail,
            "6":  list_specific_job,
            "7":  list_all_jobs,
            "8":  issue_invoice,
            "9":  record_payment,
            "10": generate_total_summary,
            "11": generate_client_summary,
        }

        if choice == "0":
            running = False
            print("System Exiting.")
        elif choice in actions:
            actions[choice]()
            press_enter()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
