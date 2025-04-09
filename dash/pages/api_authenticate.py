from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import dash
import requests

dash.register_page(
    __name__,
    path="/api-app/authenticate",
    title="API-based Authentication",
    name="API-based Authentication",
    category="Authentication",
    icon="material-symbols:api",
)


def layout():
    return dbc.Container(
        [
            html.H1("API-based Authentication", className="my-4"),
            html.H2(
                "Access Databricks Apps using an OAuth2 Bearer Token", className="mb-3"
            ),
            html.P(
                [
                    "This recipe demonstrates how to access Databricks Apps using an OAuth2 Bearer Token."
                ],
                className="mb-4",
            ),
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="Try it",
                        tab_id="tab-1",
                        children=[
                            html.Div(
                                [
                                    html.H5(
                                        "Make an API call using token-based authentication",
                                        className="mb-3",
                                    ),
                                    dbc.Button(
                                        "GET /api/healthcheck",
                                        id="healthcheck-button",
                                        color="primary",
                                        className="mb-3",
                                    ),
                                    dbc.Spinner(
                                        html.Pre(
                                            id="api-response",
                                            style={
                                                "backgroundColor": "#f8f9fa",
                                                "padding": "1rem",
                                                "borderRadius": "0.25rem",
                                                "maxHeight": "400px",
                                                "overflowY": "auto",
                                                "whiteSpace": "pre-wrap",
                                                "wordBreak": "break-word",
                                            },
                                        ),
                                        color="primary",
                                        type="border",
                                    ),
                                ],
                                className="p-3",
                            )
                        ],
                        className="p-3",
                    ),
                    dbc.Tab(
                        label="Code snippets",
                        tab_id="tab-2",
                        children=[
                            html.Div(
                                [
                                    html.H4("Example FastAPI App", className="mb-3"),
                                    html.H6("app.py", className="mb-3"),
                                    dcc.Markdown(
                                        """```python
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI()

# Example endpoint where /api prefix must be used to support token-based authentication
@app.get("/api/healthcheck")
def healthcheck():
    return {
        'status': 'OK',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
```""",
                                        className="p-4 border rounded mb-4",
                                    ),
                                    html.H6("app.yaml", className="mb-3"),
                                    dcc.Markdown(
                                        """```yaml
command: ["uvicorn", "app:app"]
```""",
                                        className="p-4 border rounded mb-4",
                                    ),
                                    html.H4(
                                        "Obtain an OAuth2 Bearer Token using the Databricks CLI",
                                        className="mb-3",
                                    ),
                                    dcc.Markdown(
                                        """```sh
$ databricks auth login --host https://<your-databricks-workspace-url> --profile <your-profile-name>
Profile <your-profile-name> was successfully saved

$ databricks auth token --profile <your-profile-name>
{
  "access_token": "eyJ...<REDACTED>",
  "token_type": "Bearer",
  "expiry": "2025-04-10T00:12:59.78761+01:00"
}
```""",
                                        className="p-4 border rounded mb-4",
                                    ),
                                    html.H4("Client Code", className="mb-3"),
                                    dcc.Markdown(
                                        """```python
import requests

# Replace with appropriate OAuth2 Bearer token
OAUTH_TOKEN = "eyJ...<REDACTED>"

# Replace with your app's URL path
APP_URL_PATH = "https://<app-name>-<app-id>.<cloud>.databricksapps.com/api/healthcheck"

res = requests.get(url=APP_URL_PATH, headers={'Authorization': f'Bearer {OAUTH_TOKEN}'})

if res.status_code == 200:
    print(res.json())
```""",
                                        className="p-4 border rounded",
                                    ),
                                ],
                                className="p-3",
                            )
                        ],
                        className="p-3",
                    ),
                    dbc.Tab(
                        label="Requirements",
                        tab_id="tab-3",
                        children=[
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H4(
                                                "Permissions (app service principal)",
                                                className="mb-3",
                                            ),
                                            html.Ul(
                                                [
                                                    dcc.Markdown(
                                                        "**```CAN MANAGE```** permission on the app"
                                                    )
                                                ],
                                                className="mb-4",
                                            ),
                                        ]
                                    ),
                                    dbc.Col(
                                        [
                                            html.H4(
                                                "Databricks resources", className="mb-3"
                                            ),
                                            html.Ul(
                                                [html.Li("Databricks App")],
                                                className="mb-4",
                                            ),
                                        ]
                                    ),
                                    dbc.Col(
                                        [
                                            html.H4("Dependencies", className="mb-3"),
                                            html.Ul(
                                                [
                                                    dcc.Markdown(
                                                        "* [FastAPI](https://fastapi.tiangolo.com/) - `fastapi`"
                                                    ),
                                                    dcc.Markdown(
                                                        "* [Uvicorn](https://www.uvicorn.org/) - `uvicorn`"
                                                    ),
                                                    dcc.Markdown(
                                                        "* [Requests](https://requests.readthedocs.io/) - `requests`"
                                                    ),
                                                    dcc.Markdown(
                                                        "* [Dash](https://pypi.org/project/dash/) - `dash`"
                                                    ),
                                                ],
                                                className="mb-4",
                                            ),
                                        ]
                                    ),
                                ]
                            )
                        ],
                        className="p-3",
                    ),
                ],
                id="tabs",
                active_tab="tab-1",
                className="mb-4",
            ),
        ],
        fluid=True,
        className="py-4",
    )


@callback(
    Output("api-response", "children"),
    Input("healthcheck-button", "n_clicks"),
)
def update_api_response(n_clicks):
    if n_clicks is None:
        return "Click the button above to test the healthcheck endpoint."

    try:
        response = requests.get("http://localhost:8050/api/healthcheck")
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


# Make layout available at module level
__all__ = ["layout"]
