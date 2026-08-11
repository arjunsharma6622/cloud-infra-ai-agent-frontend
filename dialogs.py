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
    st.markdown(plan)

@st.dialog("📐 Terraform Project Plan", width="large")
def show_project_plan_modal(project_plan: dict):
    """
    Display the Terraform project plan.
    """

    if not project_plan:
        st.info("No project plan available.")
        return

    st.markdown(
        f"**Complexity:** "
        f"`{project_plan.get('complexity', 'unknown')}`"
    )

    st.divider()

    generation_units = project_plan.get(
        "generation_units",
        [],
    )

    for unit in generation_units:

        name = unit.get("name", "Unnamed")
        path = unit.get("path", ".")
        purpose = unit.get("purpose", "")
        resources = unit.get(
            "terraform_resources",
            [],
        )
        depends_on = unit.get(
            "depends_on",
            [],
        )
        files = unit.get(
            "files",
            [],
        )

        with st.expander(
            f"📦 {name}  —  `{path}`",
            expanded=False,
        ):

            if purpose:
                st.markdown(
                    f"**Purpose:** {purpose}"
                )

            if resources:
                st.markdown("**Terraform Resources:**")

                for resource in resources:
                    st.code(
                        resource,
                        language="text",
                    )

            if depends_on:
                st.markdown(
                    "**Depends on:** "
                    + ", ".join(
                        f"`{dep}`"
                        for dep in depends_on
                    )
                )

            if files:
                st.markdown("**Files:**")

                for file in files:
                    st.markdown(
                        f"- `{path.rstrip('/')}/{file}`"
                        if path not in ("", ".")
                        else f"- `{file}`"
                    )

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