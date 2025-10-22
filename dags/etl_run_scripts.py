from datetime import timedelta
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

# Ruta raíz del proyecto dentro del contenedor
REPO = "/opt/airflow/project"
PY = "python"

default_args = {
    "owner": "etl",
    "retries": 0,  # sin reintentos durante debugging
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="etl_run_scripts",
    description="Orquesta tus scripts (extract -> transform -> load) + notebook",
    start_date=pendulum.datetime(2025, 10, 1, tz="UTC"),
    schedule=None,  # equivalente a schedule_interval=None
    catchup=False,
    default_args=default_args,
    tags=["etl", "papermill"],
):

    # 0) Depuración del entorno
    debug = BashOperator(
        task_id="debug_env",
        bash_command=(
            f"cd {REPO} && pwd && {PY} -V && "
            "echo 'Contenido del proyecto:' && ls -la && "
            "echo 'Contenido de dataExtraction:' && ls -la dataExtraction || true"
        ),
    )

    # 1) Extraer datos
    extract = BashOperator(
        task_id="extract",
        bash_command=f"cd {REPO} && {PY} dataExtraction/dfExtraction.py",
        env={"PYTHONPATH": REPO},
    )

    # 2) Ejecutar notebook Jupyter directamente en raíz
    run_notebook = BashOperator(
        task_id="run_notebook",
        bash_command=(
            f"cd {REPO} && "
            "mkdir -p output_notebooks && "
            f"python -m papermill --kernel airflow_py  integration.ipynb "
            "output_notebooks/EDA_output_{{ ds_nodash }}.ipynb"
        ),
        env={"PYTHONPATH": REPO},
    )

    # 3) Transformar datos
    transform = BashOperator(
        task_id="transform",
        bash_command=f"cd {REPO} && {PY} dataTransform/resultTransformation.py",
        env={"PYTHONPATH": REPO},
    )

    # 4) Cargar datos
    load = BashOperator(
        task_id="load",
        bash_command=f"cd {REPO} && {PY} Load/dataLoad.py",
        env={"PYTHONPATH": REPO},
    )

    # Definición del flujo
    debug >> extract >> run_notebook >> transform >> load
