import streamlit as st
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.gemini_analyzer import GeminiAnalyzer as ContractAnalyzer
from src.utils.document_processor import DocumentProcessor
from src.utils.report_generator import ReportGenerator
from src.utils.templates import ContractTemplates

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f2937;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .risk-medium {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .risk-low {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'contract_text' not in st.session_state:
    st.session_state.contract_text = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv('ANTHROPIC_API_KEY', '')

def main():
    # Header
    st.markdown('<p class="main-header">📄 Contract Analysis & Risk Assessment Bot</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered legal assistant for small and medium businesses</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "Google Gemini API Key (FREE)",
            value=st.session_state.api_key,
            type="password",
            help="Enter your FREE Google Gemini API key. Get one at https://aistudio.google.com/app/apikey"
        )
        
        if api_key:
            st.session_state.api_key = api_key
        
        st.divider()
        
        st.header("📚 About")
        st.markdown("""
        This tool helps you:
        - ✅ Understand complex contracts
        - ⚠️ Identify legal risks
        - 💡 Get actionable advice
        - 📝 Generate standard templates
        - 📊 Create analysis reports
        """)
        
        st.divider()
        
        st.header("📄 Supported Formats")
        st.markdown("""
        - PDF (.pdf)
        - Word (.docx)
        - Text (.txt)
        """)
        
        st.divider()
        
        st.markdown("**Languages Supported:**")
        st.markdown("🇮🇳 English & Hindi")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📋 Contract Templates", "ℹ️ How to Use"])
    
    with tab1:
        upload_and_analyze_tab()
    
    with tab2:
        templates_tab()
    
    with tab3:
        how_to_use_tab()

def upload_and_analyze_tab():
    """Tab for uploading and analyzing contracts"""
    
    st.header("Upload Your Contract")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a contract file",
        type=['pdf', 'docx', 'txt'],
        help="Upload your contract in PDF, DOCX, or TXT format"
    )
    
    # Contract type selector
    contract_type = st.selectbox(
        "Contract Type (Optional)",
        ["Auto-detect", "Employment Agreement", "Vendor Contract", "Lease Agreement", 
         "Partnership Deed", "Service Contract", "NDA", "Other"]
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")
        
        # Extract text button
        if st.button("🔍 Extract Text from Document", type="secondary"):
            with st.spinner("Extracting text from document..."):
                try:
                    contract_text = DocumentProcessor.process_document(uploaded_file)
                    st.session_state.contract_text = contract_text
                    
                    # Detect language
                    language = DocumentProcessor.detect_language(contract_text)
                    
                    st.success(f"✅ Text extracted successfully! Detected language: {language.title()}")
                    
                    # Show preview
                    with st.expander("📄 View Extracted Text (First 1000 characters)"):
                        st.text(contract_text[:1000] + "..." if len(contract_text) > 1000 else contract_text)
                    
                except Exception as e:
                    st.error(f"❌ Error extracting text: {str(e)}")
        
        # Analyze button
        if st.session_state.contract_text and st.button("🤖 Analyze Contract with AI", type="primary"):
            if not st.session_state.api_key:
                st.error("⚠️ Please enter your Anthropic API key in the sidebar first!")
                return
            
            with st.spinner("🔄 Analyzing contract... This may take 1-2 minutes..."):
                try:
                    # Initialize analyzer
                    analyzer = ContractAnalyzer(st.session_state.api_key)
                    
                    # Perform analysis
                    analysis_result = analyzer.analyze_contract(
                        st.session_state.contract_text,
                        contract_type if contract_type != "Auto-detect" else "General"
                    )
                    
                    st.session_state.analysis_result = analysis_result
                    
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.info("Please check your API key and try again.")
    
    # Display results if available
    if st.session_state.analysis_result:
        display_analysis_results(st.session_state.analysis_result)

def display_analysis_results(analysis_result):
    """Display the analysis results in organized sections"""
    
    st.divider()
    st.header("📊 Analysis Results")
    
    # Create tabs for different sections
    result_tabs = st.tabs([
        "📝 Summary", 
        "⚠️ Risk Assessment", 
        "🔍 Key Entities",
        "📋 Obligations",
        "⚡ Unfavorable Clauses",
        "📄 Export Report"
    ])
    
    # Summary Tab
    with result_tabs[0]:
        st.subheader("Executive Summary")
        
        # Contract classification
        contract_type = analysis_result.get('contract_type', {})
        if isinstance(contract_type, dict):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Contract Type", contract_type.get('contract_type', 'N/A'))
            with col2:
                st.metric("Sub-type", contract_type.get('sub_type', 'N/A'))
            with col3:
                st.metric("Confidence", contract_type.get('confidence', 'N/A'))
        
        st.divider()
        
        # Summary text
        summary = analysis_result.get('summary', 'No summary available')
        st.markdown(f"<div class='info-box'>{summary}</div>", unsafe_allow_html=True)
    
    # Risk Assessment Tab
    with result_tabs[1]:
        st.subheader("Risk Assessment")
        
        risk_assessment = analysis_result.get('risk_assessment', {})
        
        if isinstance(risk_assessment, dict):
            # Overall risk score
            col1, col2 = st.columns(2)
            with col1:
                overall_score = risk_assessment.get('overall_risk_score', 'N/A')
                st.metric("Overall Risk Score", f"{overall_score}/100")
            with col2:
                overall_level = risk_assessment.get('overall_risk_level', 'N/A')
                st.metric("Risk Level", overall_level)
            
            st.divider()
            
            # Critical Issues
            critical_issues = risk_assessment.get('critical_issues', [])
            if critical_issues:
                st.markdown("### 🚨 Critical Issues")
                for issue in critical_issues:
                    st.markdown(f"<div class='risk-high'>❗ {issue}</div>", unsafe_allow_html=True)
            
            # High Risk Clauses
            high_risk = risk_assessment.get('high_risk_clauses', [])
            if high_risk:
                st.markdown("### 🔴 High Risk Clauses")
                for clause in high_risk:
                    if isinstance(clause, dict):
                        clause_text = clause.get('clause', clause.get('description', str(clause)))
                    else:
                        clause_text = str(clause)
                    st.markdown(f"<div class='risk-high'>{clause_text}</div>", unsafe_allow_html=True)
            
            # Medium Risk Clauses
            medium_risk = risk_assessment.get('medium_risk_clauses', [])
            if medium_risk:
                st.markdown("### 🟡 Medium Risk Clauses")
                for clause in medium_risk:
                    if isinstance(clause, dict):
                        clause_text = clause.get('clause', clause.get('description', str(clause)))
                    else:
                        clause_text = str(clause)
                    st.markdown(f"<div class='risk-medium'>{clause_text}</div>", unsafe_allow_html=True)
            
            # Low Risk Clauses
            low_risk = risk_assessment.get('low_risk_clauses', [])
            if low_risk:
                st.markdown("### 🟢 Low Risk Clauses")
                for clause in low_risk[:3]:  # Show only first 3
                    if isinstance(clause, dict):
                        clause_text = clause.get('clause', clause.get('description', str(clause)))
                    else:
                        clause_text = str(clause)
                    st.markdown(f"<div class='risk-low'>{clause_text}</div>", unsafe_allow_html=True)
    
    # Key Entities Tab
    with result_tabs[2]:
        st.subheader("Key Contract Entities")
        
        entities = analysis_result.get('entities', {})
        if isinstance(entities, dict):
            for key, value in entities.items():
                if value:
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    if isinstance(value, list):
                        for item in value:
                            st.markdown(f"- {item}")
                    else:
                        st.markdown(f"{value}")
                    st.divider()
    
    # Obligations Tab
    with result_tabs[3]:
        st.subheader("Obligations, Rights & Prohibitions")
        
        obligations_analysis = analysis_result.get('obligations_analysis', {})
        
        if isinstance(obligations_analysis, dict):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### ✅ Obligations")
                obligations = obligations_analysis.get('obligations', [])
                for item in obligations:
                    if isinstance(item, dict):
                        party = item.get('party', 'N/A')
                        desc = item.get('description', item.get('clause', 'N/A'))
                        st.markdown(f"**[{party}]** {desc}")
                    else:
                        st.markdown(f"- {item}")
            
            with col2:
                st.markdown("#### 🎯 Rights")
                rights = obligations_analysis.get('rights', [])
                for item in rights:
                    if isinstance(item, dict):
                        party = item.get('party', 'N/A')
                        desc = item.get('description', item.get('clause', 'N/A'))
                        st.markdown(f"**[{party}]** {desc}")
                    else:
                        st.markdown(f"- {item}")
            
            with col3:
                st.markdown("#### 🚫 Prohibitions")
                prohibitions = obligations_analysis.get('prohibitions', [])
                for item in prohibitions:
                    if isinstance(item, dict):
                        party = item.get('party', 'N/A')
                        desc = item.get('description', item.get('clause', 'N/A'))
                        st.markdown(f"**[{party}]** {desc}")
                    else:
                        st.markdown(f"- {item}")
    
    # Unfavorable Clauses Tab
    with result_tabs[4]:
        st.subheader("Unfavorable Clauses & Recommendations")
        
        unfavorable = analysis_result.get('unfavorable_clauses', [])
        alternatives = analysis_result.get('suggested_alternatives', [])
        
        if unfavorable:
            for idx, clause in enumerate(unfavorable, 1):
                if isinstance(clause, dict):
                    with st.expander(f"Issue {idx}: {clause.get('clause', 'Clause')[:100]}..."):
                        st.markdown(f"**Clause:** {clause.get('clause', clause.get('description', 'N/A'))}")
                        st.markdown(f"**Problem:** {clause.get('why_problematic', clause.get('problem', 'N/A'))}")
                        st.markdown(f"**Severity:** {clause.get('severity', 'N/A')}")
                        
                        if idx <= len(alternatives) and isinstance(alternatives[idx-1], dict):
                            alt = alternatives[idx-1]
                            st.divider()
                            st.markdown("**💡 Recommended Alternative:**")
                            st.info(alt.get('alternative', alt.get('recommended_alternative', 'N/A')))
                            
                            strategy = alt.get('negotiation_strategy', alt.get('why_better', ''))
                            if strategy:
                                st.markdown("**📊 Negotiation Strategy:**")
                                st.success(strategy)
        else:
            st.info("No major unfavorable clauses identified.")
    
    # Export Report Tab
    with result_tabs[5]:
        st.subheader("Export Analysis Report")
        
        st.markdown("""
        Download a comprehensive PDF report of the contract analysis for:
        - Legal consultation
        - Record keeping
        - Team sharing
        """)
        
        if st.button("📥 Generate PDF Report", type="primary"):
            with st.spinner("Generating PDF report..."):
                try:
                    # Create output directory if it doesn't exist
                    output_dir = "outputs"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Generate report
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = f"{output_dir}/contract_analysis_{timestamp}.pdf"
                    
                    ReportGenerator.generate_analysis_report(
                        analysis_result,
                        st.session_state.contract_text,
                        output_path
                    )
                    
                    # Provide download button
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="📄 Download PDF Report",
                            data=file,
                            file_name=f"contract_analysis_{timestamp}.pdf",
                            mime="application/pdf"
                        )
                    
                    st.success("✅ PDF report generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")

def templates_tab():
    """Tab for contract templates"""
    
    st.header("📋 Standard Contract Templates")
    
    st.markdown("""
    Select a template below to view and download standardized, SME-friendly contract templates.
    These templates are designed to be fair and balanced for small and medium businesses.
    """)
    
    templates = ContractTemplates.get_available_templates()
    
    selected_template = st.selectbox(
        "Choose a template:",
        options=list(templates.keys())
    )
    
    if selected_template:
        template_key = templates[selected_template]
        template_text = ContractTemplates.get_template(template_key)
        
        st.subheader(f"{selected_template} Template")
        
        # Display template
        st.text_area(
            "Template Content",
            value=template_text,
            height=400,
            help="You can copy this template and customize it for your needs"
        )
        
        # Download button
        st.download_button(
            label="📥 Download Template",
            data=template_text,
            file_name=f"{template_key}_template.txt",
            mime="text/plain"
        )
        
        st.info("💡 **Note:** These templates are starting points. Always customize them for your specific situation and consider having them reviewed by a legal professional.")

def how_to_use_tab():
    """Tab with usage instructions"""
    
    st.header("ℹ️ How to Use This Tool")
    
    st.markdown("""
    ### Getting Started
    
    #### 1. Set Up Your API Key
    - Get an API key from [Anthropic Console](https://console.anthropic.com/)
    - Enter it in the sidebar under "Settings"
    
    #### 2. Upload Your Contract
    - Click the "Upload & Analyze" tab
    - Upload your contract (PDF, DOCX, or TXT)
    - Select the contract type if known
    
    #### 3. Analyze
    - Click "Extract Text from Document" to preview the content
    - Click "Analyze Contract with AI" to start the analysis
    - Wait 1-2 minutes for comprehensive analysis
    
    #### 4. Review Results
    - Navigate through different tabs to review:
        - **Summary**: Quick overview of the contract
        - **Risk Assessment**: Identification of potential risks
        - **Key Entities**: Parties, dates, amounts, etc.
        - **Obligations**: What you must, can, and cannot do
        - **Unfavorable Clauses**: Problematic terms with alternatives
        - **Export Report**: Download PDF for legal consultation
    
    ### Features
    
    ✅ **Contract Type Classification** - Automatically identifies contract type
    
    ⚠️ **Risk Scoring** - Comprehensive risk assessment with severity levels
    
    🔍 **Entity Extraction** - Identifies parties, dates, amounts, and key terms
    
    📋 **Clause Analysis** - Breaks down obligations, rights, and prohibitions
    
    💡 **Alternative Suggestions** - Recommends better clause alternatives
    
    📄 **PDF Reports** - Generate professional reports for legal review
    
    📚 **Contract Templates** - Access standardized SME-friendly templates
    
    ### Supported Languages
    
    - 🇬🇧 English
    - 🇮🇳 Hindi (with English output)
    
    ### Important Notes
    
    ⚠️ **This tool provides analysis and suggestions, not legal advice.**
    
    🔒 **Your documents are processed securely and not stored.**
    
    👨‍⚖️ **Always consult with a qualified lawyer for final decisions.**
    
    ### Tips for Best Results
    
    1. **Upload clear, text-based PDFs** - Scanned documents may have lower accuracy
    2. **Provide complete contracts** - Partial documents may miss important clauses
    3. **Review all suggestions carefully** - AI analysis should complement human judgment
    4. **Keep reports for reference** - Export PDFs for your records
    
    ### Need Help?
    
    If you encounter any issues:
    - Check that your API key is valid
    - Ensure your document is in a supported format
    - Verify the file is not corrupted
    - Try with a smaller document first
    
    ### Privacy & Security
    
    - Documents are processed in real-time
    - No data is permanently stored
    - Analysis happens through secure API calls
    - Your contracts remain confidential
    """)

if __name__ == "__main__":
    main()