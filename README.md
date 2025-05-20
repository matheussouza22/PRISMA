# 📊 TESTE PRISMA - Base de Dados de Horários de Transporte

Este repositório contém um banco de dados com horários de saída dos modais do RJ, extraídos de forma automatizada. A base foi desenvolvida para fins de análise de transporte público e planejamento logístico no município do Rio de Janeiro.

---

## 📁 Arquivos incluídos

- `bd_transportes.db`: Banco de dados SQLite contendo os horários por linha, origem, destino e tipo de dia.
- `gtfs_supervia.ipynb`: Notebook de construção do feed GTFS para o Ramal Saracuruna.
- Scripts Python (em breve): Automatização do processo de coleta e leitura dos dados.

---

## 🚀 Como clonar este repositório

Com HTTPS:

```bash
git clone https://github.com/matheussouza22/PRISMA.git
```

---

```
⸻

✅ Tipos de ID no GTFS

| Tipo de ID  | Arquivo GTFS         | Finalidade                                                             |
|-------------|----------------------|------------------------------------------------------------------------|
| agency_id   | agency.txt           | Identifica a operadora do serviço (ex: Supervia, MetrôRio, CCR Barcas) |
| route_id    | routes.txt           | Identifica a linha ou ramal específico (ex: RAMAL_SARACURUNA)         |
| trip_id     | trips.txt            | Identifica uma viagem específica                                       |
| service_id  | calendar.txt         | Identifica o conjunto de dias de operação                              |
| stop_id     | stops.txt            | Identifica cada parada ou estação                                      |
| shape_id    | shapes.txt           | Identifica a linha geográfica da rota no mapa                          |
| fare_id     | fare_attributes.txt  | (Opcional) Identifica tarifas diferenciadas                            |




⸻

🎯 Modelos de ID por Modal
Claro! Aqui está a versão corrigida e formatada do trecho do seu `README.md` com as **tabelas corretamente formatadas em Markdown** para exibição no GitHub:



## ✅ Tipos de ID no GTFS

| Tipo de ID   | Arquivo GTFS         | Finalidade                                                             |
| ------------ | -------------------- | ---------------------------------------------------------------------- |
| `agency_id`  | agency.txt           | Identifica a operadora do serviço (ex: Supervia, MetrôRio, CCR Barcas) |
| `route_id`   | routes.txt           | Identifica a linha ou ramal específico (ex: RAMAL\_SARACURUNA)         |
| `trip_id`    | trips.txt            | Identifica uma viagem específica                                       |
| `service_id` | calendar.txt         | Identifica o conjunto de dias de operação                              |
| `stop_id`    | stops.txt            | Identifica cada parada ou estação                                      |
| `shape_id`   | shapes.txt           | Identifica a linha geográfica da rota no mapa                          |
| `fare_id`    | fare\_attributes.txt | (Opcional) Identifica tarifas diferenciadas                            |

---

## 🎯 Modelos de ID por Modal

### 🚍 Ônibus

| Campo       | Exemplo                        |
| ----------- | ------------------------------ |
| `agency_id` | SMTR\_RJ                       |
| `route_id`  | BUS\_409\_CENTRAL\_PAVUNA      |
| `trip_id`   | BUS\_409\_SEG\_0610            |
| `stop_id`   | CENTRAL\_BUS, PAVUNA\_TERMINAL |
| `shape_id`  | shape\_BUS\_409                |

---

### 🚇 Metrô

| Campo       | Exemplo                             |
| ----------- | ----------------------------------- |
| `agency_id` | METRORIO                            |
| `route_id`  | METRO\_L1\_URUGUAI\_GENERAL\_OSORIO |
| `trip_id`   | METRO\_L1\_SEG\_0700                |
| `stop_id`   | URUGUAI, GENERAL\_OSORIO            |
| `shape_id`  | shape\_METRO\_L1                    |

---

### 🚆 Supervia (Trem)

| Campo       | Exemplo                       |
| ----------- | ----------------------------- |
| `agency_id` | SUPERVIA                      |
| `route_id`  | RAMAL\_SARACURUNA             |
| `trip_id`   | SARACURUNA\_SEG\_0515         |
| `stop_id`   | SARACURUNA, CENTRAL\_SUPERVIA |
| `shape_id`  | shape\_SUPERVIA\_SARACURUNA   |

---

### 🚈 VLT

| Campo       | Exemplo                             |
| ----------- | ----------------------------------- |
| `agency_id` | VLT\_CARIOCA                        |
| `route_id`  | VLT\_L1\_RODOVIARIA\_PRAIA\_FORMOSA |
| `trip_id`   | VLT\_L1\_SEG\_0800                  |
| `stop_id`   | RODOVIARIA\_VLT, PRAIA\_FORMOSA     |
| `shape_id`  | shape\_VLT\_L1                      |

---

### ⛴️ Barcas

| Campo       | Exemplo                    |
| ----------- | -------------------------- |
| `agency_id` | CCR\_BARCAS                |
| `route_id`  | BARCAS\_NITEROI\_PRAÇA\_XV |
| `trip_id`   | BARCAS\_SEG\_0730          |
| `stop_id`   | PRAÇA\_XV, NITEROI         |
| `shape_id`  | shape\_BARCAS\_NITEROI     |

---
```
