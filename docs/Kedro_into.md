# Kedro

Comprehensive Kedro Guide

## 1. What is Kedro?
Kedro is an open-source Python framework for building production-ready data pipelines. It applies software engineering best practices (modularity, separation of concerns, versioning) to data science projects. Think of it as "project scaffolding" for machine learning workflows.

## 2. Core Concepts

### a) Project Structure 

A Kedro project has a standardized layout:

```
my_project/
├── conf/           # Configuration (parameters, credentials)
├── data/           # Local datasets (not versioned)
├── docs/           # Documentation
├── notebooks/      # Jupyter notebooks
├── src/            # Source code
│   └── my_project/
│       ├── nodes/  # Data processing functions
│       ├── pipelines/ # Pipeline definitions
│       └── __init__.py
├── tests/          # Unit tests
└── pyproject.toml  # Dependencies

```

b) Key Components

- Nodes: Pure Python functions (e.g., clean_data(raw_df) -> cleaned_df).

    - Input: Data from catalog

    - Output: Processed data saved to catalog

-   Pipelines: Collections of nodes connected via data dependencies

```bash
pipeline = Pipeline([
    node(clean_data, "raw_data", "cleaned_data"),
    node(train_model, "cleaned_data", "model")
])
```

-   Data Catalog: `conf/base/catalog.yml` defines datasets:

```bash
raw_data:
  type: pandas.CSVDataSet
  filepath: data/01_raw/raw.csv
model:
  type: pickle.PickleDataSet
  filepath: data/06_models/model.pkl
  ```

-   Parameters: conf/base/parameters.yml stores settings (e.g., test_size: 0.2).

### 3. Technical Workflow

1.  Create Project:
    ```bash
    kedro new
    ```

2.  Develop Nodes: Write functions in ```src/my_project/nodes/data_processing.py.```

3.  Build Pipeline: Connect nodes in ```src/my_project/pipelines/data_science.py.```

4.  Configure Data: Add datasets to ```catalog.yml.```

5. Run Pipeline:

```bash
kedro run
```

6. Visualize:

```bash
kedro viz  # Opens browser-based DAG visualizer
```

### 4. Integration with Domino + GitLab + Airflow

#### a) Domino Data Lab

##### 1. Setup:

-   Link GitLab repo to Domino project.
-   Add kedro to requirements.txt.

##### 2. Run Pipeline:

-   Use Domino Jobs to execute `kedro run`.
-   Mount datasets via Domino's `/mnt` paths in `catalog.yml`.

##### 3.Example catalog.yml:

```bash
raw_data:
  type: pandas.CSVDataSet
  filepath: /mnt/data/raw.csv
```

#### b) GitLab

##### 1. Version Control:

- Store code, conf/, and src/ in GitLab.

- Exclude data/, logs/, and credentials.yml via .gitignore.

#####  2. CI/CD (.gitlab-ci.yml):

```bash
test_pipeline:
  image: python:3.8
  script:
    - pip install kedro
    - kedro install
    - kedro test  # Run unit tests
```

#### c) Airflow (Production Scheduling)

##### 1. Generate DAG:

```bash
kedro airflow create  # Creates Airflow DAG .py file
```

##### 2. Deploy:

-   Place the generated DAG in Airflow's dags/ folder.

##### 3. Run in Airflow:

- Trigger DAGs via Airflow UI or API.

#### 5. Advantages

-   `Reproducibility`: Catalog tracks data versions; pipelines rerun identically.

-   `Modularity`: Nodes/pipelines enable team collaboration.

-   `Portability`: Runs anywhere (local, cloud, Domino, Airflow).

-   `Best Practices`: Built-in testing, logging, and configuration.

- `Visualization:` kedro viz for pipeline debugging.


#### 6. Disadvantages

-   Learning Curve: Requires understanding of pipelines/catalogs.

-   Overhead: May be excessive for tiny projects.

-   Debugging: Node failures require inspecting intermediate datasets.

-   Limited Cloud Integration: Needs custom setup for cloud storage (S3, GCS).


#### 7. When to Use Kedro?

-   Multi-step ML/data pipelines

-   Team collaboration projects

-   Production deployments (via Airflow/AWS Batch)

-   One-off scripts or exploratory analysis
