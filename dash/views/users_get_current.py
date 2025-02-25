from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from flask import request

def layout():
    return dbc.Container([
        html.H1("Users", className="my-4"),
        html.H2("Get current user", className="mb-3"),
        html.P([
            "This recipe gets information about the user accessing this Databricks App from their ",
            html.A(
                "HTTP headers",
                href="https://docs.databricks.com/en/dev-tools/databricks-apps/app-development.html#what-http-headers-are-passed-to-databricks-apps",
                target="_blank"
            ),
            "."
        ], className="mb-4"),
        
        dbc.Tabs([
            dbc.Tab(label="Try it", tab_id="tab-1", children=[
                html.Div([
                    html.H4("User Details", className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.P([
                                html.Strong("E-mail: "), 
                                html.Span(id="user-email")
                            ]),
                            html.P([
                                html.Strong("Username: "), 
                                html.Span(id="user-name")
                            ]),
                            html.P([
                                html.Strong("IP Address: "), 
                                html.Span(id="user-ip")
                            ])
                        ])
                    ]),
                    html.H4("All Headers", className="mt-4 mb-3"),
                    html.Pre(id="all-headers", style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '1rem',
                        'borderRadius': '0.25rem'
                    })
                ], className="p-3")
            ], className="p-3"),
            
            dbc.Tab(label="Code snippet", tab_id="tab-2", children=[
                dcc.Markdown('''```python
from flask import request
headers = request.headers
email = headers.get("X-Forwarded-Email")
username = headers.get("X-Forwarded-Preferred-Username")
user = headers.get("X-Forwarded-User")
ip = headers.get("X-Real-Ip")
print(f"E-mail: {email}, username: {username}, user: {user}, ip: {ip}")
```''', className="p-4 border rounded"),
                dbc.Alert([
                    html.H4("Other frameworks", className="alert-heading"),
                    html.P([
                        "Streamlit: use ",
                        html.Code("st.context.headers"),
                        " from the Streamlit library."
                    ])
                ], color="info", className="mt-3")
            ], className="p-3"),
            
            dbc.Tab(label="Requirements", tab_id="tab-3", children=[
                dbc.Row([
                    dbc.Col([
                        html.H4("Permissions (app service principal)", className="mb-3"),
                        html.P("No permissions needed", className="mb-4")
                    ]),
                    dbc.Col([
                        html.H4("Databricks resources", className="mb-3"),
                        html.P("None", className="mb-4")
                    ]),
                    dbc.Col([
                        html.H4("Dependencies", className="mb-3"),
                        html.Ul([
                            dcc.Markdown("* [Dash](https://pypi.org/project/dash/) - `dash`")
                        ], className="mb-4")
                    ])
                ])
            ], className="p-3")
        ], id="tabs", active_tab="tab-1", className="mb-4")
    ], fluid=True, className="py-4")

@callback(
    [Output("user-email", "children"),
     Output("user-name", "children"),
     Output("user-ip", "children"),
     Output("all-headers", "children")],
    Input("_", "children") 
)
def update_user_info(_):
    headers = dict(request.headers)
    return (
        headers.get("X-Forwarded-Email", "Not available"),
        headers.get("X-Forwarded-Preferred-Username", "Not available"),
        headers.get("X-Real-Ip", "Not available"),
        str(headers)
    )

# Make layout available at module level
__all__ = ['layout']