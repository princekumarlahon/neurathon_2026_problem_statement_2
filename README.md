🧠 Bharat Biz-Agent

AI-Powered Smart Order & Revenue Management System for Small Businesses
________________________________________

🚀 Overview
Bharat Biz-Agent is an intelligent backend system designed to help small businesses automate order management, inventory tracking, and revenue monitoring — all through a conversational interface.
Instead of manually updating stock and calculating revenue, business owners can interact naturally with an AI assistant that handles everything in real time.
This project was built to demonstrate how AI + backend automation can simplify daily business operations.
________________________________________

🎯 Problem We Solved
Small businesses often struggle with:
•Manual order recording
•Inventory mismanagement
•Revenue calculation errors
•Lack of analytics dashboard
•No intelligent automation
Most small vendors still rely on notebooks or spreadsheets.
We built a system that replaces that manual workflow with an AI-powered assistant.
________________________________________

💡 Our Solution

Bharat Biz-Agent combines:
•Natural Language Processing (LLM-based intent detection)
•Backend automation using Flask
•MySQL-based inventory & order management
•Real-time revenue analytics
•Admin dashboard using Streamlit

Users can:

•Ask for product availability
•Place orders naturally
•Generate draft invoices
•Confirm orders
•Automatically update inventory
•Track total and daily revenue
•Monitor stock levels
•Manage credit (udhaar)
________________________________________

🏗 System Architecture
Customer → Chat Interface (Streamlit)
           ↓
        Flask Backend
           ↓
     LLM Intent Analyzer
           ↓
     Business Logic Layer
           ↓
        MySQL Database
           ↓
 Admin Dashboard + Revenue Metrics
________________________________________

🔥 Key Features

🗣 Conversational Order System

Users can place orders in natural language.
Example:
Is chocolate cake available?
I want 2 vanilla cake

The system automatically:

•Detects intent
•Extracts product and quantity
•Updates inventory
•Generates invoice draft
________________________________________

🧾 Invoice Confirmation Flow

Orders are first created as PENDING.
On confirmation:
•Invoice is generated
•Order becomes CONFIRMED
•Revenue updates automatically
________________________________________

📦 Inventory Management
•Real-time stock updates
•Low stock detection
•Admin can update inventory manually
•Automatic quantity deduction after confirmed orders
________________________________________

💰 Revenue Analytics
Admin dashboard displays:
•Total Revenue
•Today’s Revenue
•Confirmed orders only
•Live updates from database
________________________________________

💳 Credit (Udhaar) Tracking
System supports:
•Adding customer credit
•Storing unpaid amounts
•Tracking credit records
________________________________________

🛠 Tech Stack
•Python (Flask)
•Streamlit
•MySQL
•Groq LLM API
•REST API Architecture
•Session-based conversational memory
________________________________________

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/princekumarlahon/neurathon_2026_problem_statement_2.git
cd bharat-biz-agent
________________________________________

2️⃣ Install Dependencies
pip install -r requirements.txt
________________________________________

3️⃣ Setup Database
Create MySQL database:
CREATE DATABASE biz_agent;
Then run project once to auto-create tables
(or manually initialize schema if required).
________________________________________

4️⃣ Add Environment Variables
Create .env file:
GROQ_API_KEY=your_api_key_here
________________________________________

5️⃣ Run Backend
python main.py
________________________________________

6️⃣ Run Frontend
streamlit run streamlit_app.py
________________________________________

📊 Example Workflow
Customer asks:
“Chocolate cake available?”
2.System responds with availability.
3.Customer says:
“2 chocolate cake dena”
4.System generates draft invoice.
5.Admin confirms invoice.
6.Revenue updates automatically.
________________________________________

🧠 What Makes This Project Unique?
This is not just a chatbot.
It is a conversational business automation system that integrates:
•AI intent detection
•Stateful conversation memory
•Backend order processing
•Revenue intelligence
•Inventory automation
It demonstrates how AI can move beyond Q&A systems and directly power business operations.
________________________________________

🚀 Future Improvements
•Multi-store support
•Payment gateway integration
•Sales forecasting
•Revenue trend graphs
•Mobile app integration
•Multi-language support
________________________________________

👨‍💻 Author
Built with ❤️ to explore the intersection of AI and real-world business automation.

