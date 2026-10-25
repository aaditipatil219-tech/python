
from flask import Flask, request, render_template_string

app = Flask(__name__)

questions = [
    {"question": "What is the capital of India?",
     "answer": ["delhi"]},
    {"question": "What is the capital of Karnataka?",
     "answer": ["bangalore", "bengaluru"]},
    {"question": "What is the capital of Maharashtra?",
     "answer": ["mumbai"]},
    {"question": "What is the capital of Telangana?",
     "answer": ["hyderabad"]},
    {"question": "What is the capital of Gujarat?",
     "answer": ["gandhinagar", "gandhi nagar"]}
]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capital Quest Quiz</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #dbeafe, #f3e8ff);
            min-height: 100vh;
            padding: 30px 15px;
            color: #25264a;
        }

        .container {
            max-width: 720px;
            margin: auto;
        }

        header {
            text-align: center;
            margin-bottom: 25px;
        }

        header .emoji {
            font-size: 48px;
        }

        header h1 {
            color: #4f46e5;
            font-size: 36px;
            margin: 12px 0;
        }

        header p {
            color: #686980;
        }

        .quiz-card {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 12px 35px #3730a320;
        }

        .info {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .badge {
            background: #eef2ff;
            color: #4f46e5;
            padding: 9px 13px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: bold;
        }

        .question {
            padding: 18px;
            border: 1px solid #e5e7f5;
            background: #fcfcff;
            border-radius: 13px;
            margin-bottom: 17px;
        }

        .question label {
            display: block;
            font-weight: bold;
            line-height: 1.5;
            margin-bottom: 12px;
        }

        .number {
            color: #6366f1;
        }

        input {
            width: 100%;
            padding: 13px;
            border: 1px solid #d1d5e5;
            border-radius: 9px;
            font-size: 15px;
            outline: none;
        }

        input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px #6366f120;
        }

        .feedback {
            margin-top: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        .correct {
            color: #15803d;
        }

        .wrong {
            color: #dc2626;
        }

        .result {
            background: #f1f0ff;
            padding: 25px;
            text-align: center;
            border-radius: 14px;
            margin-top: 20px;
        }

        .result h2 {
            color: #4f46e5;
        }

        .score {
            font-size: 38px;
            font-weight: bold;
            margin: 12px;
        }

        button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(90deg, #4f46e5, #9333ea);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
            transition: 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px #4f46e540;
        }

        footer {
            text-align: center;
            color: #777;
            margin-top: 20px;
            font-size: 13px;
        }

        @media (max-width: 500px) {
            .quiz-card {
                padding: 18px;
            }

            header h1 {
                font-size: 29px;
            }
        }
    </style>
</head>

<body>
<div class="container">

    <header>
        <div class="emoji">🌍</div>
        <h1>Capital Quest</h1>
        <p>How well do you know India's state capitals?</p>
    </header>

    <div class="quiz-card">

        <div class="info">
            <span class="badge">🧠 Geography Quiz</span>
            <span class="badge">5 Questions</span>
        </div>

        <form method="POST">

            {% for q in questions %}
            <div class="question">
                <label for="answer_{{ loop.index0 }}">
                    <span class="number">
                        {{ "%02d" | format(loop.index) }}.
                    </span>
                    {{ q.question }}
                </label>

                <input
                    type="text"
                    id="answer_{{ loop.index0 }}"
                    name="answer_{{ loop.index0 }}"
                    placeholder="Enter your answer..."
                    value="{{ answers[loop.index0] }}"
                    autocomplete="off"
                    required
                >

                {% if submitted %}
                    {% if results[loop.index0] %}
                    <div class="feedback correct">
                        ✓ Correct answer!
                    </div>
                    {% else %}
                    <div class="feedback wrong">
                        ✗ Wrong answer.
                        Correct answer: {{ q.answer[0].title() }}
                    </div>
                    {% endif %}
                {% endif %}
            </div>
            {% endfor %}

            {% if submitted %}
            <div class="result">
                <h2>
                    {% if score == 5 %}
                        🎉 Perfect Score!
                    {% elif score >= 3 %}
                        👏 Good Job!
                    {% else %}
                        💪 Keep Practicing!
                    {% endif %}
                </h2>

                <div class="score">
                    {{ score }} / {{ questions|length }}
                </div>

                <p>You scored {{ score * 20 }}%</p>
            </div>
            {% endif %}

            <button type="submit">
                {% if submitted %}
                    Check Again
                {% else %}
                    Submit Answers
                {% endif %}
            </button>

        </form>
    </div>

    <footer>
        Made with ❤️ using Python, Flask, HTML & CSS
    </footer>

</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    submitted = request.method == "POST"
    answers = []
    results = []
    score = 0

    for i, q in enumerate(questions):
        if submitted:
            answer = request.form.get(
                f"answer_{i}", ""
            ).strip().lower()
        else:
            answer = ""

        answers.append(answer)

        if submitted:
            correct = answer in q["answer"]
            results.append(correct)

            if correct:
                score += 1

    return render_template_string(
        HTML,
        questions=questions,
        answers=answers,
        results=results,
        score=score,
        submitted=submitted
    )


if __name__ == "__main__":
    app.run(debug=True)
