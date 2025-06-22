# 🧠 TriviaDev — Programming Trivia API

TriviaDev is a toy backend project built to practice modern Python development.  
It simulates a trivia game where users can answer questions about programming topics like Git, Python, Linux, Networking, and more.

This project is part of a personal learning journey, inspired by the curriculum at [Boot.dev](https://boot.dev), and aims to apply skills related to:

- REST API design with FastAPI
- Database management using SQLite
- Data modeling with SQLAlchemy
- API schema validation with Pydantic
- Authentication and authorization with JWT
- API documentation with Swagger / OpenAPI

---

## 🧪 Getting Started

> Note: Python 3.11+ is recommended.

```bash
# 1. Clone the repo
git clone https://github.com/your-username/code-trivia.git
cd code-trivia

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
uvicorn app.main:app --reload

# 5. Visit Swagger UI
http://localhost:8000/docs
```

## ⚠️ Disclaimer

This is a learning project. The codebase is not intended for production use. Contributions, suggestions, or feedback are welcome!

📘 License

This project is licensed under the MIT License.