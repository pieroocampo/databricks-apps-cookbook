from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container([
        html.H1("Data Visualization", className="my-4"),
        html.H2("AI/BI Dashboard", className="mb-3"),
        html.P([
            "This recipe uses ",
            html.A(
                "Databricks AI/BI",
                href="https://www.databricks.com/product/ai-bi",
                target="_blank"
            ),
            " to embed a dashboard into a Databricks App."
        ], className="mb-4"),
        
        dbc.Tabs([
            # Try it tab
            dbc.Tab(label="Try it", children=[
                dbc.Form([
                    dbc.Label("Embed the dashboard:", className="mt-3"),
                    dbc.Input(
                        id="iframe-source-input",
                        type="text",
                        placeholder="https://workspace.azuredatabricks.net/embed/dashboardsv3/dashboard-id",
                        style={
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #dee2e6",
                            "boxShadow": "inset 0 1px 2px rgba(0,0,0,0.075)"
                        }
                    ),
                ]),
                html.Div(id="iframe-container", className="mt-4")
            ], className="p-3"),
            
            # Code snippet tab
            dbc.Tab(label="Code snippet", children=[
                dcc.Markdown('''```python
from dash import html

iframe_source = "https://workspace.azuredatabricks.net/embed/dashboardsv3/dashboard-id"

html.Iframe(
    src=iframe_source,
    width="700px",
    height="600px",
    style={"border": "none"}
)
```''', className="p-4 border rounded")
            ], className="p-3"),
            
            # Requirements tab
            dbc.Tab(label="Requirements", children=[
                dbc.Row([
                    dbc.Col([
                        html.H4("Permissions (app service principal)", className="mb-3"),
                        html.Ul([
                            dcc.Markdown("**```CAN VIEW```** on the dashboard")
                        ], className="mb-4")
                    ]),
                    dbc.Col([
                        html.H4("Databricks resources", className="mb-3"),
                        html.Ul([
                            html.Li("SQL Warehouse")
                        ], className="mb-4")
                    ]),
                    dbc.Col([
                        html.H4("Dependencies", className="mb-3"),
                        html.Ul([
                            dcc.Markdown("* [Dash](https://pypi.org/project/dash/) - `dash`")
                        ], className="mb-4")
                    ])
                ])
            ], className="p-3")
        ], className="mb-4")
    ], fluid=True, className="py-4")

@callback(
    Output("iframe-container", "children"),
    [Input("iframe-source-input", "value")],
    prevent_initial_call=True
)
def update_iframe(iframe_source):
    if not iframe_source:
        return None
    
    return html.Iframe(
        src=iframe_source,
        width="700px",
        height="600px",
        style={
            "border": "none",
            "borderRadius": "4px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
        }
    )

# Make layout available at module level
__all__ = ['layout']
