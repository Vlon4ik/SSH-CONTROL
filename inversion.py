import mouse
import pyautogui
import threading
import time

# Получаем размер экрана
screen_width, screen_height = pyautogui.size()

# Переменные для хранения предыдущих координат мыши
prev_x, prev_y = pyautogui.position()

# Флаг для остановки бесконечного цикла
running = True

# Функция для обработки событий перемещения мыши
def on_move(event):
    global prev_x, prev_y
    
    if isinstance(event, mouse.MoveEvent) and running:
        x, y = event.x, event.y
        
        # Вычисляем смещение мыши
        dx = x - prev_x
        dy = y - prev_y
        
        # Вычисляем новые координаты, двигая мышь в противоположную сторону
        new_x = prev_x - dx
        new_y = prev_y - dy
        
        # Перемещаем мышь в новые координаты
        pyautogui.moveTo(new_x, new_y)

        # Обновляем предыдущие координаты мыши
        prev_x, prev_y = pyautogui.position()

# Функция для бесконечного нажатия кнопок мыши
def click_forever():
    while running:
        mouse.click('left')
        mouse.click('right')
        time.sleep(0.1)  # небольшая задержка для предотвращения избыточного нажатия

# Функция для завершения работы скрипта через 15 секунд
def stop_after_delay():
    global running
    time.sleep(15)
    running = False
    mouse.unhook(on_move)  # Отменяем привязку к событию движения мыши

# Запуск функции отслеживания движений мыши в отдельном потоке
def start_mouse_tracking():
    mouse.hook(on_move)
    mouse.wait()

# Запуск бесконечного нажатия кнопок мыши в отдельном потоке
click_thread = threading.Thread(target=click_forever)
click_thread.start()

# Запуск отслеживания движений мыши
tracking_thread = threading.Thread(target=start_mouse_tracking)
tracking_thread.start()

# Запуск таймера для остановки через 15 секунд
stop_timer_thread = threading.Thread(target=stop_after_delay)
stop_timer_thread.start()

# Ожидание завершения всех потоков
click_thread.join()
tracking_thread.join()
stop_timer_thread.join()