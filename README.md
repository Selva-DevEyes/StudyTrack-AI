# StudyTrack AI — Intelligent Full-Stack Learning & Trainee Management Platform

StudyTrack AI is a production-ready, full-stack academic learning and trainee management application built with **FastAPI**, **SQLAlchemy**, **SQLite**, **Pydantic**, handwritten custom algorithms, a deterministic offline AI assistant, and a vanilla HTML/CSS/JS frontend.

---

## 1. Project Overview & Author Identification

**Capstone Project Author**: **SelvamSDE**

StudyTrack AI provides academic administrators and trainees with a unified dashboard to:
- Manage student rosters and enrolled courses with full CRUD capabilities.
- Perform high-performance client/server data sorting and binary searching using handwritten algorithms.
- Generate aggregated roster reports based on customizable age criteria using database-level SQL aggregations.
- Utilize an offline AI Study Assistant for structured note summarization and vector-based semantic note search.

---

## 2. Technology Stack

- **Backend Framework**: Python 3.10+ / FastAPI (high performance, async ASGI framework)
- **ORM / Database**: SQLAlchemy 2.0 / SQLite
- **Data Validation & Serialization**: Pydantic v2 (custom field validators & schema definitions)
- **ASGI Web Server**: Uvicorn
- **Frontend**: Plain HTML5, Modern Vanilla CSS3, JavaScript (ES6+ with Event Delegation)
- **Testing**: pytest, httpx, FastAPI TestClient
- **Version Control**: Git

---

## 3. Architecture

StudyTrack AI uses a single-process architecture where FastAPI handles API routes, executes custom algorithm/AI modules, manages database state via SQLAlchemy, and serves the static frontend directly.

```text
[ Browser / Frontend Client ]
        │  (relative HTTP requests / static assets)
        ▼
[ FastAPI Server (Uvicorn) ] ── (CORS Middleware: http://localhost:5500)
   ├── Static Files Middleware (serves frontend/ index.html, style.css, app.js)
   ├── REST API Endpoints (/students/, /courses/, /assistant/)
   ├── Handwritten Algorithms Module (algorithms.py)
   ├── Offline Deterministic AI Service (ai_service.py)
   └── CRUD Layer (crud.py)
        ▼
   [ SQLAlchemy ORM (models.py) ]
        ▼
   [ SQLite Database (studytrack.db) ]
```

---

## 4. Folder Structure

```text
studytrack/
├── backend/
│   ├── main.py            # FastAPI app initialization, routes, CORS & static file mounting
│   ├── database.py        # SQLAlchemy engine, SessionLocal, Base, and DB dependency
│   ├── models.py          # SQLAlchemy models (Student, Course) with bidirectional relationships
│   ├── schemas.py         # Pydantic schemas with email and age field validation
│   ├── crud.py            # Database CRUD functions & SQL aggregate queries
│   ├── algorithms.py      # Handwritten Insertion Sort, Binary Search, and counting algorithms
│   ├── ai_service.py      # Offline mock AI summarizer, 12-dim embedding, cosine similarity
│   ├── seed_data.py       # Seed script populating exact 8 initial student records
│   ├── test_app.py        # Comprehensive Pytest end-to-end test suite
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── index.html         # Semantic HTML layout with single h1, forms, and roster grid
│   ├── style.css          # Responsive styling system with @media (max-width: 600px) grid
│   └── app.js             # Vanilla JS DOM manipulation & event delegation
├── .env.example           # Sample environment variables configuration
├── .gitignore             # Git ignore definitions for virtualenv, database, cache
└── README.md              # Comprehensive documentation and setup guide
```

---

## 5. Installation & Setup

### Prerequisites
- Python 3.10 or higher installed on your system.
- Git installed.

---

## 6. Virtual Environment Setup

### Windows (PowerShell / Command Prompt)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 7. Requirements Installation

Install all required Python packages using pip:
```bash
pip install -r backend/requirements.txt
```

Dependencies installed:
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `pydantic`
- `httpx`
- `pytest`

---

## 8. Database Setup & Seeding

The SQLite database (`studytrack.db`) is automatically initialized and seeded when you first start the FastAPI server.

Seeding logic (`backend/seed_data.py`) executes ONLY when the `Student` table is completely empty, inserting the exact 8 initial student records:

