import streamlit as st

from api import (
    get_projects,
    get_project_history,
)

from state import (
    new_project,
    load_project,
)


def render_sidebar():
    """
    Render workspace sidebar.

    Returns:
        bool
            True if the active project changed.
    """

    project_changed = False

    with st.sidebar:

        st.header("📂 Workspaces")

        if st.button(
            "➕ New Infrastructure Project",
            use_container_width=True,
        ):

            new_project()

            project_changed = True

            st.rerun()

        st.divider()

        st.subheader("Recent Projects")

        threads = get_projects()

        if not threads:

            st.caption("No saved projects.")

            return project_changed

        for thread_id in threads:

            display_name = f"Project {thread_id[:8]}"

            active = (
                thread_id ==
                st.session_state.thread_id
            )

            if st.button(
                display_name,
                key=f"project_{thread_id}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):

                # Already loaded
                if (
                    thread_id
                    == st.session_state.thread_id
                ):
                    continue

                # -------------------------
                # History Cache
                # -------------------------

                cache = st.session_state.project_cache

                if thread_id in cache:

                    history = cache[thread_id]

                else:

                    with st.spinner(
                        "Loading project..."
                    ):

                        history = get_project_history(
                            thread_id
                        )

                    if history:

                        cache[thread_id] = history

                if history:

                    load_project(
                        thread_id,
                        history,
                    )

                    project_changed = True

                    st.rerun()

    return project_changed