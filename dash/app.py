from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from view_groups import groups
from dash_iconify import DashIconify

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "📖 Databricks Apps Cookbook 🔍"

# Create navigation sidebar from groups
def create_sidebar():
    nav_items = []
    nav_items.append(
        dbc.NavLink(
            "📖 Introduction",
            href="/",
            className="sidebar-link text-dark fw-bold",
            active="exact"
        )
    )
    
    for group in groups:
        if group.get("title"):
            nav_items.append(
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            DashIconify(icon=group["title"]["icon"]),
                            html.Span(group["title"]["text"], className="h6 mt-3 mb-2 ms-2")
                        ], className="d-flex align-items-center")
                    ]),
                    dbc.Nav([
                        dbc.NavLink(
                            [
                                view["label"],
                                # Add a small dot indicator when active
                                html.Span("•", className="ms-2 d-none active-indicator")
                            ],
                            href=f"/{view['label'].lower().replace(' ', '-')}",
                            className="sidebar-link text-dark ps-3",
                            active="exact"
                        ) for view in group["views"]
                    ], vertical=True)
                ])
            )
    return html.Div(nav_items, className="py-2")

app.layout = html.Div([
    dbc.Container([
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            # Sidebar
            dbc.Col([
                html.Div([
                    html.Img(src="assets/logo.svg", className="logo ms-4", style={
                        'width': '30px',
                        'margin-top': '20px'
                    }),
                ], className="sidebar-header"),
                html.Div(create_sidebar(), className="ps-4")
            ], width=2, className="bg-light border-end overflow-auto p-0"),
            
            # Main content
            dbc.Col([
                html.Div(id='page-content', className="px-4 py-4")
            ], width=10, className="content p-0")
        ], className="g-0")
    ], fluid=True, className="vh-100 p-0")
])

# Callback to handle page routing
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if not pathname or pathname == "/":
        from views.book_intro import layout
        return layout()
    
    # Dynamically load the correct view based on URL
    for group in groups:
        for view in group.get("views", []):
            if f"/{view['label'].lower().replace(' ', '-')}" == pathname:
                try:
                    module_path = view['page'].replace('/', '.').replace('.py', '')
                    layout = getattr(__import__(module_path, fromlist=['layout']), 'layout')
                    return layout()
                except ImportError:
                    return html.Div("Page not found", className="error-message")
    
    return html.Div("404 - Page Not Found", className="error-message")

if __name__ == '__main__':
    app.run_server(debug=True)