1. **Aditi Rao** (`aditi.rao@example.com`, Age: 22)
2. **Rohan Mehta** (`rohan.mehta@example.com`, Age: 19)
3. **Kavya Nair** (`kavya.nair@example.com`, Age: 25)
4. **Farhan Sheikh** (`farhan.sheikh@example.com`, Age: 18)
5. **Priya Iyer** (`priya.iyer@example.com`, Age: 21)
6. **Devansh Gupta** (`devansh.gupta@example.com`, Age: 23)
7. **Meera Joshi** (`meera.joshi@example.com`, Age: 20)
8. **Sameer Khan** (`sameer.khan@example.com`, Age: 24)

---

## 9. Exact Run Command

Start the Uvicorn web server from the project root directory:

```bash
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Once running, access:
- **Web Interface**: `http://127.0.0.1:8000/`
- **Swagger Interactive API Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc API Documentation**: `http://127.0.0.1:8000/redoc`

---

## 10. Frontend Usage

1. Open `http://127.0.0.1:8000/` in any modern browser.
2. **Add Student**: Fill out the form in the left sidebar (Name, Email, Age) and click **+ Add Student**. The student card immediately appears in the roster without a full page reload.
3. **Save Age**: On any student card, edit the age number input and click **Save Age**. A `PATCH` request updates the record and updates the displayed badge upon success.
4. **Delete Student**: Click **Delete** on any card. A `DELETE` request removes the student from the database and removes the card element from the DOM.
5. **Sort Roster**: Use the dropdown menu to select "Age (Ascending)" or "Name (Alphabetical)" to trigger the handwritten Insertion Sort.
6. **Binary Search**: Type an exact student name (e.g. `Kavya Nair`) into the Binary Search input and click **Search**.
7. **Roster Report**: Click **Generate Report** to compute an age-filtered report using custom counting logic.
8. **AI Note Summarizer**: Paste lecture text in the AI panel and click **Summarize Notes**.
9. **Semantic Search**: Enter a search query in the AI Knowledge Base Search to rank default notes by cosine similarity.

---

## 11. Complete API Endpoints

### Student Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/students/` | Create a new student (Requires unique email & age > 0) |
| `GET` | `/students/` | Retrieve all students (Supports `?min_age=<n>`) |
| `GET` | `/students/sorted` | Retrieve students sorted by field using Insertion Sort (`?by=age\|name`) |
| `GET` | `/students/search` | Search student by exact name using iterative Binary Search (`?name=<str>`) |
| `GET` | `/students/report` | Generate text report & count meeting min age threshold (`?min_age=<n>`) |
| `GET` | `/students/{student_id}` | Retrieve single student details by ID |
| `PATCH` | `/students/{student_id}` | Update student attributes by ID |
| `DELETE` | `/students/{student_id}` | Delete student record by ID |
| `GET` | `/students/{student_id}/course-count` | Get enrolled course count via SQL aggregate |

### Course Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/courses/` | Create a new course for a student (Credits 1-6) |
| `GET` | `/courses/` | Retrieve all course records |
| `GET` | `/courses/{course_id}` | Retrieve single course details by ID |
| `PATCH` | `/courses/{course_id}` | Update course attributes by ID |
| `DELETE` | `/courses/{course_id}` | Delete course record by ID |

### AI Assistant Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/assistant/summarize` | Summarize study text into topic, key points, difficulty |
| `GET` | `/assistant/search` | Rank 5 study notes by cosine similarity score (`?query=<str>`) |

---

## 12. CRUD Examples

### Create Student
```bash
curl -X POST "http://127.0.0.1:8000/students/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Ananya Sharma", "email": "ananya.sharma@example.com", "age": 21}'
```

### Update Student Age
```bash
curl -X PATCH "http://127.0.0.1:8000/students/1" \
     -H "Content-Type: application/json" \
     -d '{"age": 23}'
```

### Create Course for Student
```bash
curl -X POST "http://127.0.0.1:8000/courses/" \
     -H "Content-Type: application/json" \
     -d '{"course_name": "Data Structures & Algorithms", "credits": 4, "student_id": 1}'
```

### Get Course Count (SQL Aggregate)
```bash
curl -X GET "http://127.0.0.1:8000/students/1/course-count"
```
Response:
```json
{
  "student_id": 1,
  "course_count": 1
}
```

