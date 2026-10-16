import google.generativeai as genai
import os
import json
from datetime import datetime
from typing import Dict, List

class GeminiAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Use the fastest free model that works
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        
        
    def analyze_contract(self, contract_text: str, contract_type: str = "General") -> Dict:
        """Main analysis function that orchestrates all analysis tasks"""
        
        # Step 1: Contract Type Classification
        contract_classification = self._classify_contract(contract_text)
        
        # Step 2: Extract entities and clauses
        entities = self._extract_entities(contract_text)
        
        # Step 3: Identify obligations, rights, and prohibitions
        obligations_analysis = self._analyze_obligations(contract_text)
        
        # Step 4: Risk assessment
        risk_assessment = self._assess_risks(contract_text)
        
        # Step 5: Generate simplified summary
        summary = self._generate_summary(contract_text)
        
        # Step 6: Identify unfavorable clauses
        unfavorable_clauses = self._identify_unfavorable_clauses(contract_text)
        
        # Step 7: Generate alternative suggestions
        alternatives = self._generate_alternatives(unfavorable_clauses)
        
        # Compile all results
        analysis_result = {
            "timestamp": datetime.now().isoformat(),
            "contract_type": contract_classification,
            "entities": entities,
            "obligations_analysis": obligations_analysis,
            "risk_assessment": risk_assessment,
            "summary": summary,
            "unfavorable_clauses": unfavorable_clauses,
            "suggested_alternatives": alternatives
        }
        
        return analysis_result
    
    def _classify_contract(self, contract_text: str) -> Dict:
        """Classify the type of contract"""
        prompt = f"""Analyze this contract and classify it into one of these categories:
- Employment Agreement
- Vendor Contract
- Lease Agreement
- Partnership Deed
- Service Contract
- Non-Disclosure Agreement (NDA)
- Purchase Agreement
- Other

Contract text:
{contract_text[:2000]}

Respond with ONLY a JSON object (no markdown, no backticks) containing:
{{
    "contract_type": "the main category",
    "sub_type": "more specific classification if applicable",
    "confidence": "high/medium/low"
}}"""

        try:
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            return {"contract_type": "Unknown", "sub_type": "Error", "confidence": "low", "error": str(e)}
    
    def _extract_entities(self, contract_text: str) -> Dict:
        """Extract named entities from the contract"""
        prompt = f"""Extract the following entities from this contract:
1. Parties (all parties involved with their roles)
2. Important Dates (effective date, termination date, renewal dates)
3. Financial Amounts (payment terms, penalties, deposits)
4. Jurisdiction (governing law, dispute resolution location)
5. Liabilities (who is liable for what)
6. Key Deliverables

Contract text:
{contract_text[:3000]}

Respond with ONLY a JSON object (no markdown, no backticks) with these keys: parties, dates, financial_terms, jurisdiction, liabilities, deliverables"""

        try:
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_obligations(self, contract_text: str) -> Dict:
        """Identify obligations, rights, and prohibitions"""
        prompt = f"""Analyze this contract and categorize clauses into:
1. OBLIGATIONS (what parties MUST do)
2. RIGHTS (what parties CAN do)
3. PROHIBITIONS (what parties CANNOT do)

Contract text:
{contract_text[:3000]}

Respond with ONLY a JSON object (no markdown, no backticks) with keys: obligations, rights, prohibitions. Each should be a list of objects with "party", "clause", and "description"."""

        try:
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            return {"obligations": [], "rights": [], "prohibitions": [], "error": str(e)}
    
    def _assess_risks(self, contract_text: str) -> Dict:
        """Perform comprehensive risk assessment"""
        prompt = f"""Perform a detailed risk assessment of this contract. Identify:

1. HIGH RISK clauses (could cause significant harm)
2. MEDIUM RISK clauses (potentially problematic)
3. LOW RISK clauses (minor concerns)

Contract text:
{contract_text[:4000]}

Respond with ONLY JSON (no markdown, no backticks):
{{
    "overall_risk_score": "number 0-100",
    "overall_risk_level": "Low/Medium/High/Critical",
    "high_risk_clauses": ["list of clauses with explanations"],
    "medium_risk_clauses": ["list of clauses"],
    "low_risk_clauses": ["list of clauses"],
    "critical_issues": ["list of must-address items"],
    "compliance_concerns": ["potential legal compliance issues for Indian SMEs"]
}}"""

        try:
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            return {
                "overall_risk_score": "0",
                "overall_risk_level": "Unknown",
                "high_risk_clauses": [],
                "medium_risk_clauses": [],
                "low_risk_clauses": [],
                "critical_issues": [],
                "compliance_concerns": [],
                "error": str(e)
            }
    
    def _generate_summary(self, contract_text: str) -> str:
        """Generate a simplified summary in plain language"""
        prompt = f"""Create a simple summary of this contract for a small business owner. 

Cover:
1. What is this contract about?
2. Who are the parties?
3. What are the main obligations?
4. Key financial terms?
5. Duration?
6. Termination?
7. Main risks?

Keep it concise.

Contract text:
{contract_text[:4000]}"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _identify_unfavorable_clauses(self, contract_text: str) -> List[Dict]:
        """Identify clauses that are unfavorable to the user"""
        prompt = f"""Identify all unfavorable clauses in this contract for a small/medium business. 

For each clause provide:
1. The clause text (or summary)
2. Why it's problematic
3. Potential consequences
4. Severity (Low/Medium/High)

Contract text:
{contract_text[:4000]}

Respond with ONLY a JSON array (no markdown, no backticks) of unfavorable clauses."""

        try:
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            return result if isinstance(result, list) else result.get("unfavorable_clauses", [])
        except Exception as e:
            return []
    
    def _generate_alternatives(self, unfavorable_clauses: List[Dict]) -> List[Dict]:
        """Generate alternative clause suggestions"""
        if not unfavorable_clauses:
            return []
        
        clauses_summary = json.dumps(unfavorable_clauses[:5], indent=2)
        
        prompt = f"""For these unfavorable contract clauses, suggest better alternatives:

{clauses_summary}

For each clause, provide:
1. Recommended alternative wording
2. Why this alternative is better
3. Negotiation strategy

Respond with ONLY a JSON array (no markdown, no backticks) matching the input clauses."""

        try:
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            return result if isinstance(result, list) else result.get("alternatives", [])
        except Exception as e:
            return []
    
    def _parse_json_response(self, response_text: str) -> Dict:
        """Parse JSON from Gemini's response"""
        cleaned = response_text.strip()
        
        # Remove markdown code blocks if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"raw_response": response_text, "parse_error": True}
    
    def generate_clause_explanation(self, clause_text: str) -> str:
        """Generate plain language explanation for a specific clause"""
        prompt = f"""Explain this contract clause in simple language:

"{clause_text}"

Explain:
1. What does this mean?
2. Your obligations?
3. Your rights?
4. What to watch out for?"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error explaining clause: {str(e)}"