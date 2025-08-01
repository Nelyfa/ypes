#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# HTML шаблон для веб-интерфейса
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Зеркальное отображение текста - ypes</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            font-size: 1.1em;
        }
        textarea, input[type="text"] {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            box-sizing: border-box;
            resize: vertical;
        }
        textarea {
            min-height: 120px;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s;
            width: 100%;
            margin-top: 10px;
        }
        button:hover {
            background: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .api-info {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            font-size: 14px;
        }
        .api-info h3 {
            margin-top: 0;
            color: #FFD700;
        }
        code {
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔄 Зеркальное отображение текста</h1>
        
        <div class="input-group">
            <label for="text-input">Введите текст для зеркального отображения:</label>
            <textarea id="text-input" placeholder="Например: привет мир"></textarea>
        </div>
        
        <button onclick="mirrorText()">Отзеркалить текст</button>
        
        <div id="result" class="result" style="display: none;">
            <label>Результат:</label>
            <textarea id="result-text" readonly></textarea>
        </div>

        <div class="api-info">
            <h3>📡 API Документация</h3>
            <p><strong>POST /api/mirror</strong></p>
            <p>Тело запроса: <code>{"text": "ваш текст"}</code></p>
            <p>Ответ: <code>{"original": "ваш текст", "mirrored": "тскет шав"}</code></p>
            
            <p><strong>GET /api/mirror?text=ваш+текст</strong></p>
            <p>Ответ: <code>{"original": "ваш текст", "mirrored": "тскет шав"}</code></p>
        </div>

        <div class="footer">
            <p>🐳 Docker приложение ypes | Порт: 1</p>
            <p><a href="https://github.com/Nelyfa/ypes" style="color: #FFD700;">GitHub: Nelyfa/ypes</a></p>
        </div>
    </div>

    <script>
        async function mirrorText() {
            const input = document.getElementById('text-input').value;
            if (!input.trim()) {
                alert('Пожалуйста, введите текст!');
                return;
            }

            try {
                const response = await fetch('/api/mirror', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({text: input})
                });

                const data = await response.json();
                
                document.getElementById('result-text').value = data.mirrored;
                document.getElementById('result').style.display = 'block';
            } catch (error) {
                alert('Ошибка: ' + error.message);
            }
        }

        // Обработка Enter в textarea
        document.getElementById('text-input').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                mirrorText();
            }
        });
    </script>
</body>
</html>
"""

def mirror_text(text):
    """Функция для зеркального отображения текста"""
    return text[::-1]

@app.route('/')
def index():
    """Главная страница с веб-интерфейсом"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/mirror', methods=['POST', 'GET'])
def api_mirror():
    """API endpoint для зеркального отображения текста"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'text' not in data:
                return jsonify({'error': 'Требуется поле "text" в JSON'}), 400
            text = data['text']
        else:  # GET
            text = request.args.get('text', '')
            if not text:
                return jsonify({'error': 'Требуется параметр "text"'}), 400
        
        mirrored = mirror_text(text)
        
        return jsonify({
            'original': text,
            'mirrored': mirrored,
            'length': len(text),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'ypes-mirror'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1))
    app.run(host='0.0.0.0', port=port, debug=False)