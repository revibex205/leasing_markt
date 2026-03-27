"""
components/styles.py
CSS injection for LeaseMarkt using st.html() which bypasses Streamlit's
markdown renderer and reliably injects raw HTML into the page.
"""

import os
import streamlit as st

# Path to the static CSS file relative to this module
_CSS_FILE = os.path.join(os.path.dirname(__file__), "..", "static", "styles.css")


def inject_global_css():
    """
    Inject the LeaseMarkt design system CSS via st.html().
    Using st.html() instead of st.markdown() avoids the issue where very
    large <style> blocks are rendered as visible text by Streamlit's
    markdown processor.
    """
    # Read CSS from the static file
    try:
        with open(_CSS_FILE, encoding="utf-8") as f:
            css = f.read()
    except FileNotFoundError:
        # Fallback: minimal inline CSS if file is missing
        css = ""

    # Inject Google Fonts + the full stylesheet via st.html()
    # st.html() renders raw HTML without markdown processing (Streamlit >= 1.31)
    st.html(f"""
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
  rel="stylesheet"
>
<style>
{css}
</style>
""")
