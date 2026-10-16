# Contract Analysis & Risk Assessment Bot

AI-powered legal assistant that helps small and medium business owners understand complex contracts, identify potential legal risks, and receive actionable advice in plain language.

## 🚀 Live Application
https://contract-analyzer-qpayyguvvw37h9jtprru6g.streamlit.app/

**YouTube Demo:**
https://www.youtube.com/watch?v=9h7qoEZJF4o


## 🎯 Problem Statement

Small and medium businesses in India face a critical challenge: understanding complex legal contracts without expensive legal consultations (₹5,000-20,000 per review). Our solution democratizes legal knowledge by providing instant, AI-powered contract analysis at zero cost, enabling SME owners to make informed decisions independently.


## 💡 Solution Overview

A sophisticated GenAI-powered legal assistant built with **Google Gemini 2.0 Flash** that analyzes contracts in plain language, identifies legal risks, and provides actionable advice. The system handles:

- 📝 Employment Agreements
- 🤝 Vendor Contracts  
- 🏢 Lease Agreements
- 👥 Partnership Deeds
- ⚙️ Service Contracts


## ✨ Key Features

### Core Legal NLP Tasks
✅ **Automated Contract Type Classification** with confidence scoring  
✅ **Named Entity Recognition** (parties, dates, monetary amounts, jurisdictions, obligations)  
✅ **Obligation vs. Right vs. Prohibition** identification across all contract types  
✅ **Risk & Compliance Detection** with clause-level analysis  
✅ **Template Matching** capabilities through 5 pre-built SME-friendly contracts  

### Risk Assessment Engine
✅ **Clause-level Risk Categorization** (Low/Medium/High) with detailed explanations  
✅ **Contract-level Composite Risk Score** (0-100 scale)  
✅ **Automated Identification** of:
   - Penalty Clauses
   - Indemnity Clauses
   - Unilateral Termination Rights
   - Arbitration Terms
   - Auto-Renewal Conditions
   - Non-Compete Clauses
   - IP Transfer Provisions

### User-Facing Outputs
 **Plain-Language Summary** (7-point breakdown)  
 **Clause-by-Clause Explanations** in simple business English  
 **Unfavorable Clause Highlighting** with specific concerns  
 **Suggested Renegotiation Alternatives** for problematic terms  
 **5 Standardized Contract Templates** (Employment, Service, NDA, Vendor, Partnership)  
 **Professional PDF Export** for legal consultation  

### Data Processing
 **Multi-Format Support**: PDF (pdfplumber), DOCX (python-docx), TXT  
 **Comprehensive Data Extraction**: parties, financial amounts, obligations, deliverables, timelines, termination conditions, jurisdiction, IP rights, confidentiality terms  
 **Session-Based Audit Trail** (no data storage for privacy)  
 **English Language Support** (Hindi parsing in development roadmap)  
## 🛠️ Technology Stack

- **LLM**: Claude Sonnet 4 (Anthropic API)
- **NLP**: Python with spaCy
- **UI**: Streamlit
- **Document Processing**: pdfplumber, python-docx
- **Report Generation**: ReportLab



## 🚀 How to Use (Live App)

**Access the app:** [https://contract-analyzer-qpayyguvvw37h9jtprru6g.streamlit.app](https://contract-analyzer-qpayyguvvw37h9jtprru6g.streamlit.app)

### Quick Start:
1. **Upload** a contract file (PDF, DOCX, or TXT)
2. Click **"Extract Text from Document"**
3. Click **"Analyze Contract with AI"** (takes 1-2 minutes)
4. View results across organized tabs:
   - 📝 **Summary** - Contract type, parties, key terms
   - ⚠️ **Risk Assessment** - Risk score and categorized clauses
   - 🔍 **Key Entities** - Parties, dates, amounts, jurisdiction
   - 📋 **Obligations** - What each party must/can/cannot do
   - ⚡ **Unfavorable Clauses** - Problematic terms + alternatives
   - 📄 **Export Report** - Download PDF report
5. Optionally explore **Contract Templates** for standard agreements



## 📋 Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- pip (Python package manager)

## 🚀 Installation & Setup

### Step 1: Clone or Download the Repository
```powershell