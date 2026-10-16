from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime
import json

class ReportGenerator:
    """Generate PDF reports for contract analysis"""
    
    @staticmethod
    def generate_analysis_report(analysis_result: dict, contract_text: str, output_path: str):
        """Generate a comprehensive PDF report"""
        
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=6,
            spaceBefore=6
        )
        
        normal_style = styles['Normal']
        
        # Title
        elements.append(Paragraph("Contract Analysis Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Report metadata
        timestamp = analysis_result.get('timestamp', datetime.now().isoformat())
        elements.append(Paragraph(f"Generated on: {timestamp}", normal_style))
        elements.append(Spacer(1, 20))
        
        # 1. Contract Classification
        elements.append(Paragraph("1. Contract Classification", heading_style))
        contract_type = analysis_result.get('contract_type', {})
        if isinstance(contract_type, dict):
            elements.append(Paragraph(f"Type: {contract_type.get('contract_type', 'N/A')}", normal_style))
            elements.append(Paragraph(f"Sub-type: {contract_type.get('sub_type', 'N/A')}", normal_style))
            elements.append(Paragraph(f"Confidence: {contract_type.get('confidence', 'N/A')}", normal_style))
        elements.append(Spacer(1, 12))
        
        # 2. Executive Summary
        elements.append(Paragraph("2. Executive Summary", heading_style))
        summary = analysis_result.get('summary', 'No summary available')
        # Split summary into paragraphs for better formatting
        summary_paragraphs = summary.split('\n\n')
        for para in summary_paragraphs:
            if para.strip():
                elements.append(Paragraph(para.strip(), normal_style))
                elements.append(Spacer(1, 6))
        elements.append(Spacer(1, 12))
        
        # 3. Risk Assessment
        elements.append(Paragraph("3. Risk Assessment", heading_style))
        risk_assessment = analysis_result.get('risk_assessment', {})
        
        if isinstance(risk_assessment, dict):
            # Overall Risk Score
            overall_score = risk_assessment.get('overall_risk_score', 'N/A')
            overall_level = risk_assessment.get('overall_risk_level', 'N/A')
            elements.append(Paragraph(f"<b>Overall Risk Score:</b> {overall_score}/100", normal_style))
            elements.append(Paragraph(f"<b>Risk Level:</b> {overall_level}", normal_style))
            elements.append(Spacer(1, 12))
            
            # High Risk Clauses
            high_risk = risk_assessment.get('high_risk_clauses', [])
            if high_risk:
                elements.append(Paragraph("High Risk Clauses:", subheading_style))
                for idx, clause in enumerate(high_risk, 1):
                    if isinstance(clause, dict):
                        clause_text = clause.get('clause', clause.get('description', str(clause)))
                    else:
                        clause_text = str(clause)
                    elements.append(Paragraph(f"{idx}. {clause_text}", normal_style))
                    elements.append(Spacer(1, 4))
                elements.append(Spacer(1, 12))
            
            # Medium Risk Clauses
            medium_risk = risk_assessment.get('medium_risk_clauses', [])
            if medium_risk:
                elements.append(Paragraph("Medium Risk Clauses:", subheading_style))
                for idx, clause in enumerate(medium_risk, 1):
                    if isinstance(clause, dict):
                        clause_text = clause.get('clause', clause.get('description', str(clause)))
                    else:
                        clause_text = str(clause)
                    elements.append(Paragraph(f"{idx}. {clause_text}", normal_style))
                    elements.append(Spacer(1, 4))
                elements.append(Spacer(1, 12))
            
            # Critical Issues
            critical = risk_assessment.get('critical_issues', [])
            if critical:
                elements.append(Paragraph("Critical Issues to Address:", subheading_style))
                for idx, issue in enumerate(critical, 1):
                    elements.append(Paragraph(f"{idx}. {issue}", normal_style))
                    elements.append(Spacer(1, 4))
                elements.append(Spacer(1, 12))
        
        # 4. Key Entities
        elements.append(Paragraph("4. Key Contract Entities", heading_style))
        entities = analysis_result.get('entities', {})
        if isinstance(entities, dict):
            for key, value in entities.items():
                if value:
                    elements.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b>", subheading_style))
                    if isinstance(value, list):
                        for item in value:
                            elements.append(Paragraph(f"• {item}", normal_style))
                    else:
                        elements.append(Paragraph(str(value), normal_style))
                    elements.append(Spacer(1, 6))
        elements.append(Spacer(1, 12))
        
        # 5. Unfavorable Clauses
        elements.append(PageBreak())
        elements.append(Paragraph("5. Unfavorable Clauses & Recommendations", heading_style))
        unfavorable = analysis_result.get('unfavorable_clauses', [])
        alternatives = analysis_result.get('suggested_alternatives', [])
        
        if unfavorable:
            for idx, clause in enumerate(unfavorable, 1):
                if isinstance(clause, dict):
                    elements.append(Paragraph(f"<b>Issue {idx}:</b>", subheading_style))
                    
                    clause_text = clause.get('clause', clause.get('description', 'N/A'))
                    elements.append(Paragraph(f"Clause: {clause_text}", normal_style))
                    
                    problem = clause.get('why_problematic', clause.get('problem', ''))
                    if problem:
                        elements.append(Paragraph(f"Problem: {problem}", normal_style))
                    
                    severity = clause.get('severity', 'N/A')
                    elements.append(Paragraph(f"Severity: {severity}", normal_style))
                    
                    # Add alternative if available
                    if idx <= len(alternatives) and isinstance(alternatives[idx-1], dict):
                        alt = alternatives[idx-1]
                        alt_text = alt.get('alternative', alt.get('recommended_alternative', ''))
                        if alt_text:
                            elements.append(Paragraph(f"<b>Recommended Alternative:</b> {alt_text}", normal_style))
                    
                    elements.append(Spacer(1, 12))
        
        # 6. Obligations Analysis
        elements.append(PageBreak())
        elements.append(Paragraph("6. Obligations, Rights & Prohibitions", heading_style))
        obligations_analysis = analysis_result.get('obligations_analysis', {})
        
        if isinstance(obligations_analysis, dict):
            for category in ['obligations', 'rights', 'prohibitions']:
                items = obligations_analysis.get(category, [])
                if items:
                    elements.append(Paragraph(f"<b>{category.title()}:</b>", subheading_style))
                    for item in items:
                        if isinstance(item, dict):
                            party = item.get('party', 'N/A')
                            desc = item.get('description', item.get('clause', 'N/A'))
                            elements.append(Paragraph(f"• [{party}] {desc}", normal_style))
                        else:
                            elements.append(Paragraph(f"• {item}", normal_style))
                        elements.append(Spacer(1, 4))
                    elements.append(Spacer(1, 12))
        
        # Footer note
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<i>Note: This analysis is for informational purposes only and does not constitute legal advice. Please consult with a qualified legal professional before making any decisions based on this report.</i>", normal_style))
        
        # Build PDF
        doc.build(elements)
        
        return output_path