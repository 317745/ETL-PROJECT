from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

REPO = "/opt/airflow/project"  # <-- raiz de ETL-PROJECT-MAIN
PY = "python"

default_args = {
    "owner": "etl",
    "retries": 0,  # sin reintentos mientras debuggeamos
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="etl_run_scripts",
    description="Orquesta tus scripts (extract -> transform -> load)",
    start_date=datetime(2025, 10, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
):
    # Opcional: imprime contexto para depurar PATH y archivos
    debug = BashOperator(
        task_id="debug_env",
        bash_command=f'cd {REPO} && pwd && {PY} -V && ls -la && ls -la dataExtraction || true'
    )

    extract = BashOperator(
        task_id="extract",
        bash_command=f"cd {REPO} && {PY} dataExtraction/dfExtraction.py",
        env={"PYTHONPATH": REPO},  # ayuda a imports relativos
    )

    transform = BashOperator(
        task_id="transform",
        bash_command=f"cd {REPO} && {PY} dataTransform/resultTransformation.py",
        env={"PYTHONPATH": REPO},
    )

    load = BashOperator(
        task_id="load",
        bash_command=f"cd {REPO} && {PY} Load/dataLoad.py",
        env={"PYTHONPATH": REPO},
    )

    debug >> extract >> transform >> load
