import eel
import os

import middle.mid_utils

if __name__ == '__main__':
    try:
        print('[Info]: запуск приложения...')
        eel.init(os.path.join(os.path.dirname(__file__), "front"))
        eel.start('index.html', mode="firefox", size=(1500, 800))
    except Exception as e:
        print(f'[Error]: при запуске программы\n\n{e}\n')