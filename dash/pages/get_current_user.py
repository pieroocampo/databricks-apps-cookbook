from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import dash
from flask import request

# Register the page
dash.register_page(
    __name__,
    path='/get-current-user',
    title='Get current user',
    name='Get current user',
    icon='material-symbols:person'
)

def layout():
    return dbc.Container([
        html.H1("Get current user", className="my-4"),
        html.P([
            "This recipe gets information about the user accessing this Databricks App from their ",
            html.A("HTTP headers", 
                  href="https://docs.databricks.com/en/security/auth-authz/pass-through-auth.html",
                  target="_blank",
                  className="text-primary")
        ], className="mb-4"),
        
        dbc.Tabs([
            dbc.Tab([
                html.H3("User Details", className="mt-4 mb-3"),
                
                # User details section
                dbc.Row([
                    dbc.Col([
                        html.P([
                            html.Strong("E-mail: "), 
                            html.Span(id="user-email")
                        ], className="mb-2"),
                        html.P([
                            html.Strong("Username: "), 
                            html.Span(id="user-name")
                        ], className="mb-2"),
                        html.P([
                            html.Strong("IP Address: "), 
                            html.Span(id="user-ip")
                        ], className="mb-4"),
                    ])
                ]),
                
                html.H3("All Headers", className="mb-3"),
                html.Pre(
                    id="all-headers",
                    className="bg-light p-3 border rounded"
                )
                
            ], label="Try it", tab_id="try-it"),
            
            # ... other tabs as needed ...
            
        ], id="tabs", active_tab="try-it", className="mb-4")
    ], fluid=True, className="py-4")

@callback(
    [Output("user-email", "children"),
     Output("user-name", "children"),
     Output("user-ip", "children"),
     Output("all-headers", "children")],
    Input("tabs", "active_tab")
)
def update_user_info(tab):
    headers = dict(request.headers)
    
    # Get specific user details from headers
    email = headers.get('X-Databricks-Useremail', 'Not available')
    username = headers.get('X-Databricks-Username', 'Not available')
    ip = request.remote_addr or 'Not available'
    
    # Format all headers for display
    all_headers = "\n".join([f"{k}: {v}" for k, v in headers.items()])
    
    return email, username, ip, all_headers

# Make layout available at module level
__all__ = ['layout']