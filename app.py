import streamlit as st
import os
import hashlib
import html
from dotenv import load_dotenv
from datetime import datetime
import sys
from streamlit.errors import StreamlitSecretNotFoundError

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.gemini_analyzer import GeminiAnalyzer as ContractAnalyzer
from src.utils.document_processor import DocumentProcessor
from src.utils.report_generator import ReportGenerator
from src.utils.templates import ContractTemplates
from src.utils.vector_store import (
    add_text_chunks,
    get_collection,
    search_similar_clauses,
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom application styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #172033;
        --muted: #64748b;
        --line: #e2e8f0;
        --surface: #ffffff;
        --canvas: #f5f7fb;
        --brand: #3157d5;
    }
    .stApp {
        background: radial-gradient(ellipse at 10% 0%, #eef2ff 0, transparent 38%),
                    var(--canvas);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1380px;
        padding: 2rem 2.25rem 4rem;
    }
    h1, h2, h3, h4, .main-header {
        font-family: 'Manrope', sans-serif !important;
        letter-spacing: -0.035em;
        color: var(--ink);
    }
    .main-header {
        font-size: clamp(2rem, 4vw, 3.15rem);
        line-height: 1.12;
        font-weight: 800;
        margin: 0 0 .55rem;
    }
    .sub-header {
        font-size: 1.08rem;
        color: var(--muted);
        margin: 0;
        max-width: 760px;
    }
    .hero-kicker {
        color: var(--brand);
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: .6rem;
    }
    .hero-rule {
        height: 1px;
        border: 0;
        margin: 1.65rem 0 2rem;
        background: linear-gradient(90deg, #c7d2fe, #e2e8f0 65%, transparent);
    }
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, .88);
        border-right: 1px solid var(--line);
    }
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: .55rem;
        border-bottom: 1px solid var(--line);
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        height: 3rem;
        padding: .5rem 1rem;
        color: var(--muted);
        font-weight: 600;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: var(--brand);
    }
    [data-testid="stFileUploader"], [data-testid="stExpander"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
    }
    .stButton > button, [data-testid="stDownloadButton"] button {
        border-radius: 10px;
        font-weight: 700;
        transition: transform .15s ease, box-shadow .15s ease;
    }
    .stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(49, 87, 213, .14);
    }
    .risk-metric {
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--surface);
        padding: 1rem 1.15rem;
        min-height: 104px;
        box-shadow: 0 5px 20px rgba(23, 32, 51, .045);
    }
    .risk-metric-label {
        color: var(--muted);
        font-size: .82rem;
        font-weight: 700;
        letter-spacing: .04em;
        text-transform: uppercase;
    }
    .risk-metric-value {
        font-family: 'Manrope', sans-serif;
        font-size: 2rem;
        line-height: 1.25;
        font-weight: 800;
        margin-top: .28rem;
    }
    .risk-metric.high { border-top: 4px solid #dc2626; }
    .risk-metric.high .risk-metric-value { color: #b91c1c; }
    .risk-metric.medium { border-top: 4px solid #d97706; }
    .risk-metric.medium .risk-metric-value { color: #b45309; }
    .risk-metric.low { border-top: 4px solid #059669; }
    .risk-metric.low .risk-metric-value { color: #047857; }
    .risk-table-wrap {
        overflow-x: auto;
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--surface);
        box-shadow: 0 5px 20px rgba(23, 32, 51, .04);
        margin-top: 1rem;
    }
    table.risk-table {
        width: 100%;
        border-collapse: collapse;
        font-size: .92rem;
    }
    .risk-table th {
        background: #f8fafc;
        color: #475569;
        font-size: .75rem;
        letter-spacing: .06em;
        text-align: left;
        text-transform: uppercase;
    }
    .risk-table th, .risk-table td {
        padding: .9rem 1rem;
        border-bottom: 1px solid #edf1f6;
        vertical-align: top;
    }
    .risk-table tr:last-child td { border-bottom: 0; }
    .risk-badge {
        display: inline-block;
        border-radius: 999px;
        padding: .22rem .62rem;
        font-size: .74rem;
        font-weight: 800;
        white-space: nowrap;
    }
    .risk-badge.high { color: #991b1b; background: #fee2e2; }
    .risk-badge.medium { color: #92400e; background: #fef3c7; }
    .risk-badge.low { color: #065f46; background: #d1fae5; }
    @media (max-width: 700px) {
        [data-testid="stAppViewContainer"] .main .block-container {
            padding: 1.25rem 1rem 3rem;
        }
    }
    .risk-high {
        background-color: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0.85rem;
        margin: 0.75rem 0;
    }
    .risk-medium {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.85rem;
        margin: 0.75rem 0;
    }
    .risk-low {
        background-color: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.85rem;
        margin: 0.75rem 0;
    }
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.85rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'contract_text' not in st.session_state:
    st.session_state.contract_text = None
if 'contract_chunks' not in st.session_state:
    st.session_state.contract_chunks = []
if 'contract_collection_name' not in st.session_state:
    st.session_state.contract_collection_name = None
if 'contract_file_digest' not in st.session_state:
    st.session_state.contract_file_digest = None
if 'clause_chat_history' not in st.session_state:
    st.session_state.clause_chat_history = []


def _get_chunk_heading(chunk):
    """Get a concise legal heading from a chunk, or use a general label."""
    return DocumentProcessor.get_chunk_heading(chunk)


def _get_configured_api_key():
    """Resolve a Gemini key from environment variables or Streamlit secrets."""
    for key_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        value = os.getenv(key_name, "").strip()
        if value:
            return value

    try:
        for key_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
            value = st.secrets.get(key_name, "")
            if isinstance(value, str) and value.strip():
                return value.strip()
    except StreamlitSecretNotFoundError:
        return None
    return None


def main():
    # Header
    st.markdown(
        '<div class="hero-kicker">AI-powered contract intelligence</div>'
        '<div class="main-header">Legal clarity, clause by clause.</div>'
        '<p class="sub-header">Explore obligations, retrieve the terms that matter, '
        'and surface contract risks with structured AI analysis.</p>'
        '<hr class="hero-rule">',
        unsafe_allow_html=True,
    )
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key = _get_configured_api_key()
        if api_key:
            st.success("🔒 API Key Securely Loaded")
        else:
            api_key = st.text_input(
                "Gemini API key",
                type="password",
                key="manual_gemini_api_key",
                help="Used for this session only. Get a key from Google AI Studio.",
            ).strip()
            st.caption(
                "For a persistent setup, configure GEMINI_API_KEY or GOOGLE_API_KEY "
                "in the environment or Streamlit secrets."
            )
        
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
        upload_and_analyze_tab(api_key)
    
    with tab2:
        templates_tab()
    
    with tab3:
        how_to_use_tab()

def upload_and_analyze_tab(api_key):
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
        file_bytes = uploaded_file.getvalue()
        file_digest = hashlib.sha256(
            uploaded_file.name.encode("utf-8") + b"\0" + file_bytes
        ).hexdigest()
        if st.session_state.contract_file_digest != file_digest:
            st.session_state.contract_file_digest = file_digest
            st.session_state.contract_text = None
            st.session_state.contract_chunks = []
            st.session_state.analysis_result = None
            st.session_state.clause_chat_history = []
            st.session_state.contract_collection_name = (
                f"contract_{file_digest[:24]}"
                if uploaded_file.name.lower().endswith(".pdf")
                else None
            )

        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")
        
        # Extract text button
        if st.button("🔍 Extract Text from Document", type="secondary"):
            with st.spinner("Extracting text from document..."):
                try:
                    uploaded_file.seek(0)
                    contract_text = DocumentProcessor.process_document(uploaded_file)
                    st.session_state.contract_text = contract_text
                    chunks = DocumentProcessor.chunk_text(contract_text)
                    st.session_state.contract_chunks = chunks

                    if (
                        uploaded_file.name.lower().endswith(".pdf")
                        and chunks
                    ):
                        collection = get_collection(
                            st.session_state.contract_collection_name
                        )
                        if collection.count() == 0:
                            headings = [_get_chunk_heading(chunk) for chunk in chunks]
                            add_text_chunks(
                                chunks,
                                headings,
                                uploaded_file.name,
                                collection,
                            )
                    
                    # Detect language
                    language = DocumentProcessor.detect_language(contract_text)
                    
                    st.success(f"✅ Text extracted successfully! Detected language: {language.title()}")
                    if uploaded_file.name.lower().endswith(".pdf"):
                        if chunks:
                            st.success(
                                f"✅ Indexed {len(chunks)} contract sections for clause search."
                            )
                        else:
                            st.warning(
                                "No searchable text sections were found in this PDF."
                            )
                    
                    # Show preview
                    with st.expander("📄 View Extracted Text (First 1000 characters)"):
                        st.text(contract_text[:1000] + "..." if len(contract_text) > 1000 else contract_text)
                    
                except Exception as e:
                    st.error(f"❌ Error extracting text: {str(e)}")
        
        # Analyze button
        if st.session_state.contract_text and st.button("🤖 Analyze Contract with AI", type="primary"):
            if not api_key:
                st.error("⚠️ Please enter your Google Gemini API key in the sidebar first!")
                return
            
            with st.spinner("🔄 Analyzing contract... This may take 1-2 minutes..."):
                try:
                    # Initialize analyzer
                    analyzer = ContractAnalyzer(api_key)
                    
                    # Perform analysis
                    analysis_result = analyzer.analyze_contract(
                        st.session_state.contract_text,
                        contract_type if contract_type != "Auto-detect" else "General"
                    )
                    analysis_result["structured_risk_assessment"] = (
                        analyzer.analyze_retrieved_chunks(
                            st.session_state.contract_chunks
                            or [st.session_state.contract_text]
                        )
                    )
                    
                    st.session_state.analysis_result = analysis_result
                    
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.info("Please check your API key and try again.")

        if (
            uploaded_file.name.lower().endswith(".pdf")
            and st.session_state.contract_text
            and st.session_state.contract_collection_name
        ):
            st.divider()
            st.subheader("💬 Ask About a Contract Clause")
            st.caption(
                "Ask a question to retrieve the most relevant clauses from this PDF."
            )

            for chat_entry in st.session_state.clause_chat_history:
                with st.chat_message("user"):
                    st.write(chat_entry["question"])
                with st.chat_message("assistant"):
                    if not chat_entry["results"]:
                        st.info("No matching clauses were found in this contract.")
                    for result in chat_entry["results"]:
                        st.markdown(f"**{result.get('heading') or 'Contract clause'}**")
                        st.write(result["text"])
                        st.caption(
                            f"Source: {result.get('source') or uploaded_file.name} "
                            f"· Semantic distance: {result.get('distance', 0):.3f}"
                        )

            question = st.chat_input(
                "What is our liability cap?",
                key="clause_search_question",
            )
            if question:
                try:
                    collection = get_collection(
                        st.session_state.contract_collection_name
                    )
                    results = search_similar_clauses(question, collection)
                    st.session_state.clause_chat_history.append(
                        {"question": question, "results": results}
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Clause search failed: {e}")
    
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
        structured_risks = analysis_result.get(
            "structured_risk_assessment",
            [],
        )
        if isinstance(structured_risks, list):
            st.markdown("### Clause-Level Risk Findings")
            risk_counts = {
                level: sum(
                    1
                    for item in structured_risks
                    if isinstance(item, dict) and item.get("risk_level") == level
                )
                for level in ("High", "Medium", "Low")
            }
            high_col, medium_col, low_col = st.columns(3)
            for column, level, style in (
                (high_col, "High", "high"),
                (medium_col, "Medium", "medium"),
                (low_col, "Low", "low"),
            ):
                column.markdown(
                    f"""<div class="risk-metric {style}">
<div class="risk-metric-label">{level} Risk</div>
<div class="risk-metric-value">{risk_counts[level]}</div>
</div>""",
                    unsafe_allow_html=True,
                )

            if structured_risks:
                table_rows = []
                for item in structured_risks:
                    if not isinstance(item, dict):
                        continue
                    risk_level = item.get("risk_level", "Low")
                    risk_style = {
                        "High": "high",
                        "Medium": "medium",
                        "Low": "low",
                    }.get(risk_level, "low")
                    table_rows.append(
                        "<tr>"
                        f"<td>{html.escape(str(item.get('clause_title', 'Clause')))}</td>"
                        f'<td><span class="risk-badge {risk_style}">'
                        f"{html.escape(str(risk_level))}</span></td>"
                        f"<td>{html.escape(str(item.get('identified_issue', '')))}</td>"
                        f"<td>{html.escape(str(item.get('recommended_action', '')))}</td>"
                        "</tr>"
                    )
                if table_rows:
                    st.markdown(
                        '<div class="risk-table-wrap"><table class="risk-table">'
                        "<thead><tr><th>Clause</th><th>Risk</th><th>Identified issue</th>"
                        "<th>Recommended action</th></tr></thead><tbody>"
                        + "".join(table_rows)
                        + "</tbody></table></div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No clause-level risks were identified in the analyzed sections.")

            st.divider()
        
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
    - Get a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
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

    #### 5. Ask About PDF Clauses
    - After extracting a PDF, use the clause chat box to search for relevant sections
    - Results are retrieved from a local ChromaDB collection for the current contract
    
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
    - Extracted PDF clauses are stored locally in the `chroma_db` directory for semantic search
    - Analysis happens through secure API calls
    - Your contracts remain confidential
    """)

if __name__ == "__main__":
    main()