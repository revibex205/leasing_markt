"""
patch_html_calls.py
Converts st.markdown(..., unsafe_allow_html=True) to st.html(...)
across all page files. Run once: python patch_html_calls.py
"""

import os
import glob

FILES = ["app.py"] + sorted(glob.glob("pages/*.py"))


def patch(text: str) -> str:
    """
    Walk through the file tracking open parentheses to find
    st.markdown( calls that contain unsafe_allow_html=True
    and convert them to st.html( calls.
    """
    result = []
    i = 0
    n = len(text)

    while i < n:
        # Look for st.markdown(
        start = text.find("st.markdown(", i)
        if start == -1:
            result.append(text[i:])
            break

        # Copy everything before this call unchanged
        result.append(text[i:start])

        # Find the matching closing paren
        depth = 0
        j = start + len("st.markdown(")
        depth = 1
        while j < n and depth > 0:
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
            j += 1

        call_content = text[start:j]  # the full call including st.markdown( and )

        if "unsafe_allow_html=True" in call_content:
            # Replace st.markdown( with st.html(
            call_content = call_content.replace("st.markdown(", "st.html(", 1)
            # Remove , unsafe_allow_html=True
            call_content = call_content.replace(", unsafe_allow_html=True)", ")")
            call_content = call_content.replace(",unsafe_allow_html=True)", ")")
            call_content = call_content.replace(", unsafe_allow_html = True)", ")")

        result.append(call_content)
        i = j

    return "".join(result)


def main():
    for fp in FILES:
        if not os.path.exists(fp):
            print(f"  skip (not found): {fp}")
            continue
        with open(fp, encoding="utf-8") as f:
            original = f.read()
        patched = patch(original)
        if patched != original:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(patched)
            count = original.count("unsafe_allow_html=True")
            print(f"  ✓ Patched {count} call(s): {fp}")
        else:
            print(f"  — No changes: {fp}")


if __name__ == "__main__":
    main()
    print("Done.")
