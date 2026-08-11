import requests
import streamlit as st

BASE_URL = "http://localhost:8000"
TIMEOUT = (5, 120)  # connect timeout, read timeout


# -------------------------------
# Cached API Calls
# -------------------------------

@st.cache_data(ttl=30, show_spinner=False)
def get_projects():
    """
    Returns all workspace IDs.
    Cached for 30 seconds because this changes infrequently.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/chats",
            timeout=TIMEOUT,
        )
        response.raise_for_status()

        return response.json().get("threads", [])

    except Exception:
        return []


@st.cache_data(show_spinner=False)
def get_project_history(thread_id: str):
    """
    Returns the saved state of a project.
    Cached until manually cleared.
    """

    try:
        response = requests.get(
            f"{BASE_URL}/chat/{thread_id}/history",
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    except Exception:
        return None


# -------------------------------
# Backend Status Stream
# -------------------------------

def stream_chat(prompt: str, thread_id: str):
    """
    Streams LangGraph events from FastAPI.

    Returns:
        requests.Response
    """

    payload = {
        "prompt": prompt,
        "thread_id": thread_id,
    }

    response = requests.post(
        f"{BASE_URL}/stream",
        json=payload,
        stream=True,
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    return response


# -------------------------------
# Cache Helpers
# -------------------------------

def refresh_projects():
    """
    Clears workspace cache after a new project
    or deleted project.
    """

    get_projects.clear()


def refresh_history(thread_id=None):
    """
    Clears cached history.

    If thread_id is None,
    clears all cached histories.
    """

    get_project_history.clear()