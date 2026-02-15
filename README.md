🧠 Bharat Biz-Agent

AI-Powered Smart Order & Revenue Management System for Small Businesses

🚀 Overview

Bharat Biz-Agent is an intelligent backend system designed to help small businesses automate order management, inventory tracking, and revenue monitoring — all through a conversational interface.

Instead of manually updating stock and calculating revenue, business owners can interact naturally with an AI assistant that handles everything in real time.

This project was built to demonstrate how AI + backend automation can simplify daily business operations.

🎯 Problem We Solved

Small businesses often struggle with:

Manual order recording

Inventory mismanagement

Revenue calculation errors

Lack of analytics dashboard

No intelligent automation

Most small vendors still rely on notebooks or spreadsheets.

We built a system that replaces that manual workflow with an AI-powered assistant.

💡 Our Solution

Bharat Biz-Agent combines:

Natural Language Processing (LLM-based intent detection)

Backend automation using Flask

MySQL-based inventory & order management

Real-time revenue analytics

Admin dashboard using Streamlit

Users can:

Ask for product availability

Place orders naturally

Generate draft invoices

Confirm orders

Automatically update inventory

Track total and daily revenue

Monitor stock levels

Manage credit (udhaar)

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

🔥 Key Features
🗣 Conversational Order System

Users can place orders in natural language.

Example:

Is chocolate cake available?
I want 2 vanilla cake


The system automatically:

Detects intent

Extracts product and quantity

Updates inventory

Generates invoice draft

🧾 Invoice Confirmation Flow

Orders are first created as PENDING.

On confirmation:

Invoice is generated

Order becomes CONFIRMED

Revenue updates automatically

📦 Inventory Management

Real-time stock updates

Low stock detection

Admin can update inventory manually

Automatic quantity deduction after confirmed orders

💰 Revenue Analytics

Admin dashboard displays:

Total Revenue

Today’s Revenue

Confirmed orders only

Live updates from database

💳 Credit (Udhaar) Tracking

System supports:

Adding customer credit

Storing unpaid amounts

Tracking credit records

🛠 Tech Stack

Python (Flask)

Streamlit

MySQL

Groq LLM API

REST API Architecture

Session-based conversational memory

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/yourusername/bharat-biz-agent.git
cd bharat-biz-agent

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Setup Database

Create MySQL database:

CREATE DATABASE biz_agent;


Then run project once to auto-create tables
(or manually initialize schema if required).

4️⃣ Add Environment Variables

Create .env file:

GROQ_API_KEY=your_api_key_here

5️⃣ Run Backend
python main.py

6️⃣ Run Frontend
streamlit run streamlit_app.py

📊 Example Workflow

Customer asks:
“Chocolate cake available?”

System responds with availability.

Customer says:
“2”

System generates draft invoice.

Admin confirms invoice.

Revenue updates automatically.

🧠 What Makes This Project Unique?

This is not just a chatbot.

It is a conversational business automation system that integrates:

AI intent detection

Stateful conversation memory

Backend order processing

Revenue intelligence

Inventory automation

It demonstrates how AI can move beyond Q&A systems and directly power business operations.

🚀 Future Improvements

Multi-store support

Payment gateway integration

Sales forecasting

Revenue trend graphs

Mobile app integration

Multi-language support

👨‍💻 Author

Built with ❤️ to explore the intersection of AI and real-world business automation.
