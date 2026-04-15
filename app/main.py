# main.py

import sys
from pathlib import Path

# Running `python app/main.py` puts `app/` on sys.path, not the repo root.
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# If invoked as a script outside this project's venv, re-exec with ./venv (symlinked
# interpreters can share the same resolved binary as system Python but not site-packages).
if __name__ == "__main__":
    _venv_dir = (_root / "venv").resolve()
    if _venv_dir.is_dir() and Path(sys.prefix).resolve() != _venv_dir:
        import os

        for _venv_name in ("python3", "python"):
            _venv_py = _venv_dir / "bin" / _venv_name
            if _venv_py.is_file():
                os.execv(str(_venv_py), [str(_venv_py), str(Path(__file__).resolve()), *sys.argv[1:]])
                break

import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:

    def load_dotenv(*_args, **_kwargs):
        return False


from openai import OpenAI
from evaluation.evaluator import evaluate_response

# Load the environment variables from the .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_response(user_query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict customer support agent. Only give policy-based answers."},
            {"role": "user", "content": user_query}
        ],
        temperature=0
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    query = "What is the refund policy?"
    answer = get_ai_response(query)
    evaluation = evaluate_response(query, answer)
    print("\nEvaluation:\n", evaluation)

# Run the app (from repo root):
#   python3 app/main.py   (uses ./venv when present)
#   python -m app.main
