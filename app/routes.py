from flask import current_app, jsonify, request, render_template
from .agents import run_graph # Assuming run_graph is in agents.py

@current_app.route('/')
def index():
    return render_template('index.html')

@current_app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message')

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Call the LangGraph agent executor
        agent_response = run_graph(user_input)

        return jsonify({"response": agent_response})

    except Exception as e:
        # Log the exception for debugging
        current_app.logger.error(f"Error in /chat endpoint: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500

# You can add more routes here
