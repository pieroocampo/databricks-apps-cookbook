from dash import html, dcc
import dash_bootstrap_components as dbc
from view_groups import groups
from dash_iconify import DashIconify

def create_group_cards(groups):
    cards = []
    for idx, group in enumerate(groups):
        if group.get("title"):
            cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            # Modified group title to ensure class is applied
                            html.Div([
                                DashIconify(icon=group["title"]["icon"], className="me-2"),
                                group["title"]["text"]
                            ], className="h5 mb-3", style={
                                'cursor': 'pointer',
                                'display': 'inline-block',
                                'padding': '4px 8px',
                                'borderRadius': '4px',
                            }),
                            # Modified recipe links
                            html.Ul([
                                html.Li(
                                    dcc.Link(
                                        view["label"],
                                        href=f"/{view['label'].lower().replace(' ', '-')}",
                                        className="recipe-link",
                                        style={
                                            'display': 'block',
                                            'padding': '8px 12px',
                                            'borderRadius': '4px',
                                            'color': '#1b3139',
                                            'textDecoration': 'none',
                                        }
                                    )
                                ) for view in group["views"]
                            ], className="list-unstyled mb-0")
                        ])
                    ], className="h-100 bg-light")
                ], md=6, lg=3, className="mb-4")
            )
    return dbc.Row(cards, className="g-4")

def layout():
    return dbc.Container([
        # Header section with icon and title
        dbc.Row([
            dbc.Col([
                html.Div([
                    "📖 Databricks Apps Cookbook 🔍"
                ], className="display-5 mb-5 mt-4")
            ], className="text-left ps-3")
        ]),
        
        # Welcome section
        html.Div([
            html.H4("Welcome to the Databricks Apps Cookbook!", className="mb-3"),
            html.P([
                "Are you ready to serve some tasty apps to your users? You're in the right place!",
                html.Br(),
                html.Br(),
                "Explore the recipes via the sidebar to quickly build flexible and engaging data apps directly on Databricks.",
                html.Br(),
                html.Br(),
                "Have a great recipe to share? Raise a pull request on the ",
                html.A(
                    "GitHub repository",
                    href="https://github.com/pbv0/databricks-apps-cookbook",
                    target="_blank",
                    className="text-primary"
                ),
                "!"
            ], className="mb-4")
        ], className="mb-5 ps-3"),
        
        # Recipes section
        html.H3("Recipes", className="mb-4 pb-2 border-bottom ps-3"),
        html.Div(create_group_cards(groups), className="mb-5"),
        
        # Links section
        html.H3("Links", className="mb-4 pb-2 border-bottom ps-3"),
        dbc.Row([
            dbc.Col([
                html.H4("Official documentation", className="h5 mb-3"),
                html.Ul([
                    html.Li(html.A("AWS", href="https://docs.databricks.com/en/dev-tools/databricks-apps/index.html", target="_blank")),
                    html.Li(html.A("Azure", href="https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/", target="_blank")),
                    html.Li(html.A("Python SDK", href="https://databricks-sdk-py.readthedocs.io/en/latest/", target="_blank"))
                ], className="list-unstyled")
            ], md=4),
            dbc.Col([
                html.H4("Code samples", className="h5 mb-3"),
                html.Ul([
                    html.Li(html.A("Databricks Apps Templates", href="https://github.com/databricks/app-templates", target="_blank"))
                ], className="list-unstyled")
            ], md=4),
            dbc.Col([
                html.H4("Blog posts", className="h5 mb-3"),
                html.Ul([
                    html.Li(html.A("Building Data Applications", href="https://www.linkedin.com/pulse/building-data-applications-databricks-apps-ivan-trusov-6pjwf/", target="_blank"))
                ], className="list-unstyled")
            ], md=4)
        ], className="ps-3")
    ], fluid=True, className="py-4")

# Make layout available at module level
__all__ = ['layout']
