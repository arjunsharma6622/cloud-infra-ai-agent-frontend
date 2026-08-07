import streamlit as st

from api import deploy_infrastructure


@st.dialog("🚀 Confirm Deployment")
def deploy_dialog(deployment, code):

    st.warning(
        "Please review the generated Terraform before deployment."
    )

    st.subheader("Terraform Files")

    for filename, content in code.items():

        with st.expander(filename):

            st.code(
                content,
                language="hcl",
            )

    st.divider()

    st.markdown(
        f"**Branch:** {deployment['branch_name']}"
    )

    st.link_button(
        "Open Pull Request",
        deployment["pr_url"],
    )

    confirmation = st.text_input(
        "Type YES to confirm deployment"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Deploy",
            use_container_width=True,
        ):

            if confirmation.strip().upper() != "YES":

                st.error(
                    "Please type YES to continue."
                )

                return

            with st.spinner(
                "Starting deployment..."
            ):

                result = deploy_infrastructure(
                    deployment["pr_number"]
                )

            st.success(result["message"])

            st.rerun()

    with col2:

        if st.button(
            "Cancel",
            use_container_width=True,
        ):

            st.rerun()