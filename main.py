from flask import Flask, render_template_string

app = Flask(__name__)

# База данных продуктов
PRODUCTS = [
    {"name": "Гречка", "carbs": 20},
    {"name": "Рис", "carbs": 79},
    {"name": "Картофель", "carbs": 17},
    {"name": "Яблоко", "carbs": 10},
    {"name": "Банан", "carbs": 23},
    {"name": "Хлеб", "carbs": 38},
    {"name": "Макароны", "carbs": 70},
    {"name": "Овсянка", "carbs": 64},
]

# HTML-шаблон с красивыми кнопками продуктов
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Калькулятор ХЕ</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #e0f7fa, #fce4ec);
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            transition: background 0.5s ease;
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            font-weight: 500;
            font-size: 24px;
            color: #333;
        }
        .input-group {
            display: flex;
            align-items: center;
            margin-bottom: 16px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            padding: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .input-group:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        .input-group i {
            margin: 0 10px;
            font-size: 20px;
            transition: opacity 0.3s ease;
        }
        input {
            width: 100%;
            padding: 10px;
            border: none;
            background: transparent;
            color: #333;
            font-size: 16px;
            outline: none;
        }
        .result {
            margin-top: 20px;
            text-align: center;
        }
        .result p {
            margin: 10px 0;
            font-size: 18px;
            font-weight: 500;
            color: #333;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .result i {
            margin-right: 10px;
            font-size: 20px;
        }
        #xe_result, #insulin_result {
            color: #ff6f61;
            font-weight: bold;
            transition: opacity 0.3s ease;
        }
        .product-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }
        .product-buttons button {
            background: #ff6f61;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.3s ease, transform 0.3s ease;
            flex: 1 1 calc(50% - 10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .product-buttons button:hover {
            background: #ff3b2f;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Калькулятор ХЕ</h1>

        <div class="input-group">
            <i>🌾</i>
            <input type="number" step="0.1" id="carbs" name="carbs" oninput="calculateXE()" placeholder="Углеводы на 100 г" inputmode="decimal">
        </div>

        <div class="input-group">
            <i>⚖️</i>
            <input type="number" step="0.1" id="portion" name="portion" oninput="calculateXE()" placeholder="Порция (г)" inputmode="decimal">
        </div>

        <div class="result">
            <p><i>🍞</i>ХЕ: <span id="xe_result">0.0</span></p>
            <p><i>💉</i>Инсулин: <span id="insulin_result">0</span></p>
        </div>

        <div class="product-buttons">
            {% for product in products %}
                <button onclick="setCarbs({{ product.carbs }})">{{ product.name }}</button>
            {% endfor %}
        </div>
    </div>

    <script>
        // Рассчитываем ХЕ и инсулин
        function calculateXE() {
            const carbs = parseFloat(document.getElementById("carbs").value) || 0;
            const portion = parseFloat(document.getElementById("portion").value) || 0;
            const xe = (carbs * portion) / (100 * 10); // 1 ХЕ = 10 г углеводов
            const insulin = Math.round(xe * 2); // 1 ХЕ = 2 ЕД инсулина
            document.getElementById("xe_result").textContent = xe.toFixed(1);
            document.getElementById("insulin_result").textContent = insulin;
        }

        // Устанавливаем углеводы при выборе продукта
        function setCarbs(carbs) {
            document.getElementById("carbs").value = carbs;
            calculateXE();
        }

        // Ограничиваем ввод только цифрами и точкой
        document.getElementById("carbs").addEventListener("input", function (e) {
            e.target.value = e.target.value.replace(/[^0-9.]/g, "").replace(/(\..*)\./g, "$1");
        });

        document.getElementById("portion").addEventListener("input", function (e) {
            e.target.value = e.target.value.replace(/[^0-9.]/g, "").replace(/(\..*)\./g, "$1");
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, products=PRODUCTS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