---

## 13. Algorithms Explanation

The `backend/algorithms.py` module contains purely handwritten Python implementations without relying on prohibited Python built-ins like `.sort()` or `sorted()` inside the algorithm body.

---

## 14. Insertion Sort Complexity & Implementation

### Algorithm Code Structure
```python
def insertion_sort_by_field(students, field):
    arr = list(students)
    n = len(arr)
    for i in range(1, n):
        key_item = arr[i]
        key_val = get_val(key_item, field)
        j = i - 1
        while j >= 0 and get_val(arr[j], field) > key_val:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr
```

### Complexity Analysis
- **Best Case Time Complexity**: \(O(n)\) — When array is already sorted; inner while loop checks once and terminates.
- **Worst Case Time Complexity**: \(O(n^2)\) — When array is reverse sorted; requires \(n(n-1)/2\) comparisons and shifts.
- **Average Case Time Complexity**: \(O(n^2)\)
- **Space Complexity**: \(O(1)\) auxiliary space (in-place modification on array copy).

---

## 15. Binary Search Complexity & Sorted Requirement

### Algorithm Code Structure
```python
def binary_search_by_name(sorted_by_name_list, name):
    low = 0
    high = len(sorted_by_name_list) - 1
    while low <= high:
        mid = low + (high - low) // 2  # Overflow-safe midpoint
        mid_name = sorted_by_name_list[mid].name
        if mid_name == name:
            return sorted_by_name_list[mid]
        elif mid_name < name:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

### Complexity & Requirements
- **Prerequisite Requirement**: The input list **MUST BE SORTED** alphabetically by `name` before calling `binary_search_by_name`. If the list is unsorted, dividing search intervals based on midpoint comparisons fails to eliminate half the elements correctly.
- **Midpoint Formula**: Uses `mid = low + (high - low) // 2` to avoid integer overflow issues present in `(low + high) // 2` in bounded languages.
- **Time Complexity**: \(O(\log n)\) — Halves the remaining search domain in each iteration.
- **Space Complexity**: \(O(1)\) auxiliary space.

---

## 16. AI Demonstration Mode Declaration (`AI_MODE=mock`)

> [!IMPORTANT]
> **Grading Demonstration Mode**: `AI_MODE=mock` is used for all grading demonstrations and evaluation. The application runs 100% offline, locally, and deterministically without external API network calls or paid LLM services. No API keys or secret credentials are committed anywhere in the repository.

---

## 17. AI Summarizer Rules

The `summarize_notes(raw_text)` function applies the following deterministic rules:
1. **Topic**: Extracted as the first non-empty line of text (or `"untitled"` if empty).
2. **Key Points**: First 3 non-empty sentences extracted by splitting on sentence boundary punctuation (`.`, `!`, `?`).
3. **Difficulty Rating**:
   - Word count < 40 words \(\rightarrow\) `"easy"`
   - Word count 40 to 100 words \(\rightarrow\) `"medium"`
   - Word count > 100 words \(\rightarrow\) `"hard"`
4. **Empty / Whitespace Input**: Returns exactly:
   ```json
   {
     "topic": "untitled",
     "key_points": [],
     "difficulty": "easy"
   }
   ```

---

## 18. Embedding Vocabulary

Vector representations are constructed over an exact 12-word fixed vocabulary:
```python
VOCABULARY = [
    "sort",
    "search",
    "binary",
    "insertion",
    "sql",
    "join",
    "fastapi",
    "pydantic",
    "prompt",
    "llm",
    "database",
    "validate"
]
```

Text is tokenized by converting to lowercase and splitting on non-alphanumeric character sequences (`re.split(r'[^a-z0-9]+', text.lower())`). Token frequencies for each vocabulary word are counted to produce a 12-dimensional numerical vector.

---

## 19. Cosine Similarity Explanation

Cosine similarity measures the angle between two vectors in 12-dimensional vector space:

\[
\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^{12} A_i B_i}{\sqrt{\sum_{i=1}^{12} A_i^2} \sqrt{\sum_{i=1}^{12} B_i^2}}
\]

Implementation from first principles:
```python
def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    mag_a = math.sqrt(sum(a * a for a in vec1))
    mag_b = math.sqrt(sum(b * b for b in vec2))
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0
    return dot_product / (mag_a * mag_b)
```

