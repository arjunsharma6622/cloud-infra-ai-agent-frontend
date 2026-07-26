import streamlit as st


from dialogs import (
    show_json_modal,
    show_srs_modal,
    show_architecture_modal,
    show_code_modal,
)


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