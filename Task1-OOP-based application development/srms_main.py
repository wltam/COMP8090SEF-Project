import yaml
import os
from collections import defaultdict
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox
from srms_class import (
    Client, Job, Invoice,
    all_clients, all_jobs, all_invoices
)
from srms_report import build_month_graph


# ==========================================
# Config
# ==========================================

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.yaml")

# ==========================================
# YAML I/O
# ==========================================

# function to load / save data from/to YAML file
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data : dict = yaml.safe_load(f) # data is dict with keys: clients, jobs, invoices

    #convert client to dict to object
    for c in data.get("clients", []):
        all_clients.append(Client(c["client_id"], c["name"], c["phone"], c["address"]))

    #convert job to dict to object
    for j in data.get("jobs", []):
        all_jobs.append(Job(j["job_id"], j["description"], j["contract_total"], j["client_id"]))

    #convert invoice to dict to object
    for inv in data.get("invoices", []):
        issue_date: date = date.fromisoformat(str(inv["issue_date"])) #convert string to date 
        payment_date: date | None = date.fromisoformat(str(inv["payment_date"])) if inv.get("payment_date") else None
        all_invoices.append(Invoice(inv["invoice_id"], float(inv["amount"]), inv["job_id"], 
                                    issue_date, payment_date, inv.get("notes", "")))
    return True

def save_data(clients, jobs, invoices):
    data = {
        "clients":  [{"client_id": cli.client_id, 
                      "name": cli.name, 
                      "phone": cli.phone, 
                      "address": cli.address} for cli in clients],  #list for client dict
        "jobs":     [{"job_id": job.job_id, 
                      "description": job.description, 
                      "contract_total": job.contract_total, 
                      "client_id": job.client_id} for job in jobs], #list for job dict
        "invoices": [{"invoice_id": inv.invoice_id,             
                        "job_id": inv.job_id,
                        "amount": inv.amount,
                        "issue_date": inv.issue_date.isoformat(), #change to string
                        "payment_date": inv.payment_date.isoformat() if inv.payment_date else None,
                        "is_paid": inv.is_paid,
                        "notes": inv.notes,} for inv in invoices], #list for invoice dict
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


# ==========================================
# GUI
# ==========================================

#: General Form Dialog
class FormDialog(tk.Toplevel):
    """
    Genearic form dialog
    """
    def __init__(self, parent, title, fields): #Enter for fields with a list of (label, default_value, disabled:bool)
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()  
        self.result = None

        #create entry form based on fields
        self.entries = []
        for i, (label, default, disabled) in enumerate(fields):
            tk.Label(self, text=label, anchor="w").grid(row=i, column=0, padx=12, pady=6, sticky="w")
            state = "disabled" if disabled else "normal"
            e = tk.Entry(self, width=36)
            e.grid(row=i, column=1, padx=12, pady=6)
            if default is not None:
                e.insert(0, str(default))
            e.config(state=state)
            self.entries.append(e)

        btn_frame = tk.Frame(self) #botton frame at the bottom of the dialog

        # OK and Canel buttons
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="OK",     width=10, command=self._ok).pack(side="left",  padx=6)
        tk.Button(btn_frame, text="Cancel", width=10, command=self._cancel).pack(side="left", padx=6)


        self.bind("<Return>", lambda e: self._ok())
        self.bind("<Escape>", lambda e: self._cancel())
        self.wait_window()

    def _ok(self):
        self.result = [e.get().strip() for e in self.entries]
        self.destroy()

    def _cancel(self):
        self.destroy()

