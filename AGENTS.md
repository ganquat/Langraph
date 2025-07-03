## Project: Multi-Agent LangGraph with Gemini and Flask

This project implements a multi-agent system using LangGraph, Google's Gemini Pro model, and a Flask API.

### Project Structure:

- **`run.py`**: The main entry point to start the Flask application.
- **`requirements.txt`**: Lists all Python dependencies.
- **`.env`**: Configuration file for environment variables (e.g., `GOOGLE_API_KEY`). **Note:** This file is in `.gitignore` and should not be committed. A `.env.example` or clear setup instruction is crucial.
- **`.gitignore`**: Specifies intentionally untracked files that Git should ignore.
- **`app/`**: Contains the core application logic.
    - **`__init__.py`**: Initializes the Flask application and imports routes.
    - **`agents.py`**: Defines the LangGraph agents, their tools (if any), and the graph structure. It sets up the connections between agents and how they process information.
    - **`routes.py`**: Defines the Flask API endpoints (e.g., `/chat` for interacting with the agent system).
- **`templates/`**: Contains HTML templates for the frontend.
    - **`index.html`**: A simple web interface to send messages to the agent system and display responses.
- **`static/`**: (Currently empty) Can be used for static files like CSS or JavaScript if the frontend becomes more complex.

### How to Run:

1.  **Clone the repository.**
2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your environment variables:**
    -   Copy the contents of `.env.example` (if provided) to a new file named `.env`, or create `.env` manually.
    -   Add your Google Gemini API key to the `.env` file:
        ```
        GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
        ```
5.  **Run the Flask application:**
    ```bash
    python run.py
    ```
6.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

### Agent Workflow (Conceptual):

The `app/agents.py` file defines the core logic:

1.  **User Input**: Received via the Flask `/chat` endpoint.
2.  **Researcher Agent**: Takes the user input, potentially uses tools (like a search function) to gather initial information or clarify the query.
3.  **Planner Agent**: Receives information from the researcher and formulates a plan or a structured approach to address the user's request.
4.  **Final Responder Agent**: Synthesizes the information from previous agents and the plan to generate a final, coherent response to the user.
5.  **Output**: The final response is sent back to the user via the Flask API.

The LangGraph library manages the state and transitions between these agents.

### Notes for Development:

*   **API Key**: Ensure `GOOGLE_API_KEY` is correctly set in `.env`. The application will warn you if it's missing or set to the placeholder.
*   **Gemini Model**: The `app/agents.py` currently uses `gemini-1.0-pro`. You can change this to other compatible models like `gemini-1.5-flash` if needed, but ensure your API key has access to it.
*   **Error Handling**: Basic error handling is in place in `app/routes.py` and `app/agents.py`. Check Flask console output and browser console for errors.
*   **Tool Implementation**: The `simple_search` tool in `app/agents.py` is a placeholder. For real functionality, this would need to be connected to an actual search API or database.
*   **LangGraph Complexity**: This is a basic multi-agent setup. LangGraph allows for much more complex graphs, conditional routing, and state management. Refer to the LangGraph documentation for advanced features.