---

## 20. Zero-Vector Behavior

When a query contains no vocabulary words (e.g. `"xyz 123"`), its 12-dimensional embedding vector contains all zeros (\([0.0, \dots, 0.0]\)).

In this case:
- Magnitude of the vector is `0.0`.
- The `cosine_similarity` function catches `mag_a == 0.0` or `mag_b == 0.0` and immediately returns `0.0`.
- It **never raises `ZeroDivisionError`**.
- Semantic search returns all 5 default notes with a score of `0.0`, preserving their original note ID order (`1, 2, 3, 4, 5`) without crashing.

---

## 21. AI Helper Usage

- **Summarization**: Enter notes into the textarea under **Study Note Summarizer** and click **Summarize Notes**. The rendered card displays the extracted topic, difficulty badge (`easy`, `medium`, `hard`), and bulleted key points.
- **Semantic Search**: Type terms like `"sql join"` or `"binary search"` in the query field and click **Search Notes**. The results display the 5 study notes ranked in descending order of cosine similarity score.

---

## 22. Real LLM Prompt Documentation

Although StudyTrack AI uses an offline mock implementation for evaluation and grading, below is the exact production prompt structure that would be sent to an online LLM (e.g. OpenAI GPT-4o or Google Gemini 1.5 Pro) for structured JSON note summarization:

```text
System:
You are an expert academic tutor and structured summarization engine.
Your task is to analyze study notes provided by a student and output a valid JSON object matching the schema below.

Output JSON Schema:
{
  "topic": "string (Main subject title of the notes)",
  "key_points": ["string (3 concise bullet points summarizing core concepts)"],
  "difficulty": "string (One of: 'easy', 'medium', 'hard')"
}

Rules:
1. "topic" must summarize the core subject in 2-6 words.
2. "key_points" must contain exactly 3 clear, educational key points extracted from the text.
3. "difficulty" must be determined based on concept complexity ('easy' for introductory definitions, 'medium' for procedural explanations, 'hard' for complex multi-concept architectures).
4. Do not include markdown code fence wrappers or extra conversational text. Return raw JSON only.

User Input:
<STUDENT_STUDY_NOTES>
{{student_notes_text}}
</STUDENT_STUDY_NOTES>
```

---

## 23. Testing & Verification Steps

Run the automated Pytest test suite from the project root:

```bash
python -m pytest backend/test_app.py -v
```

Test coverage includes:
- Startup database table creation and automatic seeding (8 students).
- Pydantic custom field validators (email `@` check and age `gt=0`).
- Duplicate student email rejection (400 Bad Request).
- Student and Course CRUD routes.
- SQL aggregate `func.count(Course.id)` course count endpoint.
- Handwritten Insertion Sort by age and name.
- Iterative Binary Search by exact name and 404 error handling.
- Roster report generation and custom age counting loop.
- Offline AI note summarizer and difficulty classification.
- 12-dimensional vector embedding, cosine similarity, and zero-vector safety.

---

## 24. Git Workflow & Feature Branch History

This repository is maintained as ONE single public repository following a strict Git feature branch workflow:

### Feature Branch Commands & Merge Workflow
```bash
# 1. Initialize repository on main branch
git init
git add .
git commit -m "Initial commit - StudyTrack AI complete platform"
git branch -M main
git remote add origin https://github.com/Selva-DevEyes/StudyTrack-AI.git

# 2. Create and switch to feature branch
git checkout -b feature/algorithms-and-ai

# 3. Make multiple commits on feature branch
git add backend/algorithms.py && git commit -m "Refine insertion sort in-place helper and roster report format"
git add backend/ai_service.py && git commit -m "Tune AI mock rules and id field schema"

# 4. Push feature branch to remote
git push -u origin feature/algorithms-and-ai

# 5. Merge feature branch into main preserving commit history with --no-ff
git checkout main
git merge --no-ff feature/algorithms-and-ai -m "Merge branch 'feature/algorithms-and-ai' into main"

# 6. Push main branch to remote
git push -u origin main
```

---

## 25. Security & Credentials Notice

> [!NOTE]
> **No secret keys, API credentials, `.env` files, or virtual environments (`.venv/`) are committed to this repository.** The application runs 100% locally and offline out of the box using SQLite and mock AI vector algorithms.
