from crewai import Task
from agents import financial_analyst

def create_analysis_task(document_text: str, query: str):
    # Prevent token overflow
    document_text = document_text[:4000]

    return Task(
        description=f"""
You are a senior financial analyst.

Analyze the financial data below:

{document_text}

User Query: {query}

Rules:
- Do NOT fabricate or assume missing data.
- If data is not provided, explicitly say "Not Provided".
- Perform calculations only if sufficient data is available.
- Keep output strictly valid JSON.

Return strictly valid JSON in this format:

{{
  "revenue_summary": {{
      "revenue": "",
      "growth_rate": "",
      "revenue_mix": ""
  }},
  "profitability": {{
      "net_profit": "",
      "gross_margin": "",
      "operating_margin": ""
  }},
  "risk_factors": [],
  "investment_outlook": "",
  "confidence_score": ""
}}
""",
        expected_output="Strict JSON financial analysis",
        agent=financial_analyst
    )