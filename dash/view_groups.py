groups = [
    {
        "views": [
            {
                "label": "Introduction",
                "help": "",
                "page": "views/book_intro.py",
                "icon": "material-symbols:skillet-cooktop",
            },
        ],
    },
    {
        "title": {"text": "Tables", "icon": "material-symbols:table-view"},
        "views": [
            {
                "label": "Read a table",
                "help": "Query a Unity Catalog Delta table.",
                "page": "views/tables_read.py",
                "icon": "material-symbols:table-view",
            },
            {
                "label": "Edit a table",
                "help": "Interactively edit a Delta table in the UI.",
                "page": "views/tables_edit.py",
                "icon": "material-symbols:edit-document",
            },
        ],
    },
    {
        "title": {"text": "Volumes", "icon": "material-symbols:folder"},
        "views": [
            {
                "label": "Upload a file",
                "help": "Upload a file into a Unity Catalog Volume.",
                "page": "views/volumes_upload.py",
                "icon": "material-symbols:publish",
            },
            {
                "label": "Download a file",
                "help": "Download a Volume file.",
                "page": "views/volumes_download.py",
                "icon": "material-symbols:download",
            },
        ],
    },
    {
        "title": {"text": "AI / ML", "icon": "material-symbols:model-training"},
        "views": [
            {
                "label": "Invoke a model",
                "help": "Invoke a model across classical ML and Large Language with UI inputs.",
                "page": "views/ml_serving_invoke.py",
                "icon": "material-symbols:experiment",
            },
            {
                "label": "Run vector search",
                "help": "Use Mosaic AI to generate embeddings for textual data and perform vector search.",
                "page": "views/ml_vector_search.py",
                "icon": "material-symbols:search",
            },
        ],
    },
    {
        "title": {"text": "Business Intelligence", "icon": "material-symbols:analytics"},
        "views": [
            {
                "label": "AI/BI Dashboard",
                "help": "Embed an AI/BI dashboard.",
                "page": "views/embed_dashboard.py",
                "icon": "material-symbols:dashboard",
            },
        ],
    },
    {
        "title": {"text": "Workflows", "icon": "material-symbols:settings-suggest"},
        "views": [
            {
                "label": "Trigger a job",
                "help": "Trigger a job with job parameters.",
                "page": "views/workflows_run.py",
                "icon": "material-symbols:valve",
            },
            {
                "label": "Retrieve job results",
                "help": "Retrieve results for a Workflow Job run.",
                "page": "views/workflows_get_results.py",
                "icon": "material-symbols:account-tree",
            },
        ],
    },
    {
        "title": {"text": "Compute", "icon": "material-symbols:computer"},
        "views": [
            {
                "label": "Connect",
                "help": "Transform data at scale with UI inputs.",
                "page": "views/compute_connect.py",
                "icon": "material-symbols:lan",
            },
        ],
    },
    {
        "title": {"text": "Authentication", "icon": "material-symbols:security"},
        "views": [
            {
                "label": "Get current user",
                "help": "Get current App user information.",
                "page": "views/users_get_current.py",
                "icon": "material-symbols:fingerprint",
            },
            {
                "label": "Retrieve a secret",
                "help": "Get a sensitive API key without hard-coding it.",
                "page": "views/secrets_retrieve.py",
                "icon": "material-symbols:lock",
            },
        ],
    },
]
