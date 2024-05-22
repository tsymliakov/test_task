# Задание 6*

# Имеется банковское API возвращающее JSON
# {
#     "Columns": ["key1", "key2", "key3"],
#     "Description": "Банковское API каких-то важных документов",
#     "RowCount": 2,
#     "Rows": [
#         ["value1", "value2", "value3"],
#         ["value4", "value5", "value6"]
#     ]
# }
# Основной интерес представляют значения полей "Columns" и "Rows",
# которые соответственно являются списком названий столбцов и значениями столбцов
# Необходимо:
#     1. Получить JSON из внешнего API
#         ендпоинт: GET https://api.gazprombank.ru/very/important/docs?documents_date={"начало дня сегодня в виде таймстемп"}
#         (!) ендпоинт выдуманный
#     2.1 Валидировать входящий JSON используя модель pydantic
#         (из ТЗ известно что поле "key1" имеет тип int, "key2"(datetime), "key3"(str))
#     2.2 Представить данные "Columns" и "Rows" в виде плоского csv-подобного pandas.DataFrame
#     3.1 В полученном DataFrame произвести переименование полей по след. маппингу
#         "key1" -> "document_id", "key2" -> "document_dt", "key3" -> "document_name"
#     3.2 Полученный DataFrame обогатить доп. столбцом:
#         "load_dt" -> значение "сейчас"(датавремя)
# *реализовать п.1 с использованием Apache Airflow HttpHook


# from datetime import datetime
from os import getcwd
from pathlib import Path
import requests
import logging
import pandas
from pydantic import ValidationError
from task_6.pydantic_models import APIResponse
from datetime import datetime, date


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("Логер")


def get_dataframe_from_response(
    columns: list[str] = ["column1", "column2", "column3"],
    rows: list[tuple[int, int, int]] = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9)]) -> pandas.DataFrame:
    """В целях сближения с литерой S принципов SOLID, в функцию залетают
    лишь два списка, а не весь ответ от внешнего API.
    """
    df = pandas.DataFrame(rows, columns=columns)
    LOGGER.info("\nCreated dataframe from response.\n")
    return df


def get_response(url: str) -> APIResponse:
    try:
        r = requests.get(url)
    except requests.RequestException as e:
        logging.error(e)
        return

    if r.status_code != 200:
        logging.error(
            f"Status code {r.status_code}.\
Failed to get response from server.\n\
{r.text}\n")
        return

    LOGGER.info(
        f"\n1. Got response from server. Status code {r.status_code}\n")

    try:
        response = APIResponse.model_validate_json(r.text)
        LOGGER.info("\n2.1. Validation succeed.\n")
    except ValidationError as e:
        LOGGER.error(e.json(indent=4))
        return

    LOGGER.info(
        f"\nResponse from server :\n\n{response.model_dump_json(indent=4)}\n")

    return response


def export_df_like_csv(dt: pandas.DataFrame, path: str = '.') -> None:
    try:
        # Было бы хорошо писать в файл в режиме дописывания, но как писал
        # Дональд Кнут: "Преждевременная оптимизация - корень всех зол"

        # Было бы лучше писать в файл с бОльшей гарантией не переписать
        # существующий. Но в каких- то ситуациях будет достаточно и такого
        # подхода.
        datetime_now = datetime.now().strftime("%d-%m %H_%M_%S")
        filename = f"exported_response-{datetime_now}.csv"
        file_path = Path(path) / filename
        dt.to_csv(f"{file_path}",
                  sep="|", encoding="utf-8",
                  index=False)

        with open(f"{file_path}") as f:
            LOGGER.info(
                f"\n2.2. Dataframe was succesfully exported to csv file \
{file_path.resolve()}:\n{f.read()}")
    except PermissionError:
        logging.error(
            f"Unable to export data to {getcwd()}. Operation not permitted.")
    except Exception as e:
        raise SystemExit(e)


def get_dt_with_renamed_fields(df: pandas.DataFrame,
                               map: dict[str, str]) -> pandas.DataFrame:
    dt_renamed_columns = df.rename(columns=map)
    logging.info(
        f"\n3.1. Dataframe with renamed columns:\n{dt_renamed_columns}\n")
    return dt_renamed_columns


def _get_datetime_now_str() -> str:
    return datetime.now().strftime("%d.%m.%Y_%H:%M:%S")


def add_column_to_df(df: pandas.DataFrame,
                     new_column_name: str,
                     new_value_getter: callable,
                     *args,
                     **kwrags) -> pandas.DataFrame:
    """
    new_value_getter : функция- геттер, которая должна вернуть значение для
    колонки.
    args и kwargs - передаются на вход функции new_value_getter

    Такой подход - один из способов повторного использования уже имеющегося
    кода.
    """

    # Чтобы сделать функцию чистой, прибегаю к копированию DataFrame.
    # В случае необходимости (недостаточной производительности), возможно
    # запустить код под профилировщиком и взвесив за и против, провести
    # оптимизацию этого места
    addition_column_df = df.copy()
    addition_column_df["load_dt"] = [
        new_value_getter(*args, **kwrags) for _ in range(len(df))]

    logging.info(
        f"\n3.2. Dataframe with additional column:\n{addition_column_df}\n")

    return addition_column_df


def main():
    start_of_today = datetime.combine(date.today(), datetime.min.time())
    start_of_today_timestamp = int(start_of_today.timestamp())
    url = f"http://localhost:8000/very/important/docs/?\
documents_date={start_of_today_timestamp}"

    response = get_response(url)

    if type(response) is not APIResponse:
        raise SystemExit(
            "Unable to continue work because of uncorrect response")

    if response.RowCount == 0:
        # Сервер может и обмануть. Но кому тогда вообще верить?
        LOGGER.info("\nNo rows to process\n")
        return

    df = get_dataframe_from_response(response.Columns, response.Rows)
    export_df_like_csv(df)

    renamed_df = get_dt_with_renamed_fields(df, map={
        "key1": "document_id",
        "key2": "document_dt",
        "key3": "document_name"})

    df_additional_column = add_column_to_df(renamed_df,
                                            "load_dt",
                                            _get_datetime_now_str)

    LOGGER.warning("\nК сожалению с Appache у меня нет опыта, но это лишь \
вопрос времени в случае необходимости")


if __name__ == "__main__":
    """
    Для запуска uvicorn-fastapi-сервера потребуется команда

    `uvicorn --app-dir ./task_6/ server:app`
    """
    main()