# Client Tab
class ClientTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_toolbar()
        self._build_tree()
        self.refresh()

    def _build_toolbar(self):
        '''the top toolbar with buttons'''
        bar = tk.Frame(self)
        bar.pack(fill="x", padx=8, pady=6)
        tk.Button(bar, text="New Client",  width=14, command=self.on_new).pack(side="left", padx=4)
        tk.Button(bar, text="Edit Client", width=14, command=self.on_edit).pack(side="left", padx=4)

    def _build_tree(self):
        '''the treeview to display client list'''
        cols = ("client_id", "name", "phone", "address")
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=4)

        self.tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")

        #set the heading and column 
        for col, heading, width in [("client_id", "ID", 80), ("name", "Name", 180),
                                    ("phone", "Phone", 120), ("address", "Address", 300),]:
            self.tree.heading(col, text=heading)
            self.tree.column(col,  width=width, anchor="w")

        # vertical scrollbar
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def refresh(self):
        
        self.tree.delete(*self.tree.get_children()) #del existing rows
        
        #reload all clients value to the tree
        for c in all_clients:
            self.tree.insert("", "end", iid=c.client_id, values=(c.client_id, c.name, c.phone, c.address))

    def _selected_client(self) -> Client | None:
        sel = self.tree.selection() #returns tuple with selected item idd 
        if not sel:
            messagebox.showwarning("No Selection", "Please select a client first.")
            return None
        return Client.find_client(sel[0])

    def on_new(self):
        '''for creating a new client'''
        new_id = Client.generate_client_id()
        formD = FormDialog(self, "New Client", [("ID (auto)", new_id, True),
                                              ("Name", "", False),
                                              ("Phone", "", False),
                                              ("Address", "", False)])
        if formD.result:
            _, name, phone, addr = formD.result
            if not name:
                messagebox.showerror("Error", "Name is required.")
                return
            all_clients.append(Client(new_id, name, phone, addr))
            
            #always save & refresh
            save_data(all_clients, all_jobs, all_invoices)
            self.refresh()

    def on_edit(self):
        '''for editing the selected client'''
        c = self._selected_client()
        if not c:
            return
        formD = FormDialog(self, "Edit Client", [("ID (fixed)", c.client_id, True),
                                               ("Name", c.name, False),
                                               ("Phone", c.phone, False),
                                               ("Address", c.address, False)])
        if formD.result:
            _, name, phone, addr = formD.result
            if name: c.name = name
            if phone: c.phone = phone
            if addr: c.address = addr
            
            #always save & refresh
            save_data(all_clients, all_jobs, all_invoices)
            self.refresh()

