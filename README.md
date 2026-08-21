Quotation Agent using LangGraph

An AI-powered quotation generation system built using LangGraph, FastAPI, and Python.

The application takes customer requirements such as processor, RAM, storage, quantity, and maximum budget. It searches available products, selects the best matching option, calculates pricing and GST, generates a quotation, processes approval, creates a PDF quotation, and provides an API endpoint to download the PDF.

Features
Customer requirement processing
Product search based on requirements
Best product selection
Supplier-based product data
Pricing calculation
Profit margin calculation
GST calculation
Automatic approval workflow
Quotation generation
PDF quotation generation
PDF download API
LangGraph workflow orchestration
FastAPI REST API
Pydantic request and response validation
Pytest workflow testing
Workflow
Customer Requirements
        │
        ▼
Requirement Node
        │
        ▼
Product Search Node
        │
        ▼
Pricing Node
        │
        ▼
Quotation Node
        │
        ▼
Approval Node
        │
        ├── Auto Approval
        │
        └── Manual Approval
        │
        ▼
PDF Generation Node
        │
        ▼
Final Response
Project Architecture
Quotation_Agent/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── graph.py
│   ├── state.py
│   ├── schemas.py
│   │
│   ├── nodes/
│   │   ├── requirement_node.py
│   │   ├── product_search_node.py
│   │   ├── pricing_node.py
│   │   ├── quotation_node.py
│   │   ├── approval_node.py
│   │   ├── manual_approval_node.py
│   │   └── pdf_node.py
│   │
│   └── tools/
│       ├── supplier_tool.py
│       ├── price_calculator.py
│       └── quotation_generator.py
│
├── generated_quotations/
│
├── tests/
│   └── test_langgraph_workflow.py
│
├── main.py
├── requirements.txt
└── README.md
Technologies Used
Python
LangGraph
FastAPI
Pydantic
Uvicorn
Pytest
ReportLab
REST API
Installation
1. Clone the repository
git clone https://github.com/vishnu-charitha/Quotation_Agent.git
2. Navigate to the project
cd Quotation_Agent
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment
Windows
venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
Running the Application

Start the FastAPI server using:

python -m uvicorn main:app --reload

The application will run at:

http://127.0.0.1:8000

Open the Swagger API documentation:

http://127.0.0.1:8000/docs
API Endpoints
Home

GET

/

Response:

{
  "message": "Quotation Agent API is running successfully"
}
Generate Quotation

POST

/generate-quotation

Example request:

{
  "customer_name": "XYZ Solutions",
  "processor": "i7",
  "ram": "16GB",
  "storage": "512GB SSD",
  "quantity": 10,
  "max_budget": 70000
}

The LangGraph workflow performs:

Process customer requirements.
Search matching products.
Select the best product.
Calculate profit margin.
Calculate GST.
Generate a quotation.
Process quotation approval.
Generate a PDF quotation.

Example response structure:

{
  "customer_name": "XYZ Solutions",
  "selected_product": {
    "product_id": "L001",
    "supplier": "Tech Supplier A",
    "brand": "Lenovo",
    "model": "IdeaPad Slim 5",
    "processor": "Intel Core i5",
    "ram": "16GB",
    "storage": "512GB SSD",
    "price": 50000,
    "warranty": "1 Year"
  },
  "pricing_details": {
    "supplier_price_per_unit": 50000,
    "quantity": 10,
    "profit_margin_percent": 10,
    "profit_amount_per_unit": 5000,
    "selling_price_per_unit": 55000,
    "subtotal": 550000,
    "gst_rate": 18,
    "gst_amount": 99000,
    "final_total": 649000
  },
  "approval_status": "approved",
  "pdf_path": "generated_quotations/QT-XXXXXXXX.pdf"
}
Download Quotation PDF

GET

/download-quotation/{quotation_number}

Example:

/download-quotation/QT-20260821150039

This endpoint downloads the generated quotation PDF.

Testing

Run the LangGraph workflow test using:

python -m pytest tests/test_langgraph_workflow.py -s

Example workflow output:

--- REQUIREMENT NODE ---


--- PRODUCT SEARCH NODE ---


--- PRICING NODE ---


--- QUOTATION NODE ---


--- APPROVAL NODE ---


--- PDF GENERATION NODE ---


FINAL LANGGRAPH RESULT
LangGraph Workflow

The project uses LangGraph to manage the quotation generation workflow.

Each node is responsible for a specific task:

Node	Responsibility
Requirement Node	Processes customer requirements
Product Search Node	Searches and selects matching products
Pricing Node	Calculates profit, subtotal, GST, and final total
Quotation Node	Creates the quotation
Approval Node	Determines the approval flow
Manual Approval Node	Handles quotations requiring manual approval
PDF Node	Generates the quotation PDF
Future Improvements
Integrate a real supplier API
Store products in a database
Add MongoDB or PostgreSQL
Add user authentication
Add quotation history
Build a React or Next.js frontend
Add email functionality for sending quotations
Add human-in-the-loop approval using LangGraph interrupts
Add multiple supplier price comparison
Deploy the API to the cloud
Author

Vishnu Charitha

GitHub: vishnu-charitha
