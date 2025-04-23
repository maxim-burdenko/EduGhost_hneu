import json
from typing import Any
from datetime import datetime

class CustomSchedule:

    def __init__(self, path_to_file:str):
        self.path = path_to_file


    def save_schedule(self, data:dict):
        try:
            try:
                with open(self.path, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = {}

            existing_data.update(data)

            with open(self.path, 'w', encoding='utf-8') as file:
                file.write(json.dumps(existing_data, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f'[Error]: при вставке данных в JSON\n\n{e}\n\n')

    def get_schedule(self) -> dict:
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f'[Error] при получении расписания\n\n{e}\n\n')
            return {}

    def generate_custom_schedule(self) -> list[Any] | None:
        data = self.get_schedule()
        today = datetime.now().strftime('%A')

        if not data: print('[Info]: личного расписания нет'); return None
        if not today in data: print(f'[Info]: нет сегодняшнего дня "{today}" в расписание'); return None

        return data[today]






