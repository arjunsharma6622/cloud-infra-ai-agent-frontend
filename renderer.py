import streamlit as st

from dialogs import (
    show_json_modal,
    show_srs_modal,
    show_architecture_modal,
)

from deployment_dialog import deploy_dialog


def render_user_prompt(prompt: str):
    """Render a user message."""
    st.markdown(prompt)


def render_assistant_output(
    msg_id,
    summary,
    spec,
    srs,
    plan,
    code,
    deployment=None,
):

    with st.container(border=True):

        st.success("Infrastructure Generated")

        st.markdown(summary)

        st.markdown("#### 📦 Generated Artifacts")

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button(
                "🧠 Intent",
                key=f"intent_{msg_id}",
                use_container_width=True,
            ):
                show_json_modal(spec)

        with c2:
            if st.button(
                "📄 SRS",
                key=f"srs_{msg_id}",
                use_container_width=True,
            ):
                show_srs_modal(srs)

        with c3:
            if st.button(
                "🏗️ Architecture",
                key=f"arch_{msg_id}",
                use_container_width=True,
            ):
                show_architecture_modal(plan)

        st.divider()

        st.subheader("Terraform Files")

        for filename, content in code.items():

            with st.expander(
                f"📄 {filename}",
                expanded=False,
            ):
                st.code(
                    content,
                    language="hcl",
                )

        # ----------------------------------
        # Deployment Section
        # ----------------------------------

        if deployment:

            st.divider()

            st.success("🚀 Deployment Ready")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Branch:** {deployment['branch_name']}")
                st.write(f"**Deployment ID:** {deployment['deployment_id']}")

            with col2:
                st.link_button(
                    "🔗 Open Pull Request",
                    deployment["pr_url"],
                    use_container_width=True,
                )

            st.info(
                "Please review the Pull Request and Terraform before deployment."
            )

            if st.button(
                "🚀 Deploy Infrastructure",
                key=f"deploy_{msg_id}",
                use_container_width=True,
            ):
                deploy_dialog(
                    deployment,
                    code,
                )