from streamlit_navigation_bar import st_navbar
import app_pages

style = {
    "nav": {
        "background-color": " #FF5F05",
        "justify-content": "left",
    }
}
page = st_navbar(pages=["All Projects View", "Project View", "Add Invoice", "Project", "IGA"], logo_path='images/ICTlogo.svg',styles=style)

if page == "All Projects View":
    app_pages.all_projects_view.all_projects_view_func()
elif page == "Project View":
    app_pages.project_view.project_view_func()
elif page == "Add Invoice":
    app_pages.add_invoice.add_invoice_func()
elif page == "Project":
    app_pages.add_project.add_project_func()
elif page == "IGA":
    app_pages.add_iga.add_iga_func()

