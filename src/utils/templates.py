from typing import Dict

class ContractTemplates:
    """Generate standardized SME-friendly contract templates"""
    
    @staticmethod
    def get_template(contract_type: str) -> str:
        """Get a template based on contract type"""
        templates = {
            "service_contract": ContractTemplates.service_contract_template(),
            "vendor_contract": ContractTemplates.vendor_contract_template(),
            "employment_agreement": ContractTemplates.employment_agreement_template(),
            "nda": ContractTemplates.nda_template(),
            "partnership_deed": ContractTemplates.partnership_deed_template(),
        }
        
        return templates.get(contract_type.lower().replace(" ", "_"), 
                            ContractTemplates.general_template())
    
    @staticmethod
    def service_contract_template() -> str:
        return """
SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into on [DATE] ("Effective Date")

BETWEEN:

1. [YOUR COMPANY NAME], a company registered under [Registration Details]
   Having its registered office at [ADDRESS] ("Service Provider")

AND

2. [CLIENT NAME], a company/individual
   Having its address at [CLIENT ADDRESS] ("Client")

1. SCOPE OF SERVICES
The Service Provider agrees to provide the following services:
[DESCRIBE SERVICES IN DETAIL]

2. TERM
This Agreement shall commence on [START DATE] and continue until [END DATE], 
unless terminated earlier in accordance with the terms herein.

3. PAYMENT TERMS
3.1 Total Fees: INR [AMOUNT]
3.2 Payment Schedule: [MILESTONE-BASED/MONTHLY/UPON COMPLETION]
3.3 Payment shall be made within [NUMBER] days of invoice
3.4 Late payment will attract interest at [RATE]% per month

4. DELIVERABLES
The Service Provider shall deliver:
[LIST DELIVERABLES WITH TIMELINE]

5. INTELLECTUAL PROPERTY
5.1 All intellectual property created during this engagement shall belong to [CLIENT/SERVICE PROVIDER]
5.2 Pre-existing IP of Service Provider remains with Service Provider

6. CONFIDENTIALITY
Both parties agree to keep confidential information private and not disclose to third parties.

7. TERMINATION
7.1 Either party may terminate with [NUMBER] days written notice
7.2 Client may terminate immediately for breach with full payment for work completed
7.3 Service Provider may terminate for non-payment after [NUMBER] days notice

8. LIABILITY
8.1 Service Provider's total liability is limited to the fees paid under this Agreement
8.2 Service Provider is not liable for indirect or consequential damages

9. GOVERNING LAW
This Agreement shall be governed by the laws of India.
Disputes shall be resolved through arbitration in [CITY].

10. GENERAL PROVISIONS
10.1 This Agreement constitutes the entire agreement
10.2 Modifications must be in writing and signed by both parties
10.3 Neither party may assign this Agreement without consent

SIGNED:

Service Provider: _________________ Date: _______
Name & Title:

Client: _________________ Date: _______
Name & Title:
"""

    @staticmethod
    def vendor_contract_template() -> str:
        return """
VENDOR SUPPLY AGREEMENT

This Agreement is made on [DATE]

BETWEEN:

1. [BUYER COMPANY NAME] ("Buyer")
   Address: [ADDRESS]

AND

2. [VENDOR NAME] ("Vendor")
   Address: [VENDOR ADDRESS]

1. SUPPLY OF GOODS/SERVICES
Vendor agrees to supply the following:
[DESCRIPTION OF GOODS/SERVICES]

2. PRICING
2.1 Unit Price: INR [AMOUNT] per [UNIT]
2.2 Total estimated value: INR [AMOUNT]
2.3 Prices are valid until [DATE]
2.4 Price revisions require 30 days notice and mutual agreement

3. DELIVERY TERMS
3.1 Delivery Location: [ADDRESS]
3.2 Delivery Schedule: [TIMELINE]
3.3 Vendor responsible for delivery costs unless specified otherwise
3.4 Risk passes to Buyer upon delivery and acceptance

4. QUALITY STANDARDS
4.1 Goods must meet specifications: [SPECIFICATIONS]
4.2 Buyer reserves right to inspect and reject non-conforming goods
4.3 Vendor shall replace rejected goods within [NUMBER] days

5. PAYMENT TERMS
5.1 Payment within [NUMBER] days of invoice and delivery
5.2 Payment method: [BANK TRANSFER/CHEQUE/OTHER]
5.3 Vendor to provide GST-compliant invoices

6. WARRANTIES
6.1 Vendor warrants goods are free from defects for [NUMBER] months
6.2 Vendor warrants title and right to sell the goods
6.3 Warranty does not cover misuse or normal wear and tear

7. TERM AND TERMINATION
7.1 Agreement valid for [DURATION]
7.2 Either party may terminate with [NUMBER] days notice
7.3 Immediate termination for material breach

8. LIMITATION OF LIABILITY
Total liability limited to the value of goods supplied in the preceding 3 months.

9. GOVERNING LAW
Indian law applies. Jurisdiction: [CITY] courts.

SIGNED:

Buyer: _________________ Date: _______

Vendor: _________________ Date: _______
"""

    @staticmethod
    def employment_agreement_template() -> str:
        return """
EMPLOYMENT AGREEMENT

Between [COMPANY NAME] ("Employer")
And [EMPLOYEE NAME] ("Employee")

Date: [DATE]

1. POSITION
Employee is hired as [JOB TITLE] in the [DEPARTMENT] department.

2. EMPLOYMENT START DATE
Employment commences on [START DATE].

3. PROBATION PERIOD
[NUMBER] months probation period. Either party may terminate with [NUMBER] days notice during probation.

4. COMPENSATION
4.1 Monthly Salary: INR [AMOUNT] (gross)
4.2 Payment on [DAY] of each month
4.3 Annual increment: Performance-based review in [MONTH]

5. BENEFITS
5.1 Provident Fund (PF) as per regulations
5.2 Employee State Insurance (ESI) if applicable
5.3 [NUMBER] days paid leave per year
5.4 [OTHER BENEFITS]

6. WORKING HOURS
6.1 [NUMBER] hours per week
6.2 Working days: [DAYS]
6.3 Overtime as per company policy

7. DUTIES AND RESPONSIBILITIES
[LIST KEY RESPONSIBILITIES]

8. CONFIDENTIALITY
Employee shall not disclose confidential company information during or after employment.

9. NON-COMPETE (if applicable)
Employee agrees not to work for direct competitors for [NUMBER] months after employment ends 
within [GEOGRAPHICAL AREA].

10. INTELLECTUAL PROPERTY
All work created during employment belongs to the Employer.

11. TERMINATION
11.1 Either party may terminate with [NUMBER] months notice
11.2 Company may terminate immediately for gross misconduct with no notice pay
11.3 Employee entitled to notice pay or payment in lieu

12. GOVERNING LAW
Governed by Indian employment laws and regulations.

AGREED:

Employer: _________________ Date: _______

Employee: _________________ Date: _______
"""

    @staticmethod
    def nda_template() -> str:
        return """
NON-DISCLOSURE AGREEMENT (NDA)

Date: [DATE]

BETWEEN:

Disclosing Party: [NAME]
Address: [ADDRESS]

AND

Receiving Party: [NAME]
Address: [ADDRESS]

1. PURPOSE
The parties wish to explore [BUSINESS OPPORTUNITY/PURPOSE] and will share confidential information.

2. CONFIDENTIAL INFORMATION
"Confidential Information" means all information disclosed by either party including:
- Business plans and strategies
- Financial information
- Technical data and know-how
- Customer lists and supplier information
- Trade secrets

Excludes information that:
- Is publicly available
- Was known before disclosure
- Is independently developed
- Is rightfully received from third parties

3. OBLIGATIONS
3.1 Receiving Party shall:
    - Keep information confidential
    - Use only for the stated purpose
    - Not disclose to third parties without written consent
    - Protect with same care as own confidential information

3.2 Return or destroy information upon request or termination

4. TERM
This Agreement remains in effect for [NUMBER] years from the date of disclosure.

5. NO LICENSE
This Agreement does not grant any license or rights to intellectual property.

6. REMEDIES
Breach may cause irreparable harm. Disclosing Party entitled to injunctive relief in addition to damages.

7. GOVERNING LAW
Indian law applies. Jurisdiction: [CITY].

SIGNED:

Disclosing Party: _________________ Date: _______

Receiving Party: _________________ Date: _______
"""

    @staticmethod
    def partnership_deed_template() -> str:
        return """
PARTNERSHIP DEED

This Partnership Deed is made on [DATE]

BETWEEN:

1. [PARTNER 1 NAME], residing at [ADDRESS] ("First Partner")
2. [PARTNER 2 NAME], residing at [ADDRESS] ("Second Partner")

1. FIRM NAME AND BUSINESS
1.1 Firm Name: [FIRM NAME]
1.2 Principal Place of Business: [ADDRESS]
1.3 Nature of Business: [DESCRIPTION]

2. COMMENCEMENT
Partnership commences on [START DATE].

3. DURATION
Partnership shall continue until [END DATE/UNTIL DISSOLVED].

4. CAPITAL CONTRIBUTION
Partner 1: INR [AMOUNT] ([PERCENTAGE]%)
Partner 2: INR [AMOUNT] ([PERCENTAGE]%)
Total Capital: INR [TOTAL]

5. PROFIT AND LOSS SHARING
Partner 1: [PERCENTAGE]%
Partner 2: [PERCENTAGE]%

6. DRAWINGS
Each partner may draw up to INR [AMOUNT] per month for personal expenses.

7. DUTIES AND RESPONSIBILITIES
[LIST DUTIES OF EACH PARTNER]

8. DECISION MAKING
8.1 Day-to-day decisions: Any partner
8.2 Major decisions: Unanimous consent required

9. ACCOUNTS
9.1 Financial year: [START DATE] to [END DATE]
9.2 Books maintained at principal place of business
9.3 Annual audit by chartered accountant

10. DISSOLUTION
By mutual consent of all partners or by court order.

11. GOVERNING LAW
Partnership governed by Indian Partnership Act, 1932.

SIGNED:

Partner 1: _________________ Date: _______

Partner 2: _________________ Date: _______
"""

    @staticmethod
    def general_template() -> str:
        return """
GENERAL AGREEMENT

This Agreement is made on [DATE]

BETWEEN:

Party A: [NAME AND DETAILS]

AND

Party B: [NAME AND DETAILS]

1. SCOPE
[Describe what the agreement covers]

2. OBLIGATIONS
Party A shall: [LIST OBLIGATIONS]
Party B shall: [LIST OBLIGATIONS]

3. TERM
Agreement effective from [START DATE] to [END DATE].

4. PAYMENT
[Details of payment/consideration]

5. TERMINATION
Either party may terminate with [NOTICE PERIOD] written notice.

6. GOVERNING LAW
Governed by Indian law.

SIGNED:

Party A: _________________ Date: _______

Party B: _________________ Date: _______
"""
    
    @staticmethod
    def get_available_templates() -> Dict[str, str]:
        """Return list of available templates"""
        return {
            "Service Contract": "service_contract",
            "Vendor/Supply Agreement": "vendor_contract",
            "Employment Agreement": "employment_agreement",
            "Non-Disclosure Agreement (NDA)": "nda",
            "Partnership Deed": "partnership_deed",
            "General Agreement": "general"
        }