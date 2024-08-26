from streamlit_navigation_bar import st_navbar
import pages_folder

style = {
    "nav": {
        "background-color": " #FF5F05",
        "justify-content": "left",
    }
}
page = st_navbar(pages=["All Projects View", "Project View", "Add Invoice", "Add Project"], logo_path='images/ICTlogo.svg',styles=style)

if page == "All Projects View":
    pages_folder.all_projects_view.all_projects_view_func()
elif page == "Project View":
    pages_folder.project_view.project_view_func()
elif page == "Add Invoice":
    pages_folder.add_invoice.add_invoice_func()
elif page == "Add Project":
    pages_folder.add_project.add_project_func()

