import streamlit as st
import uuid


def init_session_state():
    """Initialize all session state variables."""

    defaults = {
        "thread_id": str(uuid.uuid4()),
        "messages": [],
        "projects": [],
        "project_cache": {},
        "active_project": None,
        "is_streaming": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def new_project():
    """Reset UI for a brand-new infrastructure project."""

    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.active_project = st.session_state.thread_id
    st.session_state.is_streaming = False


def load_project(thread_id: str, history: dict):
    """Load a project returned from the backend into session state."""

    st.session_state.thread_id = thread_id
    st.session_state.active_project = thread_id

    messages = []

    if history.get("user_prompt"):
        messages.append(
            {
                "role": "user",
                "content": history["user_prompt"],
            }
        )

    if history.get("code"):
        messages.append(
            {
                "role": "assistant",
                "summary": "✅ **Infrastructure recovered from history.**",
                "spec": history.get("spec", {}),
                "srs": history.get("srs", ""),
                "plan": history.get("plan", ""),
                "code": history.get("code", {}),
            }
        )

    st.session_state.messages = messages

    # Cache it so we don't fetch it again
    st.session_state.project_cache[thread_id] = history