from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

# Получаем абсолютные пути к скриптам
base_dir = os.path.dirname(os.path.abspath(__file__))
play_pause_script = os.path.join(base_dir, 'play_pause.py')
next_track_script = os.path.join(base_dir, 'next_track.py')
previous_track_script = os.path.join(base_dir, 'previous_track.py')
history_track_script = os.path.join(base_dir, 'history.py')
inversion_script = os.path.join(base_dir, 'inversion.py')  # Добавлен путь к inversion.py

@app.route('/playpause', methods=['POST'])
def play_pause():
    return execute_script(play_pause_script)

@app.route('/next', methods=['POST'])
def next_track():
    return execute_script(next_track_script)

@app.route('/previous', methods=['POST'])
def previous_track():
    return execute_script(previous_track_script)

@app.route('/history', methods=['POST'])
def history_track():
    return execute_script(history_track_script)

@app.route('/haus', methods=['POST'])
def inversion():
    return execute_script(inversion_script)  # Исправлено на правильный путь к inversion.py

def execute_script(script):
    try:
        result = subprocess.run(["python", script], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'result': 'success', 'output': result.stdout})
        else:
            return jsonify({'result': 'error', 'output': result.stderr}), 500
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print(f"Running server with base directory: {base_dir}")
    app.run(host='0.0.0.0', port=5000)  # Запуск Flask сервера на всех интерфейсах на порту 5000