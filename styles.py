CUSTOM_CSS = """
<style>

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 950px !important;
}

/* Remove Streamlit spacing */

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

/* Better buttons */

.stButton > button {
    border-radius: 999px;
    height: 42px;
    font-weight: 600;
}

/* Container spacing */

[data-testid="stVerticalBlock"] > div:has(.stButton) {
    margin-top: 8px;
}

/* Expanders */

.streamlit-expanderHeader {
    font-weight: 600;
}

footer {
    visibility: hidden !important;
}

[data-testid="stBottomBlockContainer"] {
    padding-bottom: 1rem !important;
}

[data-testid="stChatInput"] {
    padding-bottom: 0rem !important;
}

/* -------------------------
        Prompt Card
------------------------- */

.prompt-card {
    position: relative;
    background-color: #f7f7f8;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 12px 16px 28px 16px;
    margin-bottom: 0.5rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

@media (prefers-color-scheme: dark) {

.prompt-card {
    background-color: #212121;
    border-color: #333333;
    color: #ececec;
}

}

.prompt-toggle {
    display: none;
}

.prompt-text {

    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;

    overflow: hidden;

    line-height: 1.5;
    font-size: 0.95rem;
    word-break: break-word;
}

.prompt-toggle:checked ~ .prompt-text {

    display: block;
    overflow: visible;

}

.expand-btn {

    position: absolute;
    bottom: 6px;
    right: 12px;

    display: inline-flex;
    align-items: center;
    gap: 4px;

    font-size: 0.78rem;
    font-weight: 500;

    color: #666;

    cursor: pointer;
    user-select: none;

    padding: 3px 6px;
    border-radius: 6px;

    transition: background-color .2s,color .2s;
}

.expand-btn:hover {

    background-color: rgba(0,0,0,.06);
    color:#111;

}

@media (prefers-color-scheme: dark){

.expand-btn{

    color:#999;

}

.expand-btn:hover{

    background:rgba(255,255,255,.08);
    color:white;

}

}

.chevron-icon{

    width:14px;
    height:14px;

    fill:currentColor;

    transition:transform .2s ease;

}

.prompt-toggle:checked ~ .expand-btn .chevron-icon{

    transform:rotate(180deg);

}

.prompt-toggle:not(:checked) ~ .expand-btn .btn-text::after{

    content:"Show more";

}

.prompt-toggle:checked ~ .expand-btn .btn-text::after{

    content:"Show less";

}

</style>
"""