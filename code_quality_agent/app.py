import streamlit as st
import random
import time

st.set_page_config(page_title="Code Quality Review Agent", page_icon="🤖")

st.title("👨‍💻 Telecom SaaS AI Code Quality Checker")
st.markdown("Upload a Python file or paste code below to get an AI-powered code quality analysis.")

code_input = st.text_area("Paste your Python code here:", height=300)
uploaded_file = st.file_uploader("Or upload a .py file", type=["py"])

if uploaded_file:
    code_input = uploaded_file.read().decode("utf-8")
    st.code(code_input, language="python")

if st.button("Analyze Code"):
    if not code_input:
        st.warning("Please provide code to analyze.")
    else:
        with st.spinner("Agent is analyzing your code..."):
            time.sleep(2)  # Simulate API call latency
            
            st.subheader("Analysis Results")
            
            # Simulated Agent Output
            issues_found = random.randint(0, 5)
            if issues_found == 0:
                st.success("✅ Code Quality: Excellent! No major issues found.")
            else:
                st.error(f"⚠️ Found {issues_found} potential issues.")
                
                st.markdown("### Agent Feedback:")
                st.markdown("""
                - **Security**: Hardcoded secrets might be present. Please use `.env` files.
                - **PEP8 Compliance**: Few lines exceed 79 characters. Review naming conventions.
                - **Performance**: A list comprehension could replace the loop at line 14 for better speed.
                - **Type Hinting**: Missing return types on functions.
                """)
                
                with st.expander("Suggested Refactor"):
                    st.code(code_input + "\n# [LangChain output] Code refactored beautifully here...", language="python")

st.markdown("---")
st.caption("Powered by LangChain & Streamlit")
