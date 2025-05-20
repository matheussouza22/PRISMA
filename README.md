# 📊 PRISMA - Base de Dados de Horários de Transporte

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

## ✅ Tipos de ID no GTFS

| Tipo de ID   | Arquivo GTFS        | Finalidade                                                             |
| ------------ | ------------------- | ---------------------------------------------------------------------- |
| `agency_id`  | agency.txt          | Identifica a operadora do serviço (ex: Supervia, MetrôRio, CCR Barcas) |
| `route_id`   | routes.txt          | Identifica a linha ou ramal específico (ex: RAMAL_SARACURUNA)          |
| `trip_id`    | trips.txt           | Identifica uma viagem específica                                       |
| `service_id` | calendar.txt        | Identifica o conjunto de dias de operação                              |
| `stop_id`    | stops.txt           | Identifica cada parada ou estação                                      |
| `shape_id`   | shapes.txt          | Identifica a linha geográfica da rota no mapa                          |
| `fare_id`    | fare_attributes.txt | (Opcional) Identifica tarifas diferenciadas                            |

---

## 🎯 Modelos de ID por Modal

### 🚍 Ônibus

| Campo       | Exemplo                      |
| ----------- | ---------------------------- |
| `agency_id` | SMTR_RJ                      |
| `route_id`  | BUS_409_CENTRAL_PAVUNA       |
| `trip_id`   | BUS_409_SEG_0610             |
| `stop_id`   | CENTRAL_BUS, PAVUNA_TERMINAL |
| `shape_id`  | shape_BUS_409                |

---

### 🚇 Metrô

| Campo       | Exemplo                         |
| ----------- | ------------------------------- |
| `agency_id` | METRORIO                        |
| `route_id`  | METRO_L1_URUGUAI_GENERAL_OSORIO |
| `trip_id`   | METRO_L1_SEG_0700               |
| `stop_id`   | URUGUAI, GENERAL_OSORIO         |
| `shape_id`  | shape_METRO_L1                  |

---

### 🚆 Supervia (Trem)

| Campo       | Exemplo                      |
| ----------- | ---------------------------- |
| `agency_id` | SUPERVIA                     |
| `route_id`  | RAMAL_SARACURUNA             |
| `trip_id`   | SARACURUNA_SEG_0515          |
| `stop_id`   | SARACURUNA, CENTRAL_SUPERVIA |
| `shape_id`  | shape_SUPERVIA_SARACURUNA    |

---

### 🚈 VLT

| Campo       | Exemplo                         |
| ----------- | ------------------------------- |
| `agency_id` | VLT_CARIOCA                     |
| `route_id`  | VLT_L1_RODOVIARIA_PRAIA_FORMOSA |
| `trip_id`   | VLT_L1_SEG_0800                 |
| `stop_id`   | RODOVIARIA_VLT, PRAIA_FORMOSA   |
| `shape_id`  | shape_VLT_L1                    |

---

### ⛴️ Barcas

| Campo       | Exemplo                 |
| ----------- | ----------------------- |
| `agency_id` | CCR_BARCAS              |
| `route_id`  | BARCAS_NITEROI_PRAÇA_XV |
| `trip_id`   | BARCAS_SEG_0730         |
| `stop_id`   | PRAÇA_XV, NITEROI       |
| `shape_id`  | shape_BARCAS_NITEROI    |

---
