#ArtGround

##Overview


## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Virtual environment tool (recommended: `venv`)

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/AnkurGarg07/ArtGround.git
    cd ArtGround
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
    ```
   
3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Start the development server**:
    ```bash
    python manage.py runserver
    ```