from datetime import datetime, timedelta
from fastapi import APIRouter


docs_router = APIRouter(prefix="/very/important/docs",
                        responses={404: {"description": "Not found"}})


@docs_router.get("/")
def get_docs_older(documents_date: int):
    """
    Банковское API каких- то важных документов.
    """
    response = {"Columns": database["Columns"],
                "Description": "Банковское API каких- то важных документов",
                "RowCount": len(database["Rows"])
                }

    start_of_day = datetime.fromtimestamp(documents_date)
    start_of_next_day = start_of_day + timedelta(days=1)

    rows = [row for row in database["Rows"] if
            start_of_day <= datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') < start_of_next_day]

    response["Rows"] = rows
    return response


database = {
    "Columns": ["key1", "key2", "key3"],
    "Rows": [
        ["1", "2020-04-21 15:45:57", "key3_value1"],
        ["2", "2020-04-21 11:59:06", "key3_value2"],
        ["3", "2024-05-23 23:04:21", "key3_value3"],
    ]
}