# Job Tab
class JobTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_toolbar()
        self._build_tree()
        self.refresh()

    def _build_toolbar(self):
        ''''the top toolbar with buttons'''
        bar = tk.Frame(self)
        bar.pack(fill="x", padx=8, pady=6)
        tk.Button(bar, text="New Job",  width=14, command=self.on_new).pack(side="left", padx=4)
        tk.Button(bar, text="Edit Job", width=14, command=self.on_edit).pack(side="left", padx=4)

    def _build_tree(self):
        ''''the treeview to display job list'''
        cols = ("job_id", "client", "description", "contract", "billed", "paid", "outstanding")
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=4)

        self.tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")

        # set heading and column 
        for col, heading, width, anchor in [("job_id", "Job ID", 90, "w"), 
                                            ("client", "Client", 160, "w"),
                                            ("description", "Description", 200, "w"), 
                                            ("contract", "Contract", 100, "e"),
                                            ("billed", "Billed", 100, "e"),             
                                            ("paid", "Paid", 100, "e"),
                                            ("outstanding", "Outstanding", 100, "e")]:
            self.tree.heading(col, text=heading)
            self.tree.column(col,  width=width, anchor=anchor)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def refresh(self):

        self.tree.delete(*self.tree.get_children())

        for j in all_jobs:
            client = j.client #get the client object
            cname  = f"{j.client_id} - {client.name}" if client else f"Unknown ({j.client_id})"
            self.tree.insert("", "end", iid=j.job_id, values=(
                j.job_id,
                cname,
                j.description,
                f"${j.contract_total:,.2f}",
                f"${j.get_billed_total():,.2f}",
                f"${j.get_paid_total():,.2f}",
                f"${j.get_outstanding_balance():,.2f}"))

    def _selected_job(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a job first.")
            return None
        return Job.find_job(sel[0])

    def on_new(self):
        '''for creating a new job'''
        if not all_clients:
            messagebox.showerror("Error", "No clients found. Please create a client first.")
            return

        new_job_id = Job.generate_job_id()
        
        formD = FormDialog(self, "New Job", [
            ("Job ID (auto)", new_job_id, True),(f"Client ID", "", False),
            ("Description","", False), ("Contract Total", "", False)])
        
        if formD.result:
            _, cid, desc, price_str = formD.result

            #check input error
            if not Client.find_client(cid.upper()):
                messagebox.showerror("Error", f"Client '{cid.upper()}' not found.")
                return
            
            #check input error for contract total
            try:
                price = float(price_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid contract total.")
                return
            
            all_jobs.append(Job(new_job_id, desc, price, cid.upper()))
            
            
            #always save & refresh
            save_data(all_clients, all_jobs, all_invoices)
            self.refresh()

    def on_edit(self):
        '''for editing the selected job'''
        j = self._selected_job()
        if not j:
            return
        formD = FormDialog(self, "Edit Job", [
            ("Job ID (fixed)", j.job_id, True),(f"Client ID", j.client_id, False),
            ("Description", j.description, False), ("Contract Total", j.contract_total, False) ])
        
        if formD.result:
            _, cid, desc, price_str = formD.result
            
            #check input error
            if not Client.find_client(cid.upper()):
                messagebox.showerror("Error", f"Client '{cid.upper()}' not found.")
                return
            
            j.client_id = cid.upper()
            j.description = desc

            #check input error for contract total
            if price_str:
                try:
                    j.contract_total = float(price_str)
                except ValueError:
                    messagebox.showerror("Error", "Invalid contract total.")
                    return
            
            #always save & refresh
            save_data(all_clients, all_jobs, all_invoices)
            self.refresh()

# GUI: Invoice Tab
class InvoiceTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_toolbar()
        self._build_tree()
        self.refresh()

    def _build_toolbar(self):
        '''top toolbar with buttons'''
        bar = tk.Frame(self)
        bar.pack(fill="x", padx=8, pady=6)
        tk.Button(bar, text="New Invoice", width=14, command=self.on_new).pack(side="left", padx=4)
        tk.Button(bar, text="Edit Invoice", width=14, command=self.on_edit).pack(side="left", padx=4)
        tk.Button(bar, text="Record Payment", width=14, command=self.on_pay).pack(side="left", padx=4)

    def _build_tree(self):
        '''treeview to display invoice list'''
        cols = ("invoice_id", "job_id", "client", "amount", "issued", "status", "notes")
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=4)

        self.tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
        # construct the columns
        for col, heading, width, anchor in [("invoice_id", "Invoice ID",  150, "w"),
                                            ("job_id", "Job ID", 90, "w"),
                                            ("client", "Client", 160, "w"), 
                                            ("amount", "Amount", 100, "e"),
                                            ("issued", "Issued", 100, "w"),
                                            ("status", "Status", 160, "w"),
                                            ("notes", "Notes", 200, "w")]:
            self.tree.heading(col, text=heading)
            self.tree.column(col,  width=width, anchor=anchor)

        #deal with vertical scrollbar
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # red tag for unpiad invoices
        self.tree.tag_configure("UNPAID", foreground="red")

    def refresh(self):
        '''load all invoices to the tree'''
        self.tree.delete(*self.tree.get_children())

        for inv in all_invoices:
            client = inv.client
            cname  = client.name if client else f"Unknown Job ({inv.job_id})"
            tag    = ("UNPAID",) if "UNPAID" in inv.status_label else ()
            self.tree.insert("", "end", iid=inv.invoice_id, 
                             values=(inv.invoice_id,
                                     inv.job_id,
                                     cname,
                                     f"${inv.amount:,.2f}",
                                     str(inv.issue_date),
                                     inv.status_label,
                                     inv.notes or ""), 
                            tags=tag)

    def _selected_invoice(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select an invoice first.")
            return None
        return Invoice.find_invoice(sel[0])

    #create new invoice for a job
    def on_new(self):
        if not all_jobs:
            messagebox.showerror("Error", "No jobs found. Please create a job first.")
            return
        invoice_id = Invoice.generate_invoice_id()
        formD = FormDialog(self, "New Invoice", [("Invoice ID (auto)", invoice_id, True),
                                                (f"Job ID (J000xx)", "",False),
                                                ("Amount", "", False),
                                                ("Issue Date (YYYY-MM-DD)", str(date.today()), False),
                                                ("Notes (optional)", "", False)]
                            )
        if not formD.result:
            return
        
        _, jid, amt_str, date_str, notes = formD.result

        job = Job.find_job(jid)
        if not job:
            messagebox.showerror("Error", f"Job '{jid}' not found.")
            return
        try:
            amount = float(amt_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return
        try:
            issue_date = date.fromisoformat(date_str) if date_str else date.today()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return
        if job.get_billed_total() + amount > job.contract_total:
            if not messagebox.askyesno("Warning", "This invoice exceeds the contract total. Continue?"):
                return #for ans NO
            
        inv = Invoice(
            invoice_id = invoice_id,
            amount = amount,
            job_id = jid.upper(),
            issue_date = issue_date,
            notes = notes,
        )

        all_invoices.append(inv)

        #always save and refresh
        save_data(all_clients, all_jobs, all_invoices)
        self.refresh()

    def on_edit(self):
        inv = self._selected_invoice() #return invoice object
        if not inv:
            return

        formD = FormDialog(self, "Edit Invoice", [
            ("Invoice ID (fixed)", inv.invoice_id, True),
            ("Amount", inv.amount, False),
            ("Notes", inv.notes, False),
        ])

        if formD.result:
            _, amt_str, notes = formD.result
            if amt_str:
                try:
                    inv.amount = float(amt_str)
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount.")
                    return
            inv.notes = notes
            
            #always save and refresh
            save_data(all_clients, all_jobs, all_invoices)
            self.refresh()

    def on_pay(self):

        inv = self._selected_invoice() #return invoice object

        if not inv:
            return
        if inv.is_paid:
            messagebox.showerror("Error", "Invoice is already paid.")
            return
        formD = FormDialog(self, "Record Payment", [
            ("Invoice ID (fixed)", inv.invoice_id, True),
            ("Payment Date (YYYY-MM-DD)", str(date.today()), False),
        ])

        if not formD.result:
            return
        
        _, date_str = formD.result

        try:
            pay_date = date.fromisoformat(date_str) if date_str else date.today() #check date format
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")
            return
        
        inv.mark_as_paid(pay_date)

        #always save and refresh
        save_data(all_clients, all_jobs, all_invoices)
        self.refresh()

# Reporting
class Reporting(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.content_frame = None
        self._build_toolbar()

    def _build_toolbar(self):
        '''top toolbar with buttons'''
        bar = tk.Frame(self)
        bar.pack(fill="x", padx=8, pady=6)
        tk.Button(bar, text="By Client", width=14, command=self.by_client).pack(side="left", padx=4)
        tk.Button(bar, text="By Month", width=14, command=self.by_month).pack(side="left", padx=4)
        tk.Button(bar, text="Month (Graph)", width=14, command=self.month_graph).pack(side="left", padx=4)

    def by_client(self):
        '''tree view to display report'''
        
        #reset old content
        if self.content_frame is not None:
            self.content_frame.destroy()
        
        #build new tree for report
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=8, pady=4)

        cols = ("client_id", "client_name", "c_total_contract", "c_total_billed", "c_total_paid", "c_outstanding")
        
        tree = ttk.Treeview(self.content_frame, columns=cols, show="headings")

        #set heading and column
        for col, heading, width, anchor in [("client_id", "Client ID", 90, "w"), 
                                            ("client_name", "Client Name", 160, "w"),
                                            ("c_total_contract", "Total Contract", 120, "e"), 
                                            ("c_total_billed", "Total Billed", 120, "e"),
                                            ("c_total_paid", "Total Paid", 120, "e"),
                                            ("c_outstanding", "Outstanding Balance", 120, "e")]:
            tree.heading(col, text=heading)
            tree.column(col,  width=width, anchor=anchor)
        
        vsb = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        for c in all_clients:
            client_id = c.client_id
            client_name = c.name
            
            # calculate totals contract total
            c_total_contract = 0
            for j in all_jobs:
                if j.client_id == client_id:
                    c_total_contract += j.contract_total

            
            c_total_billed = 0
            c_total_paid = 0

            for inv in all_invoices:
                job = Job.find_job(inv.job_id)

                if job and job.client_id == client_id:
                    # calculate total billed
                    c_total_billed += inv.amount
                    
                    # calculate total paid
                    if inv.is_paid:
                        c_total_paid += inv.amount

            # calculate outstanding balance
            c_outstanding = c_total_contract - c_total_paid

            # input to the tree
            tree.insert("", "end", iid=client_id, values=(
                client_id,
                client_name,
                f"${c_total_contract:,.2f}",
                f"${c_total_billed:,.2f}",
                f"${c_total_paid:,.2f}",
                f"${c_outstanding:,.2f}"
            ))

    def by_month(self):
        '''tree view to display report by month'''
        #reset old content
        if self.content_frame is not None:
            self.content_frame.destroy()

        #build new tree for report
        self.content_frame = tk.Frame(self)

        cols = ("month", "total_invoices", "total_billed", "total_paid")

        self.content_frame.pack(fill="both", expand=True, padx=8, pady=4)
        tree = ttk.Treeview(self.content_frame, columns=cols, show="headings")

        #set heading and column
        for col, heading, width, anchor in [("month", "Month", 120, "w"), 
                                            ("total_invoices", "Total Invoices", 120, "e"),
                                            ("total_billed", "Total Billed", 120, "e"), 
                                            ("total_paid", "Total Paid", 120, "e")]:
            tree.heading(col, text=heading)
            tree.column(col,  width=width, anchor=anchor)

        #vertical scrollbar
        vsb = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # aggregate data by month
        monthly_data = {}
        for inv in all_invoices:
            month = inv.issue_date.strftime("%Y-%m") #group by year-month
            # set for initial value for each month if not exist
            if month not in monthly_data:
                monthly_data[month] = {"total_invoices": 0, "total_billed": 0.0, "total_paid": 0.0}

            monthly_data[month]["total_invoices"] += 1
            monthly_data[month]["total_billed"] += inv.amount
            if inv.is_paid:
                monthly_data[month]["total_paid"] += inv.amount

        # input to the tree
        for month, data in sorted(monthly_data.items()):
            tree.insert("", "end", iid=month, values=(
                month,
                data["total_invoices"],
                f"${data['total_billed']:,.2f}",
                f"${data['total_paid']:,.2f}"))
    
    def month_graph(self):
        '''graph view to display report by month'''
        
        # calculate total paid amount for each month
        monthly : dic = defaultdict(float) # special dict [not return KeyError]

        for inv in all_invoices:
            if inv.is_paid and inv.payment_date:
                key = inv.payment_date.replace(day=1)  # set to 1st day of month
                monthly[key] += inv.amount #calculate the total amount for each month

        if not monthly:
            return [], []

        sorted_months = sorted(monthly.keys())
        amounts = [monthly[m] for m in sorted_months]

        if self.content_frame is not None:
            self.content_frame.destroy()

        #reset old content
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=8, pady=4)
        build_month_graph(self.content_frame, sorted_months, amounts)

# About
class About(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Service Record Management System\n" \
        "Version 1.0\n\nCourse: COMP8090", justify="center").pack(expand=True)

# GUI: Main Window
class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Service Record Management System")
        self.geometry("1200x500")
        self.resizable(True, True)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.client_tab = ClientTab(notebook) #frame for client tab
        self.job_tab = JobTab(notebook) #frame for job tab
        self.invoice_tab = InvoiceTab(notebook) #frame for invoice tab
        self.report_tab = Reporting(notebook) #frame for report tab

        notebook.add(self.client_tab, text="  Clients  ")
        notebook.add(self.job_tab, text="  Jobs  ")
        notebook.add(self.invoice_tab, text="  Invoices  ")
        notebook.add(self.report_tab, text="  Reports  ")
        notebook.add(About(notebook), text="  About  ")

        # refresh all tabs when switching
        notebook.bind("<<NotebookTabChanged>>", self.refresh)

    def refresh(self, event=None):
        self.client_tab.refresh()
        self.job_tab.refresh()
        self.invoice_tab.refresh()


# ==========================================
# MAIN
# ==========================================

def main():
    global all_clients, all_jobs, all_invoices

    if not os.path.exists(DATA_FILE):
        messagebox.showerror("Error", f"'{DATA_FILE}' not found.\nPlease place data.yaml in the same folder.")
        return

    if load_data():
        print("Data loaded successfully.")
    else:
        messagebox.showerror("Error", "Failed to load data.")
        return

    app = Main_Window()
    app.mainloop()

if __name__ == "__main__":
    main()
