import os
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from databricks.connect import DatabricksSession
from dash.exceptions import PreventUpdate

server_hostname = os.getenv("DATABRICKS_HOST") or os.getenv("DATABRICKS_HOSTNAME")

def connect_to_cluster(cluster_id: str):
    return DatabricksSession.builder.remote(
        host=server_hostname, cluster_id=cluster_id
    ).getOrCreate()

def layout():
    return dbc.Container([
        html.H1("Compute", className="my-4"),
        html.H2("Connect", className="mb-3"),
        html.P([
            "This recipe uses ",
            html.A(
                "Databricks Connect",
                href="https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html",
                target="_blank"
            ),
            " to execute pre-defined Python or SQL code on a ",
            html.Strong("shared"),
            " cluster with UI inputs."
        ], className="mb-4"),
        
        dbc.Tabs([
            dbc.Tab([
                dbc.Form([
                    dbc.Label("Specify cluster id:", className="mt-3"),
                    dbc.Input(
                        id="cluster-id-input",
                        type="text",
                        placeholder="0709-132523-cnhxf2p6",
                        style={
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #dee2e6",
                            "boxShadow": "inset 0 1px 2px rgba(0,0,0,0.075)"
                        }
                    ),
                ]),
                html.Div(id="connection-status", className="mt-3"),
                
                # Python and SQL tabs
                dbc.Tabs([
                    dbc.Tab([
                        dbc.Form([
                            dbc.Label("How many data points to generate?", className="mt-3"),
                            dbc.Input(
                                id="data-points-input",
                                type="number",
                                min=1,
                                value=10,
                                step=1,
                                style={
                                    "backgroundColor": "#f8f9fa",
                                    "border": "1px solid #dee2e6",
                                    "boxShadow": "inset 0 1px 2px rgba(0,0,0,0.075)"
                                }
                            ),
                            dbc.Button(
                                "Generate",
                                id="generate-button",
                                color="primary",
                                className="mt-3"
                            )
                        ]),
                        html.Div(id="python-output", className="mt-3")
                    ], label="Python", tab_id="python"),
                    
                    dbc.Tab([
                        dbc.Row([
                            dbc.Col([
                                html.H3("Dataset A", className="mb-3 mt-5"),
                                dbc.Card([
                                    dbc.CardBody(
                                        dbc.Table([
                                            html.Thead([
                                                html.Tr([
                                                    html.Th("id", style={
                                                        "backgroundColor": "#ffffff",
                                                        "borderBottom": "1px solid #dee2e6",
                                                        "fontWeight": "600"
                                                    }),
                                                    html.Th("value", style={
                                                        "backgroundColor": "#ffffff",
                                                        "borderBottom": "1px solid #dee2e6",
                                                        "fontWeight": "600"
                                                    })
                                                ])
                                            ]),
                                            html.Tbody([
                                                html.Tr([html.Td("1"), html.Td("A1")]),
                                                html.Tr([html.Td("2"), html.Td("A2")]),
                                                html.Tr([html.Td("3"), html.Td("A3")])
                                            ])
                                        ], bordered=False, hover=True, style={
                                            "marginBottom": "0"
                                        })
                                    )
                                ], style={
                                    "boxShadow": "0 0 5px rgba(0,0,0,0.1)",
                                    "border": "1px solid #dee2e6",
                                    "borderRadius": "8px"
                                }, className="mb-4")
                            ], width=3, className="pe-4 ps-4"),
                            
                            dbc.Col(width=3),
                            
                            dbc.Col([
                                html.H3("Dataset B", className="mb-3 mt-5"),
                                dbc.Card([
                                    dbc.CardBody(
                                        dbc.Table([
                                            html.Thead([
                                                html.Tr([
                                                    html.Th("id", style={
                                                        "backgroundColor": "#ffffff",
                                                        "borderBottom": "1px solid #dee2e6",
                                                        "fontWeight": "600"
                                                    }),
                                                    html.Th("value", style={
                                                        "backgroundColor": "#ffffff",
                                                        "borderBottom": "1px solid #dee2e6",
                                                        "fontWeight": "600"
                                                    })
                                                ])
                                            ]),
                                            html.Tbody([
                                                html.Tr([html.Td("2"), html.Td("B1")]),
                                                html.Tr([html.Td("3"), html.Td("B2")]),
                                                html.Tr([html.Td("4"), html.Td("B3")])
                                            ])
                                        ], bordered=False, hover=True, style={
                                            "marginBottom": "0"
                                        })
                                    )
                                ], style={
                                    "boxShadow": "0 0 5px rgba(0,0,0,0.1)",
                                    "border": "1px solid #dee2e6",
                                    "borderRadius": "8px"
                                }, className="mb-4")
                            ], width=3, className="ps-4 pe-4")
                        ], className="mb-4"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Select(
                                    id="sql-operation",
                                    options=[
                                        {"label": op, "value": op}
                                        for op in ["INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "UNION", "EXCEPT"]
                                    ],
                                    value="INNER JOIN",
                                    className="mb-3",
                                    style={
                                        "borderRadius": "8px",
                                        "boxShadow": "0 0 5px rgba(0,0,0,0.1)"
                                    }
                                ),
                                dbc.Button(
                                    "Perform",
                                    id="perform-sql-button",
                                    color="primary",
                                    className="mb-3",
                                    style={
                                        "borderRadius": "4px"
                                    }
                                ),
                                html.Div(id="sql-output", className="mt-3")
                            ])
                        ])
                    ], label="SQL", tab_id="sql")
                ], id="nested-tabs", active_tab="python", className="mt-4"),
            ], label="Try it", tab_id="tab-1"),
            
            dbc.Tab([
                dcc.Markdown('''```python
import os
from databricks.connect import DatabricksSession

cluster_id = "0709-132523-cnhxf2p6"

spark = DatabricksSession.builder.remote(
    host=os.getenv("DATABRICKS_HOST"),
    cluster_id=cluster_id
).getOrCreate()

# SQL operations example
a = "(VALUES (1, 'A1'), (2, 'A2'), (3, 'A3')) AS a(id, value)"
b = "(VALUES (2, 'B1'), (3, 'B2'), (4, 'B3')) AS b(id, value)"

# Inner join example
query = f"SELECT a.id, a.value AS value_a, b.value AS value_b FROM {a} INNER JOIN {b} ON a.id = b.id"
result = spark.sql(query).toPandas()
print(result)

# Generate sequence
result = spark.range(10).toPandas()
print(result)
```''', className="p-4 border rounded")
            ], label="Code snippet", tab_id="tab-2"),
            
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        html.H4("Permissions (app service principal)", className="mb-3"),
                        html.Ul([
                            dcc.Markdown("**```CAN ATTACH TO```** permission on the cluster")
                        ], className="mb-4")
                    ]),
                    dbc.Col([
                        html.H4("Databricks resources", className="mb-3"),
                        html.Ul([
                            html.Li("All-purpose compute")
                        ], className="mb-4")
                    ]),
                    dbc.Col([
                        html.H4("Dependencies", className="mb-3"),
                        html.Ul([
                            dcc.Markdown("* [Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html) - `databricks-connect`"),
                            dcc.Markdown("* [Dash](https://pypi.org/project/dash/) - `dash`")
                        ], className="mb-4")
                    ])
                ])
            ], label="Requirements", tab_id="tab-3")
        ], id="tabs", active_tab="tab-1", className="mb-4")
    ], fluid=True, className="py-4")

