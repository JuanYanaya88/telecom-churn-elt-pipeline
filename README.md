<div align="center">

# 📡 Telecom Churn ELT Pipeline

### Pipeline de datos end-to-end para análisis de fuga de clientes (churn)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.9-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-1.8-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

![License](https://img.shields.io/badge/Licencia-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Estado-En%20desarrollo-yellow?style=flat-square)

</div>

---

## 📋 Descripción

Pipeline **ELT** (Extract → Load → Transform) que ingesta datos de clientes de una telco desde la API pública del challenge **Telecom X (Alura Latam)**, los carga en **PostgreSQL**, los transforma con **dbt** siguiendo arquitectura por capas (staging → marts) y orquesta todo con **Apache Airflow**. El entorno completo se levanta con un solo comando gracias a **Docker Compose**.

**Objetivo de negocio:** disponibilizar datos limpios y modelados para analizar la evasión de clientes (churn) y alimentar dashboards y modelos predictivos.

## 🏗️ Arquitectura del Pipeline

```mermaid
flowchart LR
    subgraph Ingesta ["🔽 Ingesta"]
        A[API Telecom X<br/>JSON] --> B[extract_api.py<br/>Python + Requests]
    end

    subgraph Almacenamiento ["🗄️ Almacenamiento"]
        B --> C[(PostgreSQL<br/>schema: raw)]
    end

    subgraph Transformacion ["⚙️ Transformación · dbt"]
        C --> D[stg_customers<br/>staging: limpieza y tipado]
        D --> E[fct_churn<br/>mart: métricas de churn]
        D --> F[dim_customers<br/>mart: dimensión clientes]
    end

    subgraph Orquestacion ["🎯 Orquestación"]
        G[Apache Airflow<br/>DAG diario] -.->|programa y monitorea| B
        G -.-> C
        G -.-> D
    end

    E --> H[📊 BI / ML]
    F --> H
```

### Flujo diario del DAG

```mermaid
sequenceDiagram
    participant AF as Airflow
    participant EX as extract_api.py
    participant PG as PostgreSQL (raw)
    participant DBT as dbt

    AF->>EX: 1. extract_data (06:00 UTC)
    EX->>PG: 2. load_raw (COPY a schema raw)
    AF->>DBT: 3. dbt run (staging → marts)
    AF->>DBT: 4. dbt test (calidad de datos)
    DBT-->>AF: ✅ Pipeline OK / ❌ Alerta
```

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Rol |
|---|---|---|
| 🔽 Ingesta | ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white) `requests` `pandas` | Extracción desde API y carga a raw |
| 🗄️ Almacenamiento | ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) | Data warehouse local (schemas `raw` y `analytics`) |
| ⚙️ Transformación | ![dbt](https://img.shields.io/badge/-dbt-FF694B?style=flat-square&logo=dbt&logoColor=white) | Modelado SQL por capas + tests de calidad |
| 🎯 Orquestación | ![Airflow](https://img.shields.io/badge/-Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white) | Scheduling, reintentos y monitoreo |
| 📦 Infraestructura | ![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Entorno reproducible con Docker Compose |

## 📁 Estructura del Proyecto

```text
telecom-churn-elt-pipeline/
├── 📂 dags/                  # DAGs de Airflow (definición del pipeline)
│   └── churn_pipeline_dag.py
├── 📂 ingestion/             # Scripts de extracción y carga (EL)
│   └── extract_api.py
├── 📂 dbt/                   # Proyecto dbt (T de ELT)
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/          # Limpieza, tipado y renombrado (stg_*)
│       └── marts/            # Modelos de negocio (fct_*, dim_*)
├── 📂 tests/                 # Tests unitarios de los scripts Python
├── 📂 docs/                  # Documentación y diagramas
├── 🐳 docker-compose.yml     # Postgres + Airflow con un comando
├── 🔐 .env.example           # Variables de entorno (plantilla)
└── 📄 README.md
```

## 🚀 Despliegue Local

**Requisitos:** Docker y Docker Compose instalados.

```bash
# 1. Clonar el repositorio
git clone https://github.com/JuanYanaya88/telecom-churn-elt-pipeline.git
cd telecom-churn-elt-pipeline

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar el entorno (Postgres + Airflow)
docker-compose up -d

# 4. Abrir la UI de Airflow y activar el DAG
# http://localhost:8080  (usuario: airflow / contraseña: airflow)
```

```bash
# Ejecutar transformaciones dbt manualmente (opcional)
docker-compose exec airflow-scheduler bash -c "cd /opt/dbt && dbt run && dbt test"

# Apagar el entorno
docker-compose down
```

## ✅ Calidad de Datos

- Tests de **dbt**: `not_null`, `unique` y `accepted_values` sobre claves y campos críticos
- Reintentos automáticos y alertas de fallo configurados en el DAG de Airflow
- Datos crudos preservados en schema `raw` (auditabilidad y reproceso)

## 🗺️ Roadmap

- [x] Ingesta desde API y carga a PostgreSQL
- [x] Modelos staging y marts con dbt
- [x] Orquestación con Airflow + Docker Compose
- [ ] Migración del warehouse a BigQuery
- [ ] CI/CD con GitHub Actions (lint + dbt test en cada PR)
- [ ] Dashboard de churn en Looker Studio

## 👤 Autor

**Juan Yanaya** — Data Engineer en formación

[![GitHub](https://img.shields.io/badge/GitHub-JuanYanaya88-181717?style=flat-square&logo=github)](https://github.com/JuanYanaya88)
[![Email](https://img.shields.io/badge/Email-Contacto-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:juandasaenz.yanayaco@gmail.com)

> 💡 Proyecto de portafolio construido para demostrar prácticas modernas de ingeniería de datos: ELT, modelado por capas, testing y entornos reproducibles.
