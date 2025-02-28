# AI-Powered BNPL Platform

## Introduction

### Overview of the Project
This project is an AI-driven **Buy Now, Pay Later (BNPL)** platform that leverages **Large Language Model (LLM) agents** to offer dynamic, personalized payment plans for consumers. Unlike traditional BNPL solutions that rely on static user data and rigid repayment structures, our system continuously adapts to a user’s financial situation—suggesting higher or lower installments depending on changes in **income, spending habits, and real-time indicators**.

### Key Features:
- **Automated Financial Analysis**: Real-time reading of user income, credit scores, and spending patterns.
- **Dynamic Risk & Affordability Assessment**: ML-powered risk scoring to ensure users don’t overextend themselves.
- **Customized BNPL Plans**: An intelligent recommendation engine personalizing installment amounts and schedules.
- **Conversational Financial Advisor**: An interactive agent that explains and adjusts installment options in plain language.

---
## Motivation & Use Cases
The BNPL landscape is rapidly expanding, and both consumers and businesses need **flexible, intelligent payment options** to reduce default risks. A traditional **one-size-fits-all** approach often fails to capture diverse user profiles. Our AI-driven solution provides adaptability and transparency.

### Why It Matters:
- **For Consumers:** Flexible, personalized plans that match financial reality.
- **For Businesses:** Lower risk of missed payments and valuable financial insights.
- **For Financial Institutions:** Lower barriers to credit-based purchases with responsible customer expansion.

### Sample Use Cases:
- **Seasonal or Variable Incomes:** Freelancers, gig workers, or commission-based earners needing adjustable payment schedules.
- **Unexpected Financial Changes:** Users experiencing sudden drops or increases in income.
- **High-Value Purchases:** Electronics, furniture, or tuition payments benefiting from flexible installment plans.

---
## Objectives
1. **Personalized Financial Solutions:** Generate unique BNPL plans based on individual affordability metrics.
2. **Real-Time Adjustments:** Dynamically modify installment amounts as financial status changes.
3. **Minimize Default Risk:** Use ML-driven risk scoring and LLM insights to flag payment issues early.
4. **Seamless User Experience:** Provide an intuitive AI-powered interface for users to understand and customize their plans effortlessly.

---
## System Architecture
### High-Level Overview

1. **User/Front-End Application** (e.g., Streamlit UI) initiates a request.
2. **MainAgent** orchestrates sub-agents for financial data collection and analysis.
3. **CarAgent, ClubAgent, UniversityAgent** perform targeted web searches for financial data (e.g., membership fees, car prices, tuition costs).
4. **AnalysisAgent** compiles and processes financial data.
5. **LLM Engine** (Google Generative AI or GPT-4) refines BNPL recommendations.
6. **Personalized BNPL Plan** is generated and displayed to the user.

### Agents & Their Roles
1. **ClubAgent**: Retrieves average membership fees for sports clubs.
2. **CarAgent**: Collects average car prices in the user's location.
3. **UniversityAgent**: Fetches tuition fee estimates for specific universities.
4. **AnalysisAgent**: Merges financial data and suggests personalized BNPL plans.
5. **MainAgent**: Acts as the orchestrator of all sub-agents and provides the final response.

### Data Flow & State Graphs
- **StateGraph Mechanism:** A state machine approach ensures structured data flow between agents.
- **Internal States:** Each agent maintains a **TypedDict** state to track retrieved data.
- **LLM Prompting:** Agents feed structured prompts into an LLM to generate actionable BNPL suggestions.
- **Flow Summary:**
  - MainAgent receives user input → Calls sub-agents → Merges results → Calls AnalysisAgent → Generates final BNPL plan → Displays recommendations to the user.

---
## Conclusion & Future Work
### Current Status & Known Limitations
#### ✅ Current Status
- Successfully integrated multiple **LLM-powered agents** for personalized BNPL plans.
- Real-time financial data analysis, risk assessment, and installment customization.
- Local **Streamlit/Gradio UI** available for testing and demonstration.

#### ⚠ Known Limitations
- **Data Dependency:** Accuracy relies on high-quality, up-to-date financial data.
- **API Rate Limits:** External APIs (e.g., Google Custom Search) can cause delays.
- **LLM Variability:** Model output depends on prompt tuning and model parameters.
- **Security & Privacy:** Sensitive financial data needs stronger privacy measures.

### Potential Improvements
- **Enhanced Data Integration:** Automate real-time data feeds from multiple financial APIs.
- **Model Fine-Tuning:** Experiment with different **LLMs (GPT-4, Gemini)** and fine-tune prompts.
- **User Interface Enhancements:** Build an interactive UI with financial trend tracking dashboards.
- **Error Handling:** Implement caching and advanced error management for API failures.
- **Security Upgrades:** Strengthen encryption, anonymization, and compliance measures (e.g., GDPR).

### Next Steps
- **Beta Testing & Feedback:**
  - Deploy a prototype and collect real-world feedback.
  - Refine the AI models and UI based on user experience.
- **Scaling & Deployment:**
  - Use **Docker** for deployment across multiple environments.
  - Explore **cloud-based solutions** for scalability.
- **Feature Expansion:**
  - Introduce **real-time notifications** and adaptive incentives.
  - Expand to **multi-currency support** and broader financial markets.

---
## How to Run the Project
### Prerequisites
- Python 3.8+
- Streamlit or Gradio (for UI)
- OpenAI API or Google Generative AI access
- Required Python libraries (install via `requirements.txt`)

### Installation
```sh
# Clone the repository
git clone https://github.com/your-repo/AI-BNPL.git
cd AI-BNPL

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py 
```

### Configuration
- Set up API keys for **GOOGLE_API_KEY** and **TAVILY_API_KEY** in `.env`.
- Adjust model settings in `.env`.

---
## Contributing
We welcome contributions! To contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m "Added new feature"`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

---
## License
This project is licensed under the MIT License. See the LICENSE file for details.