@callback(
    [Output("connection-status", "children"),
     Output("dataset-a-table", "children"),
     Output("dataset-b-table", "children")],
    [Input("cluster-id-input", "value")],
    prevent_initial_call=True
)
def update_connection(cluster_id):
    if not cluster_id:
        raise PreventUpdate
    
    try:
        spark = connect_to_cluster(cluster_id)
        session_info = {
            "App Name": spark.conf.get("spark.app.name", "Unknown"),
            "Master URL": spark.conf.get("spark.master", "Unknown"),
        }
        
        # Create sample datasets with styled tables
        def create_styled_table(data):
            header = html.Thead(html.Tr([
                html.Th("id", style={"backgroundColor": "#f8f9fa", "color": "#666"}),
                html.Th("value", style={"backgroundColor": "#f8f9fa", "color": "#666"})
            ]))
            
            body = html.Tbody([
                html.Tr([
                    html.Td(row["id"]),
                    html.Td(row["value"])
                ]) for _, row in data.iterrows()
            ])
            
            return dbc.Table([header, body], 
                           bordered=True,
                           hover=True,
                           size="sm",
                           style={"backgroundColor": "white"})
        
        df_a = pd.DataFrame({"id": [1, 2, 3], "value": ["A1", "A2", "A3"]})
        df_b = pd.DataFrame({"id": [2, 3, 4], "value": ["B1", "B2", "B3"]})
        
        return [
            html.Div([
                dbc.Alert("Successfully connected to Spark", color="success", className="mb-3"),
                dbc.Card(dbc.CardBody(dcc.Markdown(f"```json\n{session_info}\n```")))
            ]),
            create_styled_table(df_a),
            create_styled_table(df_b)
        ]
    except Exception as e:
        return dbc.Alert(f"Error connecting to cluster: {str(e)}", color="danger"), None, None

@callback(
    Output("python-output", "children"),
    [Input("generate-button", "n_clicks")],
    [State("cluster-id-input", "value"),
     State("data-points-input", "value")],
    prevent_initial_call=True
)
def generate_data(n_clicks, cluster_id, num_points):
    if not all([cluster_id, num_points]):
        raise PreventUpdate
    
    try:
        spark = connect_to_cluster(cluster_id)
        df = spark.range(num_points).toPandas()
        return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    except Exception as e:
        return dbc.Alert(f"Error generating data: {str(e)}", color="danger")

@callback(
    Output("sql-output", "children"),
    [Input("perform-sql-button", "n_clicks")],
    [State("cluster-id-input", "value"),
     State("sql-operation", "value")],
    prevent_initial_call=True
)
def perform_sql(n_clicks, cluster_id, operation):
    if not all([cluster_id, operation]):
        raise PreventUpdate
    
    try:
        spark = connect_to_cluster(cluster_id)
        a = "(VALUES (1, 'A1'), (2, 'A2'), (3, 'A3')) AS a(id, value)"
        b = "(VALUES (2, 'B1'), (3, 'B2'), (4, 'B3')) AS b(id, value)"
        
        if operation in ("INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN"):
            query = f"SELECT a.id, a.value AS value_a, b.value AS value_b FROM {a} {operation} {b} ON a.id = b.id"
        else:
            query = f"SELECT * FROM {a} {operation} SELECT * FROM {b}"
        
        result = spark.sql(query).toPandas()
        return dbc.Table.from_dataframe(result, striped=True, bordered=True, hover=True)
    except Exception as e:
        return dbc.Alert(f"Error executing SQL: {str(e)}", color="danger")

# Make layout available at module level
__all__ = ['layout']
