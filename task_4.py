import os
import time


def delete_old_files(directory, days):
    current_time = time.time()
    age_in_seconds = days * 24 * 60 * 60

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            file_mod_time = os.path.getmtime(file_path)
            if current_time - file_mod_time > age_in_seconds:
                os.remove(file_path)
                print(f"Удален файл: {file_path}")


if __name__ == "__main__":
    delete_old_files("./folder", 0)
