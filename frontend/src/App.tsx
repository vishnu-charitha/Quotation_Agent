import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [rejectedData, setRejectedData] = useState<any>(null);
  const [error, setError] = useState("");

  const generateQuotation = async () => {
    if (!query.trim()) {
      setError("Please enter customer requirements.");
      return;
    }

    // Reset previous results
    setResult(null);
    setRejectedData(null);
    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/generate-quotation",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query,
          }),
        }
      );

      const data = await response.json();

      // Handle backend HTTP errors
      if (!response.ok) {
        setError(data.detail || "Something went wrong.");
        return;
      }

      // Handle rejected quotation
      if (data.status === "rejected") {
        setRejectedData(data);
        return;
      }

      // Handle successful quotation
      if (
        data.status === "success" &&
        data.selected_product &&
        data.pricing_details &&
        data.quotation
      ) {
        setResult(data);
        return;
      }

      // Unexpected response
      setError("Unexpected response received from the backend.");
    } catch (error) {
      console.error(error);

      setError(
        "Could not connect to the FastAPI backend. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="quotation-container">
        <div className="header">
          <h1>Quotation Agent</h1>
          <p>AI-Powered Product Quotation Generator</p>
        </div>

        <div className="form-card">
          <h2>Enter Customer Requirement</h2>

          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Example: My name is Charitha. I need 10 laptops with Intel Core i5 processor, 16GB RAM and 512GB SSD. My maximum budget is 800000."
          />

          <button
            onClick={generateQuotation}
            disabled={loading}
          >
            {loading ? "Generating..." : "Generate Quotation"}
          </button>
        </div>

        {/* LOADING */}
        {loading && (
          <div className="loading-card">
            <h2>Generating quotation...</h2>
            <p>Please wait while the AI processes your requirements.</p>
          </div>
        )}

        {/* ERROR */}
        {error && (
          <div className="error-card">
            <h2>Connection / Request Error</h2>
            <p>{error}</p>
          </div>
        )}

        {/* REJECTED QUOTATION */}
        {rejectedData && (
          <div className="rejected-card">
            <h2>Quotation Rejected ❌</h2>

            <div className="info-section">
              <h3>Customer Details</h3>

              <p>
                <strong>Name:</strong>{" "}
                {rejectedData.customer_name || "Not Available"}
              </p>

              <p>
                <strong>Quantity:</strong>{" "}
                {rejectedData.requirements?.quantity || "Not Available"}
              </p>

              <p>
                <strong>Maximum Budget:</strong> ₹
                {rejectedData.requirements?.max_budget || "Not Available"}
              </p>
            </div>

            <div className="info-section">
              <h3>Reason</h3>

              <p>
                {rejectedData.message ||
                  "No matching product fits within the specified budget."}
              </p>
            </div>

            {/* Show cheapest product if available */}
            {rejectedData.selected_product && (
              <div className="info-section">
                <h3>Cheapest Available Product</h3>

                <p>
                  <strong>Brand:</strong>{" "}
                  {rejectedData.selected_product.brand}
                </p>

                <p>
                  <strong>Model:</strong>{" "}
                  {rejectedData.selected_product.model}
                </p>

                <p>
                  <strong>Processor:</strong>{" "}
                  {rejectedData.selected_product.processor}
                </p>

                <p>
                  <strong>RAM:</strong>{" "}
                  {rejectedData.selected_product.ram}
                </p>

                <p>
                  <strong>Storage:</strong>{" "}
                  {rejectedData.selected_product.storage}
                </p>

                {rejectedData.pricing_details?.final_total && (
                  <p className="total">
                    <strong>
                      Estimated Final Total: ₹
                      {rejectedData.pricing_details.final_total}
                    </strong>
                  </p>
                )}
              </div>
            )}
          </div>
        )}

        {/* SUCCESSFUL QUOTATION */}
        {result && (
          <div className="success-card">
            <h2>Quotation Generated Successfully 🎉</h2>

            <div className="info-section">
              <h3>Customer Details</h3>

              <p>
                <strong>Name:</strong> {result.customer_name}
              </p>

              <p>
                <strong>Quantity:</strong>{" "}
                {result.requirements?.quantity}
              </p>

              <p>
                <strong>Maximum Budget:</strong> ₹
                {result.requirements?.max_budget}
              </p>
            </div>

            <div className="info-section">
              <h3>Selected Product</h3>

              <p>
                <strong>Brand:</strong>{" "}
                {result.selected_product?.brand}
              </p>

              <p>
                <strong>Model:</strong>{" "}
                {result.selected_product?.model}
              </p>

              <p>
                <strong>Processor:</strong>{" "}
                {result.selected_product?.processor}
              </p>

              <p>
                <strong>RAM:</strong>{" "}
                {result.selected_product?.ram}
              </p>

              <p>
                <strong>Storage:</strong>{" "}
                {result.selected_product?.storage}
              </p>

              <p>
                <strong>Warranty:</strong>{" "}
                {result.selected_product?.warranty}
              </p>
            </div>

            <div className="info-section">
              <h3>Pricing Details</h3>

              <p>
                <strong>Price Per Unit:</strong> ₹
                {result.pricing_details?.selling_price_per_unit}
              </p>

              <p>
                <strong>Quantity:</strong>{" "}
                {result.pricing_details?.quantity}
              </p>

              <p>
                <strong>Subtotal:</strong> ₹
                {result.pricing_details?.subtotal}
              </p>

              <p>
                <strong>GST:</strong> ₹
                {result.pricing_details?.gst_amount}
              </p>

              <p className="total">
                <strong>
                  Final Total: ₹{result.pricing_details?.final_total}
                </strong>
              </p>
            </div>

            <div className="info-section">
              <h3>Quotation Details</h3>

              <p>
                <strong>Quotation Number:</strong>{" "}
                {result.quotation?.quotation_number}
              </p>

              <p>
                <strong>Approval Status:</strong>{" "}
                {result.approval_status}
              </p>
            </div>

            {/* DOWNLOAD PDF BUTTON */}
            {result.quotation?.quotation_number && (
              <a
                className="download-button"
                href={`http://127.0.0.1:8000/download-quotation/${result.quotation.quotation_number}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                Download Quotation PDF
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;