## **Task 1 - OOP-based application development**

**5-minute introduction video** [To be input]

### Intoduction

The **Service Record Management System (SRMS)** is an application developed using the Python programming language. It is designed to assist small companies in managing clients, jobs and invoices. The system allows for the creation of client profiles, the tracking of job contracts, the issuing of invoices, and the recording of payments.

---

### Prerequisites

#### Required Python Packages
- **PyYAML** - for reading and writing YAML data files
- **tkinter** - for the graphical user interface 
- **matplotlib** — for rendering the monthly payment chart

### Data Storage

#### Data File
- The loading data should be the same folder with python file
- Data is persisted in `data.yaml` file with the following structure:

```yaml
clients:
  - client_id: C00001
    name: Client Name
    phone: 1234567890
    address: Client Address

jobs:
  - job_id: J00001
    description: Job Description
    contract_total: 1000.00
    client_id: C00001

invoices:
  - invoice_id: INV-2026-00001
    job_id: J00001
    amount: 500.00
    issue_date: "2026-04-05"
    payment_date: null
    is_paid: false
    notes: ""
```
---

### Classes

#### Client Class
Represents a client in the system.

**Attributes:**
- `client_id`: Unique client identifier (format: C followed by 5-digit number)
- `name`: Client name
- `phone`: Contact phone number
- `address`: Client address

**Method**
- `__init__(client_id, name, phone, address)`: Initialize a client with ID, name, phone, and address
- `find_client(cid)`: Static method to find a client object by client ID
- `generate_client_id()`: Static method to generate a new unique client ID (format: Cxxxxx)
---

#### Job Class
Represents a job contract for a client.

**Attributes:**
- `job_id`: Unique job identifier (format: J followed by 5-digit number)
- `description`: Job description
- `contract_total`: Total contract value
- `client_id`: Reference to the client

**Properties:**
- `client`: Returns the Client object associated with this job

**Methods:**
- `__init__(job_id, description, contract_total, client_id)`: Initialize a job with ID, description, contract value, and client ID
- `find_job(jid)`: Static method to find a job object by job ID (case-insensitive)
- `generate_job_id()`: Static method to generate a new unique job ID (format: Jxxxxx)
- `get_invoices()`: Get all invoices related to this job
- `get_paid_total()`: Calculate total amount of paid invoices
- `get_billed_total()`: Calculate total amount of all invoices
- `get_outstanding_balance()`: Calculate outstanding balance (contract total - paid total)

---

#### Invoice Class
Represents an invoice for a job.

**Attributes:**
- `invoice_id`: Unique invoice identifier (format: INV-YYYY-xxxxx)
- `amount`: Invoice amount
- `job_id`: Reference to the job
- `issue_date`: Date invoice was issued
- `payment_date`: Date payment was received (None if unpaid)
- `is_paid`: Boolean indicating payment status
- `notes`: Optional notes

**Properties:**
- `job`: Returns the Job object associated with this invoice
- `client`: Returns the Client object associated with this invoice's job
- `status_label`: Returns payment status ("PAID on YYYY-MM-DD" or "UNPAID")

**Methods:**
- `__init__(invoice_id, amount, job_id, issue_date, payment_date, notes)`: Initialize an invoice
- `find_invoice(inv_id)`: Static method to find an invoice by invoice ID (case-insensitive)
- `generate_invoice_id()`: Static method to generate a new unique invoice ID (format: INV-YYYY-xxxxx)
- `mark_as_paid(payment_date)`: Mark the invoice as paid and set payment date


---

### Data Management Functions

#### load_data()
Load all data from the YAML file into memory.

**Procedure:**
1. Reads data.yaml file
2. Creates Client objects from client data
3. Creates Job objects from job data
4. Creates Invoice objects from invoice data (converts date strings to date objects)

---

#### save_data(clients, jobs, invoices)
Save all data from memory to the YAML file.

**Procedure:**
1. Converts objects to dictionaries
2. Converts date objects to ISO format strings
3. Writes data to data.yaml file

---

