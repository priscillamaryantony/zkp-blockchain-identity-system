# 🔐 ZKP-Based Identity Verification System (Blockchain Fintech Project)

## 📌 Overview

This project is a **Blockchain-based Identity Verification System** that uses **Zero-Knowledge Proof (ZKP)-style logic** to verify users without exposing sensitive personal data.

It simulates a **fintech KYC (Know Your Customer) system**, where identity data is securely hashed and stored on a blockchain, ensuring:

* 🔒 Privacy
* 🔗 Data Integrity
* 🛡 Tamper Resistance

## 🚀 Key Features

### 🔐 Identity Verification

* Accepts user input (Name, Age, KYC ID)
* Simulates **PAN / Aadhaar validation**
* Determines:

  * ✅ Verified User
  * ❌ Failed (with reason)

### 🔗 Blockchain Implementation

* Custom blockchain with blocks containing:

  * Index, Timestamp, Hash, Previous Hash
* Identity stored as **hashed data**
* Chain validation using:

  * `is_chain_valid()`

### 📊 Dashboard Analytics

* Total Users
* Verified Users
* Failed Users
* 📈 Success Rate (%)
* 🔐 Blockchain Integrity Status (Secure / Tampered)

### 🔍 Search & Filters

* Filter by:

  * Verified
  * Failed
* Search by:

  * User name
  * Hashed identity

### 🧾 Verification Insights

* Shows **reason for verification result**

  * Underage
  * Invalid ID format
  * Valid PAN
  * Valid Aadhaar

### 📈 Visualization

* Interactive **Chart.js doughnut chart**
* Visual breakdown of verification results

### 🧾 Recent Activity Feed

* Displays latest verification logs
* Example:

  * `Priscilla → Verified (Valid PAN)`
  * `Riya → Failed (Underage)`

### 📥 Data Export

* Export blockchain data as **CSV file**

### 🌐 API Endpoint

* Access blockchain data via:
  /api/blocks

### 🎨 UI/UX Enhancements

* Clean, modern fintech-style UI
* Smooth hover effects & animations
* Clickable blockchain blocks (interactive highlighting)
* Loading spinner during verification
* Copy-to-clipboard for hashes
* Direct **“Go to Dashboard”** access

## 🛠 Tech Stack

* **Backend:** Python (Flask)
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **Visualization:** Chart.js
* **Concepts:** Blockchain, Zero-Knowledge Proof (ZKP)

## ▶️ How to Run

1. Clone the repository:
   git clone <your-repo-link>

2. Navigate to project folder:
   cd <project-folder>

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   python app.py

5. Open in browser:
   http://127.0.0.1:5000/

## 📸 Screenshots

* 🏠 Home Page
* 📊 Dashboard
* 📄 Verification Result

## 🎯 Project Highlights

* Simulates **real-world fintech KYC systems**
* Demonstrates **secure identity verification**
* Uses **blockchain for tamper-proof storage**
* Applies **ZKP-style logic for privacy**
* Includes **analytics + API + export features**

## 🧠 Future Enhancements (Optional)

* Real API-based KYC validation
* User authentication (login system)
* Cloud deployment with database scaling
* Role-based access (admin/user)

## 📌 Author

👩‍💻 Priscilla Mary Antony.

## ⭐ Final Note

This project demonstrates how **blockchain and privacy-preserving techniques** can be applied in fintech systems to ensure secure, transparent, and user-friendly identity verification.

