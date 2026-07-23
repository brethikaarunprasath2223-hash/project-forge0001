from flask import Blueprint, render_template, request, jsonify

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/ai-guide")
def ai_guide():
    return render_template("ai_guide.html")


@ai_bp.route("/ask-ai", methods=["POST"])
def ask_ai():

    data = request.get_json()

    question = data.get("question", "")

    
    answer = f"""
    You asked: {question}

    AI Mentor suggestion:
    Start by understanding your project requirements,
    choose the right technology, and create a step-by-step roadmap.
    """

    return jsonify({
        "answer": answer
    })