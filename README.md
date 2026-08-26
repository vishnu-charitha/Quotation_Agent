# Quotation Agent

An AI-powered product quotation generation system that helps automate the process of understanding customer requirements, matching suitable products, validating budgets, generating quotations, and handling approval or rejection scenarios.

## Features

- AI-based customer requirement extraction
- Product matching based on specifications
- RAG-based product retrieval
- Vector search using Qdrant
- Budget analysis
- Pricing calculation
- Profit margin calculation
- GST calculation
- Product availability and quantity validation
- Approval and rejection workflow
- Alternative product suggestion workflow
- Automatic quotation generation
- PDF quotation generation
- React frontend
- FastAPI backend

---

# Project Architecture


Customer Request
        │
        ▼
Requirement Extraction
        │
        ▼
RAG Retrieval
        │
        ▼
Product Search & Matching
        │
        ▼
Budget Analysis
        │
        ├───────────────┐
        ▼               ▼
   Within Budget    Exceeds Budget
        │               │
        ▼               ▼
     Pricing       Alternative Product
        │               │
        ▼               ▼
    Approval       Alternative Found?
        │            │         │
        ▼           YES        NO
   Quotation         │          │
        │            ▼          ▼
        ▼        Suggest     Reject
 PDF Generation   Alternative
Technology Stack
Backend
Python
FastAPI
LangGraph
Qdrant
Gemini Embeddings
Pydantic
ReportLab
Frontend
React
TypeScript
Vite
CSS
Project Structure
Quotation_Agent/
│
├── backend/
│   ├── main.py
│   ├── quotation_graph.py
│   ├── graph.py
│   ├── state.py
│   ├── schemas.py
│   ├── agent_tools.py
│   │
│   ├── nodes/
│   │   ├── requirement_node.py
│   │   ├── requirement_extraction_node.py
│   │   ├── rag_retrieval_node.py
│   │   ├── retrieval_node.py
│   │   ├── product_search_node.py
│   │   ├── pricing_node.py
│   │   ├── approval_node.py
│   │   ├── quotation_node.py
│   │   ├── pdf_node.py
│   │   ├── alternative_product_node.py
│   │   └── alternative_suggestion_node.py
│   │
│   ├── rag/
│   │   ├── document_loader.py
│   │   ├── text_splitter.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── ingest.py
│   │
│   └── tools/
│       ├── price_calculator.py
│       ├── quotation_generator.py
│       └── supplier_tool.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── main.tsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   ├── products.csv
│   ├── laptops.csv
│   ├── desktops.csv
│   ├── printers.csv
│   └── networking_equipment.csv
│
├── Embeddings/
│   ├── embeddings.npy
│   └── metadata.json
│
├── generated_quotations/
│
├── create_embeddings.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
Product Matching

Product information is retrieved from the product catalog data.

Example product data:

Product ID: L002
Category: Laptop
Brand: Lenovo
Model: ThinkPad E14
Processor: Intel Core i5
RAM: 16GB
Storage: 512GB SSD
Supplier Price: ₹57,000
Available Quantity: 20

The system checks:

Product category
Brand
Model
Processor
RAM
Storage
Available quantity
Budget

The main product matching logic is located in:

backend/nodes/product_search_node.py
Pricing Calculation

The quotation price is calculated using:

Supplier Price
      +
Profit Margin
      ↓
Selling Price
      ×
Quantity
      ↓
Subtotal
      +
GST
      ↓
Final Total

Example:

Supplier Price: ₹57,000

Profit Margin: 10%

Selling Price Per Unit:
₹57,000 + ₹5,700 = ₹62,700

Quantity: 10

Subtotal:
₹62,700 × 10 = ₹627,000

GST: 18%

GST Amount:
₹112,860

Final Total:
₹739,860
Approval Workflow

The quotation is approved when:

Final Total ≤ Customer Maximum Budget

Example:

Maximum Budget: ₹800,000
Final Total: ₹739,860

Status: APPROVED

If the final total exceeds the budget:

Maximum Budget: ₹500,000
Final Total: ₹739,860

Status: REJECTED
Alternative Product Suggestion

When the requested product exceeds the customer's budget, the system can search for a lower-cost alternative.

Example:

Requested Product:
Dell Latitude 3550

Specifications:
Intel Core i5
16GB RAM
512GB SSD

Budget:
₹500,000

If no exact matching product fits the budget, the system can search for an alternative product with relaxed specifications.

Example:

Alternative Product:
Lenovo IdeaPad Slim 5

Processor: Intel Core i5
RAM: 8GB
Storage: 512GB SSD

The system should clearly indicate the specification differences between the requested product and the alternative product.

Running the Backend

Navigate to the project folder:

cd C:\Users\VISHNUCHARITHA\OneDrive\Desktop\Quotation_Agent

Activate the virtual environment:

venv\Scripts\activate

Run the FastAPI application:

python -m uvicorn backend.main:app --reload

The backend will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
Running the Frontend

Open another terminal and navigate to:

cd C:\Users\VISHNUCHARITHA\OneDrive\Desktop\Quotation_Agent\frontend

Run:

npm install
npm run dev

The React application will run at:

http://localhost:5173

If port 5173 is already in use, Vite may use another port such as:

http://localhost:5174
API Endpoint
Generate Quotation
POST /generate-quotation

Example request:

{
  "query": "My name is Charitha. I need 10 laptops with Intel Core i5 processor, 16GB RAM and 512GB SSD. My maximum budget is 800000."
}
Example Approved Request
My name is Charitha. I need 10 laptops with Intel Core i5 processor, 16GB RAM and 512GB SSD. My maximum budget is 800000.

Expected result:

Product: Lenovo ThinkPad E14

Quantity: 10

Final Total: ₹739,860

Approval Status: APPROVED
Example Rejected Request
My name is Charitha. I need 10 Dell Latitude 3550 laptops with Intel Core i5 processor, 16GB RAM and 512GB SSD. My maximum budget is 500000.

Expected result:

Quotation Rejected

Reason:
The matching product exceeds the customer's maximum budget.
PDF Download

Generated quotation PDFs are stored in:

generated_quotations/

The API provides a download endpoint:

GET /download-quotation/{quotation_number}

Example:

http://127.0.0.1:8000/download-quotation/QT-20260824145753
Future Enhancements
Improve alternative product recommendation
Add customer and quotation history
Add supplier comparison
Add authentication and user management
Add quotation dashboard
Add quotation status tracking
Integrate email delivery
Add database support
Improve AI-based requirement extraction
Add multiple product quotations
Deploy frontend and backend to the cloud


Author
N Vishnu Charitha
