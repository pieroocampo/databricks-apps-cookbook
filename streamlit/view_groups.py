groups = [
    {
        "views": [
            {
                "label": "Introduction",
                "help": "",
                "page": "views/book_intro.py",
                "icon": ":material/skillet_cooktop:",
            },
        ],
    },
    {
        "title": "Tables",
        "views": [
            {
                "label": "Read a table",
                "help": "Query a Unity Catalog Delta table.",
                "page": "views/tables_read.py",
                "icon": ":material/table_view:",
            },
            {
                "label": "Edit a table",
                "help": "Interactively edit a Delta table in the UI.",
                "page": "views/tables_edit.py",
                "icon": ":material/edit_document:",
            },
        ],
    }
]