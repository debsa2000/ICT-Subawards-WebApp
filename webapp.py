from streamlit_navigation_bar import st_navbar
import webapp_pages

style = {
    "nav": {
        "background-color": " #FF5F05",
        "justify-content": "left",
    }
}
page = st_navbar(pages=["All Projects View", "Project View", "Add Invoice", "Add Project"], logo_path='images/ICTlogo.svg',styles=style)

if page == "All Projects View":
    webapp_pages.all_projects_view.all_projects_view_func()
elif page == "Project View":
    webapp_pages.project_view.project_view_func()
elif page == "Add Invoice":
    webapp_pages.add_invoice.add_invoice_func()
elif page == "Add Project":
    webapp_pages.add_project.add_project_func()

