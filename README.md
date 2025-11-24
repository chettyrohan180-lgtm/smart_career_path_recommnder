# Smart Career Recommender

> A lightweight career recommendation engine that matches student profiles with possible career paths using NLP and a simple recommender model.


## Table of contents

* [Project overview](#project-overview)
* [Repository structure](#repository-structure)
* [Data](#data)
* [Key modules and design](#key-modules-and-design)

  * [Models](#models)
  * [Services](#services)
  * [Utils](#utils)
* [Setup & installation](#setup--installation)
* [Usage examples](#usage-examples)
* [Testing](#testing)
* [Development notes & TODOs](#development-notes--todos)
* [Contributing](#contributing)
* [License](#license)


## Project overview

This project implements a small pipeline for recommending careers to students based on profile information (skills, interests, courses, grades, etc.). The pipeline is split into modular components:

* **data**: raw CSV and other static inputs (example careers dataset).
* **models**: domain classes and a recommender model implementation.
* **services**: higher-level logic that performs NLP, profile management and career matching.
* **utils**: helpers for loading data and visualising results.
* **tests**: unit tests for core functionality.

The design keeps domain objects (e.g. `Student`, `Career`) separate from processing logic so you can swap models or add features easily.


## Repository structure

```
/ (repo root)
├─ data/
│  └─ careers.csv            # example dataset of careers and metadata
├─ models/
│  ├─ career.py              # Career dataclass / domain model
│  ├─ recommender_model.py   # Recommender model (fit/predict abstraction)
│  └─ student.py             # Student profile dataclass / domain model
├─ services/
│  ├─ career_matcher.py      # Orchestrates matching students -> careers
│  ├─ nlp_processor.py       # NLP preprocessing, embeddings, TF-IDF etc.
│  ├─ path_generator.py      # Creates possible learning/career paths
│  └─ profile_manager.py     # CRUD helpers for student profiles
├─ utils/
│  ├─ data_loader.py         # Load CSVs and create domain objects
│  └─ visualizer.py          # Plotting / result visualisations
├─ tests/
│  ├─ test_matching.py
│  └─ test_profiles.py
├─ main.py                   # Example CLI / script entrypoint
├─ README.md
└─ requirements.txt
```


## Data

Place any datasets in the `data/` folder. `data/careers.csv` is provided as an example and should contain fields such as `career_id`, `title`, `description`, `skills`, and other metadata used by the NLP pipeline.

If you add large datasets or trained models, **do not** commit them to the repository — instead store them in a remote artifact store or add them to `.gitignore`.


## Key modules and design

Below is a short explanation of each package and the responsibilities of the important modules. Refer to the module-level docstrings for exact class / function signatures.

### Models

* `models/career.py` — defines the `Career` domain model (likely a `dataclass`) containing fields like `id`, `title`, `description`, `skills` and helpers to serialize/deserialize.
* `models/student.py` — defines the `Student` domain model storing a student's profile: name/id, skills, interests, academic background and any other attributes used for matching.
* `models/recommender_model.py` — contains a compact recommender abstraction. Typical methods:

  * `fit(careers_corpus)` — builds internal indices or trains (TF-IDF, embeddings, or nearest-neighbours).
  * `predict(student_profile, top_k=5)` — returns the top-k career recommendations for a given profile.

> Note: Check docstrings in `recommender_model.py` for the exact class and method names. The sample usage below shows a common pattern.

### Services

* `services/nlp_processor.py` — text preprocessing utilities: tokenization, stemming/lemmatization, stopword removal and vectorisation (TF-IDF or embeddings). This module centralises all NLP decisions so the rest of the code can call `nlp_processor.preprocess(text)` or `nlp_processor.embed(texts)`.

* `services/profile_manager.py` — functions for creating/updating/deleting `Student` objects and for converting raw JSON or dict input into typed `Student` instances.

* `services/career_matcher.py` — orchestrates matching: it coordinates loading careers, calling the `RecommenderModel`, post-processing results (scoring explanation, filtering), and optionally building a suggested learning path.

* `services/path_generator.py` — given a match, this module assembles recommended next steps (courses, minor projects, resources) into a directed path for the student.

### Utils

* `utils/data_loader.py` — convenience functions for reading `data/careers.csv` and returning a list of `Career` domain objects ready for the model.
* `utils/visualizer.py` — quick plotting helpers to visualise match scores, skill overlap, and suggested pathways.


## Setup & installation

**Requirements**

* Python 3.10+ (recommended)
* `pip` and a virtual environment tool (venv)

**Local setup (macOS / Linux)**

```bash
# clone the repo
git clone <repo-url>
cd <repo-root>

# create a virtual environment
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

If you need to add a dependency, update `requirements.txt` and re-run `pip install -r requirements.txt`.

---

## Usage examples

Below are short examples showing how you might use the code. These snippets are intentionally generic — inspect each module's docstrings for exact names.

### Quick script example (interactive)

```python
# example_usage.py
from utils.data_loader import load_careers
from models.student import Student
from models.recommender_model import RecommenderModel
from services.career_matcher import CareerMatcher

# Load careers from CSV
careers = load_careers('data/careers.csv')

# Build / train the recommender
recommender = RecommenderModel()
recommender.fit(careers)

# Create a student profile
s = Student(id='u123', name='Alice', skills=['python','machine learning'], interests=['data science'])

# Match careers
matcher = CareerMatcher(recommender)
results = matcher.match(s, top_k=5)

print('Top matches:')
for r in results:
    print(f"{r['career'].title} — score: {r['score']:.3f}")
```

### Running the included example script

Run the top-level script to see a demo (if present):

```bash
python main.py
```

`main.py` typically demonstrates loading the data, instantiating the pipeline and printing or storing results. You can pass CLI flags to point to different CSVs or to enable verbose logging.


## Testing

This repository includes basic tests in the `tests/` folder. Use `pytest` to run them:

```bash
# from repo root, with venv active
pytest -q
```

Add tests when you extend the codebase. Aim to keep unit tests fast and mock any heavy NLP or model training.


## Development notes & TODOs

* Add better docstrings and typing to all public functions (use `mypy` for static checks).
* Add caching for embeddings (to avoid recomputing on every run).
* Provide a pre-trained model artifact or script to serialise the trained indices (e.g. to `models/`) for faster start-up.
* Add a lightweight web API (FastAPI / Flask) that accepts a JSON student profile and returns matches in JSON.


## Contributing

1. Fork the repo and create a feature branch (`git checkout -b feat/my-feature`).
2. Write code and tests.
3. Run tests locally: `pytest -q`.
4. Open a PR with a clear description of changes.

Please use `black` and `flake8` (or your preferred formatter/linter) for consistent style.

