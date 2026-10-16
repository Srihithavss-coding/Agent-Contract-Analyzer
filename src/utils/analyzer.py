import anthropic
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple
import re

class ContractAnalyzer:
    def __init__(self, api_key: str):
        self.client = anthropic.Client(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"        
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

Respond with a JSON object containing:
{{
    "contract_type": "the main category",
    "sub_type": "more specific classification if applicable",
    "confidence": "high/medium/low"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_json_response(response.content[0].text)
    
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

Respond with a JSON object with these keys: parties, dates, financial_terms, jurisdiction, liabilities, deliverables"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_json_response(response.content[0].text)
    
    def _analyze_obligations(self, contract_text: str) -> Dict:
        """Identify obligations, rights, and prohibitions"""
        prompt = f"""Analyze this contract and categorize clauses into:
1. OBLIGATIONS (what parties MUST do)
2. RIGHTS (what parties CAN do)
3. PROHIBITIONS (what parties CANNOT do)

For each category, list the specific clauses with clause numbers if available.

Contract text:
{contract_text[:3000]}

Respond with a JSON object with keys: obligations, rights, prohibitions. Each should be a list of objects with "party", "clause", and "description"."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_json_response(response.content[0].text)
    
    def _assess_risks(self, contract_text: str) -> Dict:
        """Perform comprehensive risk assessment"""
        prompt = f"""Perform a detailed risk assessment of this contract. Identify:

1. HIGH RISK clauses (could cause significant business/financial harm):
   - Unlimited liability
   - Harsh penalty clauses
   - Unilateral termination by other party
   - Unfavorable payment terms
   - Excessive lock-in periods
   - Broad non-compete clauses
   - IP transfer without compensation

2. MEDIUM RISK clauses (potentially problematic):
   - Auto-renewal without notice
   - Ambiguous deliverables
   - Unclear jurisdiction
   - One-sided indemnity

3. LOW RISK clauses (minor concerns):
   - Standard confidentiality
   - Reasonable notice periods

Contract text:
{contract_text[:4000]}

Respond with JSON:
{{
    "overall_risk_score": "number 0-100",
    "overall_risk_level": "Low/Medium/High/Critical",
    "high_risk_clauses": [list of clauses with explanations],
    "medium_risk_clauses": [list of clauses],
    "low_risk_clauses": [list of clauses],
    "critical_issues": [list of must-address items],
    "compliance_concerns": [potential legal compliance issues for Indian SMEs]
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_json_response(response.content[0].text)
    
    def _generate_summary(self, contract_text: str) -> str:
        """Generate a simplified summary in plain language"""
        prompt = f"""Create a simple, easy-to-understand summary of this contract for a small business owner who may not have legal expertise. 

Use plain business language. Cover:
1. What is this contract about?
2. Who are the parties?
3. What are the main obligations?
4. What are the key financial terms?
5. How long does it last?
6. How can it be terminated?
7. What are the main risks?

Keep it concise but comprehensive.

Contract text:
{contract_text[:4000]}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def _identify_unfavorable_clauses(self, contract_text: str) -> List[Dict]:
        """Identify clauses that are unfavorable to the user"""
        prompt = f"""Identify all clauses in this contract that could be unfavorable or disadvantageous to a small/medium business. 

For each unfavorable clause, provide:
1. The clause text (or summary)
2. Why it's problematic
3. Potential consequences
4. Severity (Low/Medium/High)

Contract text:
{contract_text[:4000]}

Respond with a JSON array of unfavorable clauses."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = self._parse_json_response(response.content[0].text)
        return result if isinstance(result, list) else result.get("unfavorable_clauses", [])
    
    def _generate_alternatives(self, unfavorable_clauses: List[Dict]) -> List[Dict]:
        """Generate alternative clause suggestions"""
        if not unfavorable_clauses:
            return []
        
        clauses_summary = json.dumps(unfavorable_clauses[:5], indent=2)  # Limit to first 5
        
        prompt = f"""For these unfavorable contract clauses, suggest better alternatives that would be more favorable to a small business:

{clauses_summary}

For each clause, provide:
1. Recommended alternative wording
2. Why this alternative is better
3. Negotiation strategy/talking points

Respond with a JSON array matching the input clauses."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = self._parse_json_response(response.content[0].text)
        return result if isinstance(result, list) else result.get("alternatives", [])
    
    def _parse_json_response(self, response_text: str) -> Dict:
        """Parse JSON from Claude's response, handling markdown code blocks"""
        # Remove markdown code blocks if present
        cleaned = response_text.strip()
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
            # If JSON parsing fails, return the text wrapped in an object
            return {"raw_response": response_text, "parse_error": True}
    
    def generate_clause_explanation(self, clause_text: str) -> str:
        """Generate plain language explanation for a specific clause"""
        prompt = f"""Explain this contract clause in simple, plain language that a small business owner would understand:

"{clause_text}"

Explain:
1. What does this clause mean?
2. What are your obligations?
3. What are your rights?
4. What should you watch out for?"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text