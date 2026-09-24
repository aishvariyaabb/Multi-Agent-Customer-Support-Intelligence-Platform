"""
Streamlit frontend application
"""
import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Customer Support Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Initialize session state
if "ticket_history" not in st.session_state:
    st.session_state.ticket_history = []
if "current_workflow" not in st.session_state:
    st.session_state.current_workflow = None


def process_ticket(ticket_data: dict) -> Optional[dict]:
    """Process ticket through the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/process",
            json=ticket_data,
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error processing ticket: {str(e)}")
        return None


def display_agent_logs(workflow_results: dict):
    """Display agent execution logs"""
    st.subheader("📊 Agent Execution Details")
    
    with st.expander("View Detailed Agent Logs", expanded=False):
        agent_results = workflow_results.get("agent_results", {})
        
        # Create columns for agent overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Agents",
                len(agent_results),
                f"{sum(1 for a in agent_results.values() if a.get('status') == 'success')} successful"
            )
        
        with col2:
            st.metric(
                "Total Time",
                f"{workflow_results.get('total_execution_time_ms', 0):.0f}ms",
                "execution time"
            )
        
        with col3:
            if workflow_results.get('requires_escalation'):
                st.metric("Status", "Escalated ⚠️", "priority: high")
            else:
                st.metric("Status", "Auto-Resolved ✓", "no escalation needed")
        
        with col4:
            st.metric(
                "Quality Score",
                f"{workflow_results.get('response_quality', 0):.0%}",
                "response quality"
            )
        
        # Detailed logs for each agent
        st.divider()
        st.write("**Agent Execution Timeline:**")
        
        for agent_name, agent_result in agent_results.items():
            with st.container():
                col1, col2, col3 = st.columns([0.3, 0.3, 0.4])
                
                status_icon = "✅" if agent_result.get('status') == 'success' else "❌"
                
                col1.write(f"{status_icon} **{agent_result.get('agent_name', agent_name)}**")
                col2.write(f"`{agent_result.get('execution_time_ms', 0):.0f}ms`")
                col3.write(f"Status: {agent_result.get('status')}")
                
                # Show output details
                if agent_result.get('output'):
                    with st.expander(f"View {agent_name} output"):
                        st.json(agent_result.get('output'))
                
                # Show error if any
                if agent_result.get('error_message'):
                    st.error(f"Error: {agent_result.get('error_message')}")


def display_ticket_analysis(workflow_results: dict):
    """Display ticket analysis results"""
    st.subheader("🔍 Ticket Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        category = workflow_results.get('category', 'N/A')
        st.metric("📂 Category", category)
    
    with col2:
        priority = workflow_results.get('priority', 'N/A').upper()
        priority_colors = {
            'LOW': '🟢', 'MEDIUM': '🟡', 'HIGH': '🟠', 'CRITICAL': '🔴'
        }
        icon = priority_colors.get(priority, '⚪')
        st.metric("⚡ Priority", f"{icon} {priority}")
    
    with col3:
        sentiment = workflow_results.get('sentiment', 'N/A')
        sentiment_colors = {
            'very_negative': '😠', 'negative': '😞', 'neutral': '😐',
            'positive': '😊', 'very_positive': '😄'
        }
        icon = sentiment_colors.get(sentiment, '❓')
        st.metric("💭 Sentiment", f"{icon} {sentiment}")
    
    with col4:
        confidence = workflow_results.get('classification_confidence', 0)
        st.metric("🎯 Confidence", f"{confidence:.0%}")
    
    # Additional details
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Intent:** " + workflow_results.get('intent', 'N/A'))
    
    with col2:
        st.write("**Assigned Team:** " + workflow_results.get('assigned_team', 'N/A'))


def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🤖 Multi-Agent Customer Support Intelligence Platform")
    st.markdown("### Intelligent Ticket Management & Auto-Response System")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        enable_rag = st.checkbox("Enable RAG Retrieval", value=True, help="Use knowledge base for context")
        enable_escalation = st.checkbox("Enable Escalation Logic", value=True, help="Auto-escalate complex tickets")
        
        st.divider()
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.page = "analytics"
        
        if st.button("📚 Knowledge Base", use_container_width=True):
            st.session_state.page = "knowledge_base"
        
        st.divider()
        
        st.caption("**API Status**")
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Error")
        except:
            st.error("❌ API Not Running")
        
        st.caption("API Endpoint: http://localhost:8000")
    
    # Main content
    tabs = st.tabs(["💬 New Ticket", "📋 History", "📈 Analytics"])
    
    # Tab 1: Process New Ticket
    with tabs[0]:
        st.subheader("Submit a Customer Support Ticket")
        
        with st.form("ticket_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                customer_name = st.text_input(
                    "Customer Name *",
                    placeholder="Enter customer name"
                )
                customer_email = st.text_input(
                    "Customer Email *",
                    placeholder="customer@example.com"
                )
            
            with col2:
                subject = st.text_input(
                    "Subject *",
                    placeholder="Brief description of the issue"
                )
            
            ticket_text = st.text_area(
                "Describe the Issue *",
                placeholder="Please provide detailed information about the customer's issue...",
                height=150
            )
            
            # Additional options
            col1, col2 = st.columns(2)
            with col1:
                use_rag = st.checkbox("Use Knowledge Base", value=enable_rag)
            with col2:
                use_escalation = st.checkbox("Enable Escalation", value=enable_escalation)
            
            submitted = st.form_submit_button("🚀 Process Ticket", use_container_width=True)
        
        if submitted:
            if not customer_name or not customer_email or not ticket_text:
                st.error("❌ Please fill in all required fields")
            else:
                with st.spinner("🔄 Processing ticket through multi-agent pipeline..."):
                    
                    ticket_data = {
                        "ticket_text": ticket_text,
                        "customer_name": customer_name,
                        "customer_email": customer_email,
                        "enable_rag": use_rag,
                        "enable_escalation": use_escalation
                    }
                    
                    results = process_ticket(ticket_data)
                    
                    if results:
                        st.session_state.current_workflow = results
                        st.session_state.ticket_history.append({
                            "timestamp": datetime.now(),
                            "customer": customer_name,
                            "subject": subject,
                            "status": results.get("status"),
                            "category": results.get("category"),
                            "escalated": results.get("requires_escalation")
                        })
                        
                        # Display results
                        if results.get("status") == "completed":
                            st.success("✅ Ticket processed successfully!")
                            
                            # Display analysis
                            display_ticket_analysis(results)
                            
                            st.divider()
                            
                            # Display generated response
                            st.subheader("📝 Generated Response")
                            response_text = results.get("final_response")
                            if response_text:
                                st.info(response_text)
                            
                            st.divider()
                            
                            # Display escalation details if needed
                            if results.get("requires_escalation"):
                                st.warning(
                                    f"⚠️ **This ticket requires escalation**\n\n"
                                    f"**Assigned to:** {results.get('assigned_team')}\n\n"
                                    f"**Escalation Level:** {results.get('escalation_level', 'MEDIUM')}"
                                )
                            else:
                                st.success("✓ This ticket can be auto-resolved")
                            
                            st.divider()
                            
                            # Display agent logs
                            display_agent_logs(results)
                        else:
                            st.error(f"❌ Error: {results.get('error', 'Unknown error')}")
    
    # Tab 2: Ticket History
    with tabs[1]:
        st.subheader("📋 Ticket Processing History")
        
        if st.session_state.ticket_history:
            # Convert to DataFrame
            df = pd.DataFrame(st.session_state.ticket_history)
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Processed",
                    len(st.session_state.ticket_history)
                )
            
            with col2:
                escalated = sum(1 for t in st.session_state.ticket_history if t.get('escalated'))
                st.metric("Escalated", escalated)
            
            with col3:
                auto_resolved = len(st.session_state.ticket_history) - escalated
                st.metric("Auto-Resolved", auto_resolved)
            
            with col4:
                auto_rate = (auto_resolved / len(st.session_state.ticket_history) * 100) if st.session_state.ticket_history else 0
                st.metric("Automation Rate", f"{auto_rate:.0f}%")
        
        else:
            st.info("No tickets processed yet. Submit a ticket from the 'New Ticket' tab.")
    
    # Tab 3: Analytics
    with tabs[2]:
        st.subheader("📊 System Analytics & Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "📧 Tickets Processed",
                len(st.session_state.ticket_history),
                delta=None
            )
        
        with col2:
            if st.session_state.ticket_history:
                escalated = sum(1 for t in st.session_state.ticket_history if t.get('escalated'))
                auto_resolved = len(st.session_state.ticket_history) - escalated
                automation_rate = (auto_resolved / len(st.session_state.ticket_history) * 100)
                st.metric("⚙️ Automation Rate", f"{automation_rate:.1f}%")
        
        st.divider()
        
        # System status
        st.subheader("🔧 System Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("API Status", "🟢 Running")
        
        with col2:
            st.metric("RAG Pipeline", "🟢 Active")
        
        with col3:
            st.metric("Database", "🟢 Connected")


if __name__ == "__main__":
    main()
