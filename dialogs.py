import streamlit as st


@st.dialog("📄 Parsed Intent (JSON)", width="large")
def show_json_modal(spec_data: dict):
    """
    Display the parsed Project Specification.
    """
    st.json(spec_data)


@st.dialog("📋 Software Requirements Specification", width="large")
def show_srs_modal(srs: str):
    """
    Display the generated SRS document.
    """
    st.markdown(srs)


@st.dialog("🏗️ Architecture Blueprint", width="large")
def show_architecture_modal(plan):
    """
    Display the generated architecture plan.
    """

    if isinstance(plan, list):

        if len(plan) > 0:

            if isinstance(plan[0], dict):

                plan = plan[0].get("text", str(plan))

    st.markdown(plan)


@st.dialog("💻 Terraform File", width="large")
def show_code_modal(filename: str, content: str):
    """
    Display one Terraform file.
    """

    clean_content = (
        content
        .replace("\\n", "\n")
        .replace("\\t", "  ")
    )

    st.code(
        clean_content,
        language="hcl",
        line_numbers=True,
    )