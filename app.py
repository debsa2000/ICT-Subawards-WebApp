from streamlit_navigation_bar import st_navbar
import app_pages

style = {
    "nav": {
        "background-color": " #FF5F05",
        "justify-content": "left",
    }
}
page = st_navbar(pages=["All Projects View", "Project View", "Invoice", "Project", "IGA"], logo_path='images/ICTlogo.svg',styles=style)

if page == "All Projects View":
    app_pages.all_projects_view.all_projects_view_func()
elif page == "Project View":
    app_pages.project_view.project_view_func()
elif page == "Invoice":
    app_pages.invoice_page.invoice_page_func()
elif page == "Project":
    app_pages.project_page.project_page_func()
elif page == "IGA":
    app_pages.iga_page.iga_page_func()
