from fpdf import FPDF
import os

# Tạo thư mục lưu PDF nếu chưa có
os.makedirs("data", exist_ok=True)

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", 'B', 16)

# Tiêu đề
pdf.cell(0, 10, "House Price Prediction Knowledge Base", ln=True, align="C")
pdf.ln(10)

pdf.set_font("Arial", '', 12)

# Section 1: Project Overview
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "1. Project Overview", ln=True)
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8,
    "This project is a machine learning application for predicting house prices by area. "
    "The model analyzes historical data and relevant features to estimate prices. "
    "Currently, the model is experimental and may not be fully accurate, "
    "so predictions should be interpreted with caution."
)
pdf.ln(5)

# Section 2: Key Metrics and Indicators
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "2. Key Metrics and Indicators", ln=True)
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8,
    "- Average Price per Area: The mean house price in a specific region.\n"
    "- Price Deviation: The standard deviation of house prices, indicating variability.\n"
    "- Price Trends: Information about whether prices are generally increasing or decreasing over time.\n"
    "- Other Indicators: May include median price, price per square meter, or market sentiment."
)
pdf.ln(5)

# Section 3: Common Customer Questions
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "3. Common Customer Questions", ln=True)
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8,
    "Examples of questions users might ask:\n"
    "- What is the average price in District 1?\n"
    "- Are house prices going up in my area?\n"
    "- Why is the predicted price so high/low?\n"
    "- How reliable is the prediction?\n"
    "- Can you explain the price deviation?"
)
pdf.ln(5)

# Section 4: Explanations for Users
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "4. Explanations for Users", ln=True)
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8,
    "- Average Price: Gives a quick estimate of what houses typically cost in a region.\n"
    "- Price Deviation: High deviation means prices vary a lot; low deviation means prices are stable.\n"
    "- Price Trends: Upward trend indicates rising prices, downward trend indicates falling prices.\n"
    "- Interpretation Tips: Consider location, house size, and other features when looking at predictions."
)
pdf.ln(5)

# Section 5: Usage Notes for Chatbot
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "5. Usage Notes for Chatbot", ln=True)
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8,
    "This PDF is intended as a reference for the chatbot. It should read this content "
    "to answer user questions about the house price prediction project. "
    "If a question cannot be fully answered, the chatbot should ask for the user's email "
    "for follow-up and record the unknown question for future improvement."
)

# Lưu PDF
pdf.output("data/house_price_knowledge.pdf")
print("PDF created: data/house_price_knowledge.pdf")
