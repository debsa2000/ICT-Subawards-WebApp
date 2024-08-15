from streamlit_navigation_bar import st_navbar


page_names=['Project View','Analytics']
logopath="images/ICTlogo.svg"
styles = {
    "nav": {
        "background-color": " #FF5F05",
        "justify-content": "left",
    }
}
nav_bar = st_navbar(pages=page_names, logo_path=logopath, styles=styles)

def get_navbar():
    navbar=nav_bar
    return navbar