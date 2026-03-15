# 09 — Linux Machine Specifications for Causal Atlas

> **Last updated:** March 2025
> **Status:** Research document — hardware recommendations for development and deployment
> **Important note on RAM pricing:** As of late 2025, DDR5 RAM prices have surged 80-130% due to global AI-driven DRAM shortages. Prices quoted here reflect the elevated market. Monitor pricing trends before purchasing.

---

## Table of Contents

1. [Workload Analysis](#1-workload-analysis)
2. [Development Machine Specifications](#2-development-machine-specifications)
3. [Server / Production Deployment](#3-server--production-deployment)
4. [Storage Architecture](#4-storage-architecture)
5. [Software Stack Requirements](#5-software-stack-requirements)
6. [Performance Benchmarks and Estimates](#6-performance-benchmarks-and-estimates)
7. [GPU Considerations](#7-gpu-considerations)
8. [Networking and Data Transfer](#8-networking-and-data-transfer)
9. [Monitoring and Operations](#9-monitoring-and-operations)
10. [Specific Hardware Recommendations (March 2025 Pricing)](#10-specific-hardware-recommendations-march-2025-pricing)
11. [Comparison: Self-Hosted vs Cloud](#11-comparison-self-hosted-vs-cloud)
12. [Detailed Benchmarking Plan](#12-detailed-benchmarking-plan)
13. [Power and Cooling](#13-power-and-cooling)
14. [Data Sovereignty and Legal](#14-data-sovereignty-and-legal)
15. [Backup and Disaster Recovery](#15-backup-and-disaster-recovery)
16. [Network Architecture](#16-network-architecture)
17. [Complete Build Guides](#17-complete-build-guides)

---

## 1. Workload Analysis

Causal Atlas combines several distinct computational workloads. Understanding each is essential for sizing hardware correctly.

### 1.1 Data Storage Estimates

| Dataset | Raw Size (approx.) | Processed/Parquet (est.) | Notes |
|---------|-------------------|-------------------------|-------|
| CHIRPS daily (1981-present) | ~80-100 GB | ~30-40 GB | 0.05deg global rasters, NetCDF/GeoTIFF |
| GDELT (Events + GKG) | ~3-4 TB (BigQuery) | ~200-500 GB (filtered subset) | Full GKG alone is 3.6 TB; Causal Atlas only needs event aggregates per grid cell |
| ACLED | ~500 MB - 1 GB | ~200-400 MB | Point events, growing ~50 MB/year |
| MODIS/VIIRS NDVI (monthly, 1km) | ~100-200 GB | ~20-40 GB | 16-day composites, 2000-present |
| VIIRS Nighttime Lights (monthly) | ~50-100 GB | ~15-30 GB | Monthly composites, 463m resolution, 2012-present |
| UCDP-GED | ~200-300 MB | ~100-200 MB | Point events, annual releases |
| WFP food prices | ~200-500 MB | ~100-200 MB | Tabular, market-level |
| USGS earthquakes | ~1-2 GB | ~500 MB - 1 GB | Point events with magnitudes |
| OpenAQ air quality | ~5-20 GB | ~2-5 GB | Station-level measurements |
| EM-DAT | ~50-100 MB | ~20-50 MB | Disaster events |
| World Bank indicators | ~1-5 GB | ~500 MB - 2 GB | Country-level time series |
| FAO data | ~2-5 GB | ~1-3 GB | Agricultural statistics |
| HDX/HAPI | ~1-5 GB | ~500 MB - 2 GB | Various humanitarian indicators |
| PRIO-GRID reference | ~500 MB - 1 GB | ~200-500 MB | Grid cell metadata and static variables |
| Disease outbreaks (WHO, IHME) | ~1-5 GB | ~500 MB - 2 GB | Various formats |
| **Total raw data** | **~250-550 GB** | — | Excluding full GDELT |
| **Total with GDELT subset** | **~500 GB - 1 TB** | — | Using filtered/aggregated GDELT |
| **Total processed (Parquet)** | — | **~70-130 GB** | After grid-cell aggregation |

**Key insight:** The total processed dataset that Causal Atlas actually queries against will likely be 70-130 GB of Parquet files. This is comfortably within the range of a single-machine DuckDB deployment. The raw data archive will be 500 GB to 1 TB, requiring adequate storage but nothing exotic.

### 1.2 Data Ingestion

Data ingestion involves downloading, parsing, transforming, and writing datasets to the PRIO-GRID compatible format.

- **CPU characteristics:** Mostly single-threaded or lightly parallel; bottlenecked by I/O and network bandwidth, not CPU
- **Memory:** Moderate — peak 4-8 GB for raster resampling of large CHIRPS/NDVI files; tabular datasets like ACLED need only 1-2 GB
- **I/O:** Sequential write-heavy during Parquet file generation; random read during spatial joins
- **Network:** The primary bottleneck for initial data acquisition. Downloading 500 GB of raw data on a 100 Mbps connection takes ~11 hours; on 1 Gbps, ~1.1 hours (theoretical, before API rate limits)

### 1.3 Spatial Operations

Resampling rasters to the PRIO-GRID (0.5 deg x 0.5 deg), point-to-grid aggregation, and spatial joins.

- **CPU:** Moderately CPU-intensive. Rasterio/GDAL operations are single-threaded per file but can be parallelised across files using Python multiprocessing or Dask
- **Memory:** High peak for global rasters. A single CHIRPS daily raster at 0.05 deg resolution is ~7200 x 3600 pixels x 4 bytes = ~100 MB. Monthly aggregation holding 30 daily rasters in memory: ~3 GB. Processing multiple variables simultaneously: 8-16 GB peak
- **Disk I/O:** Read-heavy; benefits strongly from NVMe SSD over HDD

### 1.4 Statistical Analysis (PCMCI)

This is the most computationally demanding component. PCMCI discovers causal relationships among time series variables at each grid cell.

**Problem dimensions:**
- Grid cells: 259,200 (PRIO-GRID global, 0.5 deg x 0.5 deg, land cells only ~64,800)
- Time steps: ~120-500 (monthly, 10-40 years)
- Variables per cell: 10-20 (conflict count, rainfall, NDVI, food price, nightlights, etc.)
- Max lag: 6-12 months

**Computational complexity per cell:**
- PCMCI has complexity O(N^2 * tau_max * C^max_conds_dim), where N = number of variables, tau_max = maximum lag, and C = number of candidate conditions
- For N=20, tau_max=12, typical runtime: 5-60 seconds per cell depending on sparsity and conditional independence test used
- ParCorr (linear): ~5-10 seconds per cell
- GPDC/CMIknn (nonlinear): ~30-120 seconds per cell

**Total runtime estimates (ParCorr, 16-core CPU):**

| Scale | Grid Cells | Est. Runtime (16 cores) | Est. Runtime (64 cores) |
|-------|-----------|------------------------|------------------------|
| City-level pilot | 100 | 1-5 minutes | <1 minute |
| Country (medium) | 1,000 | 10-50 minutes | 3-15 minutes |
| Continental | 10,000 | 2-8 hours | 30 min - 2 hours |
| Global (land only) | ~64,800 | 12-50 hours | 3-12 hours |
| Global (all cells) | 259,200 | 2-8 days | 12-48 hours |

**Memory per PCMCI run:** ~50-200 MB per parallel worker. With 16 workers: 1-3 GB total. Memory is not the bottleneck; CPU is.

### 1.5 DuckDB Analytical Queries

DuckDB is the planned analytical engine, querying Parquet files directly.

- **Memory:** DuckDB uses memory-mapped I/O and can process datasets larger than RAM. For a 100 GB Parquet dataset, 32 GB RAM is sufficient for most queries; 64 GB is comfortable for complex multi-table joins
- **CPU:** Benefits from high core counts for parallel query execution. DuckDB automatically parallelises across available cores
- **Disk:** NVMe SSD dramatically improves Parquet scan performance. DuckDB leverages column pruning and predicate pushdown, so only relevant columns/rows are read
- **Benchmark reference:** DuckDB v1.4 LTS achieved number one on the ClickBench benchmark for open-source systems. Queries on Parquet run 1.1-5x slower than on native DuckDB format, but remain fast enough for interactive analysis

### 1.6 Web Serving (FastAPI + React)

- **CPU:** Light. A single FastAPI process handles hundreds of requests per second for API queries
- **Memory:** 1-4 GB for the application server; additional memory for DuckDB query execution
- **Concurrent users:** 10-50 users can be served comfortably from a single machine with uvicorn + multiple workers
- **Static frontend:** React bundle served by nginx; negligible resource requirements

### 1.7 ML/AI Workload

If running local LLM inference (e.g., for Claude-style interpretation) or training causal ML models:

- **Local LLM inference:** Not recommended for self-hosting initially. Use the Claude API instead. Running a local 7B parameter model requires 8+ GB VRAM; a 70B model requires 48+ GB VRAM
- **PyTorch Geometric Temporal (GNN):** Moderate GPU requirements. A mid-range GPU (8-16 GB VRAM) is sufficient for training spatiotemporal GNNs on regional subsets. Full global training may require 24+ GB VRAM or distributed training
- **Traditional ML (scikit-learn, statsmodels):** CPU-only, moderate memory. No GPU needed

---

## 2. Development Machine Specifications

### 2.1 Minimum Viable (Prototyping and Regional Analysis)

Sufficient for working with individual datasets, prototyping ingestion pipelines, running PCMCI on country-level subsets (<1,000 cells), and developing the web application.

| Component | Specification | Est. Price (Mar 2025) |
|-----------|--------------|----------------------|
| CPU | AMD Ryzen 5 7600X (6C/12T, 4.7-5.3 GHz) | $150-220 |
| Motherboard | MSI PRO B650-P WiFi (AM5, DDR5) | $150-180 |
| RAM | 32 GB DDR5-5600 (2x16 GB) | $150-200 |
| Boot/OS SSD | 500 GB NVMe Gen4 (Samsung 980 Pro or equiv.) | $50-60 |
| Data SSD | 2 TB NVMe Gen4 (Samsung 990 Pro or WD Black SN850X) | $150-200 |
| GPU | Integrated (Radeon, via APU) or no discrete GPU | $0 |
| PSU | 550W 80+ Bronze | $50-70 |
| Case | Mid-tower ATX (any well-ventilated) | $60-80 |
| **Total** | | **~$760-1,010** |

**Notes:**
- 32 GB RAM is tight for large raster operations but workable for regional analysis
- No discrete GPU needed at this tier — PCMCI and DuckDB are CPU-bound
- 2 TB data SSD holds raw + processed data for most datasets (excluding full GDELT)

### 2.2 Recommended (Continental-Scale Analysis)

Handles full data ingestion pipelines, continental-scale PCMCI runs, comfortable DuckDB querying of the full processed dataset, and web application development with local testing.

| Component | Specification | Est. Price (Mar 2025) |
|-----------|--------------|----------------------|
| CPU | AMD Ryzen 9 9900X (12C/24T, 4.4-5.6 GHz) | $360-400 |
| Motherboard | ASUS TUF Gaming B650E-PLUS WiFi or MSI MAG X670E Tomahawk WiFi | $200-280 |
| RAM | 64 GB DDR5-5600 (2x32 GB) | $500-700 |
| Boot/OS SSD | 1 TB NVMe Gen4 | $80-100 |
| Data SSD | 4 TB NVMe Gen4 (Samsung 990 Pro 4TB or Crucial T500 4TB) | $280-350 |
| Archive HDD | 8 TB 7200 RPM (Seagate IronWolf or WD Red Plus) | $150-180 |
| GPU | Optional: NVIDIA RTX 4060 Ti (8 GB VRAM) for RAPIDS/GNN experiments | $350-400 |
| PSU | 750W 80+ Gold | $90-120 |
| Case | Mid-tower with good airflow (Fractal Design Meshify 2 or equiv.) | $100-130 |
| **Total (without GPU)** | | **~$1,760-2,160** |
| **Total (with GPU)** | | **~$2,110-2,560** |

**Notes:**
- 64 GB RAM comfortably handles DuckDB queries on the full processed dataset, raster operations, and multiple analysis scripts running in parallel
- 12 cores cut PCMCI continental runtime to a few hours
- 4 TB NVMe holds all raw data (minus full GDELT) plus processed Parquet files with room to spare
- 8 TB HDD provides cold archive for raw downloads and backups

### 2.3 Ideal (Global-Scale PCMCI, Team Server)

For running full global PCMCI analysis across all land grid cells, serving as a small team development server, and handling multiple concurrent analysis pipelines.

| Component | Specification | Est. Price (Mar 2025) |
|-----------|--------------|----------------------|
| CPU | AMD Ryzen 9 9950X (16C/32T, 4.3-5.7 GHz) | $500-600 |
| Motherboard | ASUS ProArt X670E-Creator WiFi or Gigabyte X670E Aorus Master | $350-450 |
| RAM | 128 GB DDR5-5600 (2x64 GB) | $1,000-1,400 |
| Boot/OS SSD | 1 TB NVMe Gen4 | $80-100 |
| Data SSD (primary) | 4 TB NVMe Gen4 (Samsung 990 Pro 4TB) | $280-350 |
| Data SSD (secondary) | 2 TB NVMe Gen4 (scratch/temp space) | $150-200 |
| Archive HDD | 2x 8 TB 7200 RPM in RAID 1 mirror | $300-360 |
| GPU | NVIDIA RTX 4070 Ti Super (16 GB VRAM) | $700-800 |
| PSU | 850W 80+ Gold (Corsair RM850x or equiv.) | $120-150 |
| Case | Full tower or workstation case | $150-200 |
| CPU Cooler | Noctua NH-D15 or 280mm AIO | $80-120 |
| **Total** | | **~$3,710-4,730** |

**Notes:**
- 128 GB RAM enables comfortable parallel PCMCI with many workers, DuckDB joins across multiple large tables, and potential for running a small PostGIS instance alongside
- 16 cores at high clocks drive global PCMCI to completion in 12-48 hours
- 16 GB VRAM GPU enables RAPIDS cuDF (up to 150x pandas acceleration), cuSpatial for GPU-accelerated spatial operations, and PyTorch Geometric Temporal experiments

---

## 3. Server / Production Deployment

### 3.1 Small Deployment (Research Group, <10 Concurrent Users)

A single well-specified machine running all components.

**Recommended specification:**

| Component | Specification |
|-----------|--------------|
| CPU | AMD Ryzen 9 9950X or Intel Core i9-14900K |
| RAM | 128 GB DDR5 ECC (if supported by motherboard) |
| Boot SSD | 1 TB NVMe Gen4 |
| Data SSD | 4 TB NVMe Gen4 |
| Archive HDD | 2x 12 TB RAID 1 |
| GPU | Optional (NVIDIA RTX 4070 Ti Super if GPU analysis needed) |
| Network | 1 Gbps Ethernet minimum; 2.5 Gbps preferred |
| UPS | 1000 VA / 600 W |

**Operating system:** Ubuntu Server 24.04 LTS

**Architecture:**
- nginx (reverse proxy + static frontend) -> uvicorn/FastAPI (API) -> DuckDB (analytics engine)
- All services managed by systemd
- SSL via Let's Encrypt / certbot
- Firewall via ufw

**Linux distro recommendation — Ubuntu Server 24.04 LTS:**
- Longest support window (12 years with Ubuntu Pro)
- Best ecosystem for scientific Python packages
- GDAL 3.8.4 available in universe repository
- NVIDIA driver support is straightforward via `ubuntu-drivers`
- Largest community for troubleshooting
- Alternatives: Debian 12 (more conservative, slightly older packages), Fedora Server (newer packages but shorter support cycle)

### 3.2 Medium Deployment (Organisation, 10-100 Users)

Multi-machine or multi-service architecture.

**Option A: Docker Compose on a single powerful machine**

```
                    +---------+
                    |  nginx  |  (reverse proxy, TLS)
                    +----+----+
                         |
              +----------+----------+
              |                     |
         +----+----+          +-----+-----+
         | FastAPI |          | React SPA |
         | (x4     |          | (static)  |
         | workers)|          +-----------+
         +----+----+
              |
         +----+----+
         | DuckDB  |  (embedded, per-worker)
         +---------+
              |
         +----+----+
         | Parquet |  (NVMe SSD)
         | files   |
         +---------+
```

This works well for up to 50-100 concurrent users if the machine is well-specified (16+ cores, 128+ GB RAM, NVMe storage).

**Option B: Two-machine split**

| Machine | Role | Spec |
|---------|------|------|
| App server | nginx, FastAPI, React | 8 cores, 32 GB RAM, 500 GB SSD |
| Data/analysis server | DuckDB, PCMCI jobs, data pipelines | 16+ cores, 128+ GB RAM, 4 TB NVMe + HDD |

**Orchestration recommendations:**
- **Docker Compose:** Best for single-machine or two-machine setups. Simple, well-understood, minimal overhead. Recommended for Causal Atlas at this scale
- **k3s:** Lightweight Kubernetes. Consider if you need auto-scaling or multi-node orchestration. Adds operational complexity but handles node failure
- **Full Kubernetes (k8s):** Overkill for <100 users. Only justified if deploying to a cloud provider that manages the control plane (EKS, GKE)

### 3.3 Cloud Deployment Alternative

#### AWS

| Component | AWS Service | Instance/Config | Monthly Cost (est.) |
|-----------|------------|----------------|-------------------|
| App server | EC2 | c6i.2xlarge (8 vCPU, 16 GB) | $250 |
| Data/analysis | EC2 | r6i.2xlarge (8 vCPU, 64 GB) | $370 |
| Data storage | S3 | 1 TB Standard | $23 |
| Parquet (hot) | EBS | 500 GB gp3 SSD | $40 |
| Load balancer | ALB | — | $20 |
| **Small tier total** | | | **~$700/mo** |

| Component | AWS Service | Instance/Config | Monthly Cost (est.) |
|-----------|------------|----------------|-------------------|
| App servers (x2) | EC2 | c6i.2xlarge | $500 |
| Analysis server | EC2 | r6i.4xlarge (16 vCPU, 128 GB) | $740 |
| Data storage | S3 | 2 TB Standard | $46 |
| Parquet (hot) | EBS | 1 TB gp3 SSD | $80 |
| Load balancer | ALB | — | $20 |
| **Medium tier total** | | | **~$1,400/mo** |

**Spot/preemptible instances for batch analysis:**
- PCMCI batch jobs are ideal for spot instances (tolerant of interruption, can checkpoint)
- Spot pricing for r6i.4xlarge: ~$220-370/mo (50-70% discount)
- Strategy: run the web app on on-demand instances, burst PCMCI analysis to spot instances

#### GCP

| Component | GCP Service | Instance/Config | Monthly Cost (est.) |
|-----------|------------|----------------|-------------------|
| App server | Compute Engine | n2-standard-8 (8 vCPU, 32 GB) | $280 |
| Analysis server | Compute Engine | n2-highmem-16 (16 vCPU, 128 GB) | $740 |
| Data storage | Cloud Storage | 1 TB Standard | $20 |
| **Small tier total** | | | **~$650/mo** |

GCP offers sustained use discounts (automatic 20-30% discount for consistent usage) which can bring costs down.

#### Hetzner (Best Value for European Deployment)

Hetzner offers dramatically better pricing than hyperscalers, especially for dedicated servers.

| Plan | Spec | Monthly Cost |
|------|------|-------------|
| AX102 | Ryzen 9 7950X3D, 128 GB DDR5 ECC, 2x NVMe | ~$130/mo + $320 setup |
| AX162-S | EPYC 9454P (48C/96T), 128 GB DDR5 ECC, 2x NVMe | ~$200/mo + $80 setup |
| CCX33 (Cloud) | 8 dedicated vCPU, 32 GB RAM, 240 GB SSD | ~$45/mo |
| CCX53 (Cloud) | 32 dedicated vCPU, 128 GB RAM, 600 GB SSD | ~$175/mo |

**Hetzner recommendation for Causal Atlas:**
- **Development/small production:** AX102 ($130/mo) — a Ryzen 9 7950X3D with 128 GB ECC RAM is extraordinarily good value. This single machine can serve the web app and run continental-scale PCMCI analysis
- **Full production:** AX162-S ($200/mo) — 48-core EPYC can run global PCMCI in hours rather than days
- **Storage:** Hetzner Storage Box for backups: 1 TB for ~$4/mo, 5 TB for ~$12/mo

---

## 4. Storage Architecture

### 4.1 Storage Tier Strategy

| Tier | Technology | Use Case | Size Recommendation |
|------|-----------|----------|-------------------|
| Hot (active queries) | NVMe Gen4 SSD | Parquet files queried by DuckDB, active analysis scratch space | 2-4 TB |
| Warm (raw data) | SATA SSD or NVMe | Raw downloaded datasets, intermediate processing files | 2-4 TB |
| Cold (archive) | HDD 7200 RPM | Historical raw data, old analysis results, backups | 8-16 TB |
| Offsite backup | Cloud object storage | Disaster recovery, GDELT subset archive | 1-2 TB |

### 4.2 Storage Breakdown by Component

| Component | Estimated Size | Tier |
|-----------|---------------|------|
| Raw data archive (all datasets) | 500 GB - 1 TB | Warm/Cold |
| Processed Parquet files | 70-130 GB | Hot |
| DuckDB databases (materialised views) | 20-50 GB | Hot |
| Temporary/scratch (raster processing) | 50-200 GB (peak) | Hot |
| Application code + models | 5-10 GB | Hot |
| PostGIS database (if used) | 10-30 GB | Hot |
| Log files | 1-10 GB (rotating) | Warm |
| **Total hot tier** | **~200-450 GB** | NVMe |
| **Total warm tier** | **~500 GB - 1 TB** | SSD/NVMe |
| **Total cold tier** | **~1-2 TB** | HDD |

### 4.3 NVMe vs SATA SSD vs HDD Performance

| Metric | NVMe Gen4 | SATA SSD | HDD 7200 RPM |
|--------|----------|----------|--------------|
| Sequential read | 5,000-7,450 MB/s | 500-560 MB/s | 150-200 MB/s |
| Sequential write | 4,000-6,900 MB/s | 450-530 MB/s | 130-180 MB/s |
| Random 4K read (IOPS) | 800K-1,000K | 80K-100K | 100-200 |
| Random 4K write (IOPS) | 800K-1,000K | 60K-80K | 100-200 |
| Price per TB (Mar 2025) | $80-175 | $50-80 | $15-25 |

**Impact on Causal Atlas workloads:**
- **DuckDB Parquet scans:** NVMe provides 10-30x faster column scans compared to HDD. This is the single largest performance impact for interactive queries
- **Raster processing:** 3-5x faster on NVMe vs HDD for CHIRPS/NDVI aggregation due to random read patterns
- **Data ingestion writes:** Moderate benefit from NVMe; sequential writes are not dramatically different from SATA SSD

### 4.4 RAID Configurations

| RAID Level | Use Case | Recommendation |
|------------|----------|---------------|
| RAID 0 (stripe) | Temporary/scratch only | Never for important data. 2x read/write speed but total data loss on single drive failure |
| RAID 1 (mirror) | Archive HDD | Recommended for cold storage. Simple, reliable, 50% capacity loss |
| RAID 5/6 | Large HDD arrays (4+ drives) | Good for production servers with 4+ HDDs. RAID 6 recommended for drives >4 TB |
| No RAID | NVMe data drives | Acceptable if backups are maintained. NVMe RAID controllers are expensive and often unnecessary |

### 4.5 Filesystem Recommendations

| Filesystem | Strengths | Weaknesses | Recommendation |
|------------|----------|-----------|---------------|
| **XFS** | Best throughput for large files, parallel I/O, scales well | Cannot shrink partitions | **Primary choice for data volumes.** Best for Parquet files and raster data. Red Hat default |
| **ext4** | Reliable, well-tested, low overhead | Slightly slower for very large files and parallel workloads | **Good default for OS partition.** Excellent for general-purpose use |
| **ZFS** | Data integrity (checksums), snapshots, compression, deduplication | High RAM overhead (~1 GB per TB minimum, more with dedup). Not in mainline Linux kernel. Requires dedicated RAM | **Consider for archive volumes** if data integrity is paramount. Not recommended for hot data unless you have 128+ GB RAM |
| **Btrfs** | Snapshots, compression, in mainline kernel | Slower for database workloads per Phoronix benchmarks. RAID 5/6 still not production-ready | Acceptable alternative to ZFS with less RAM overhead |

**Recommended layout:**
```
/           ext4    (OS + apps, 500 GB - 1 TB NVMe)
/data       XFS     (Parquet files + DuckDB + raw data, 2-4 TB NVMe)
/archive    XFS     (HDD cold storage, RAID 1 mirror)
```

### 4.6 Backup Strategy

1. **Daily:** rsync processed Parquet files to archive HDD or remote storage
2. **Weekly:** Full backup of `/data` to offsite storage (Hetzner Storage Box, Backblaze B2, or S3 Glacier)
3. **On change:** Git + Git LFS for code and small data files; DVC (Data Version Control) for large datasets
4. **Raw data:** Considered reproducible (can be re-downloaded), so lower backup priority. Keep checksums to verify integrity

---

## 5. Software Stack Requirements

### 5.1 Operating System

**Ubuntu Server 24.04 LTS** is the recommended distribution.

**Why Ubuntu 24.04 LTS:**
- 12 years of support with Ubuntu Pro (free for up to 5 machines for personal/small use)
- GDAL 3.8.4, GEOS, PROJ all available in the `universe` repository
- NVIDIA driver installation is well-supported via `ubuntu-drivers`
- Largest ecosystem of scientific computing documentation and tutorials
- Python 3.12 available by default; 3.11 and 3.13 available via deadsnakes PPA
- Docker and docker-compose available in official repos

### 5.2 System Packages

Install on a fresh Ubuntu 24.04 system:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Essential build tools
sudo apt install -y build-essential cmake pkg-config git git-lfs curl wget unzip

# Geospatial libraries (C/C++ dependencies for Python packages)
sudo apt install -y \
    libgdal-dev \
    gdal-bin \
    python3-gdal \
    libgeos-dev \
    libproj-dev \
    proj-data \
    proj-bin \
    libspatialindex-dev

# HDF5 and NetCDF4 (for CHIRPS, climate data)
sudo apt install -y \
    libhdf5-dev \
    libnetcdf-dev \
    netcdf-bin

# Database libraries
sudo apt install -y \
    libpq-dev \
    postgresql-client

# Image and compression libraries
sudo apt install -y \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    zlib1g-dev \
    liblz4-dev \
    libzstd-dev

# Python development
sudo apt install -y \
    python3-dev \
    python3-pip \
    python3-venv

# Node.js (for React frontend)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Docker
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER

# Monitoring and utilities
sudo apt install -y htop glances iotop ncdu tmux
```

### 5.3 Python Environment

**Recommended Python version:** 3.11 or 3.12

**Why 3.11+:**
- 10-60% faster than 3.10 for many workloads (CPython speedup project)
- Required by newer versions of tigramite, PyTorch, and RAPIDS
- Full typing support for better code quality

**Virtual environment management (pick one):**

```bash
# Option A: uv (fastest, recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.12 .venv
source .venv/bin/activate

# Option B: conda/mamba (best for complex C dependencies)
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh
conda create -n causal-atlas python=3.12
conda activate causal-atlas

# Option C: standard venv
python3.12 -m venv .venv
source .venv/bin/activate
```

### 5.4 Python Package Groups

```bash
# Scientific computing core
pip install numpy pandas scipy scikit-learn statsmodels

# Geospatial
pip install geopandas rasterio xarray shapely fiona pyproj
pip install rasterstats exactextract PySAL

# Causal analysis
pip install tigramite causal-learn dowhy pgmpy

# Data engineering
pip install duckdb pyarrow polars h5py netCDF4
pip install fsspec s3fs  # for cloud storage access

# Visualization
pip install matplotlib plotly folium keplergl

# Web framework
pip install fastapi uvicorn[standard] pydantic

# ML/DL (optional, if GPU work planned)
pip install torch torchvision
pip install torch-geometric torch-geometric-temporal

# Development tools
pip install pytest black ruff mypy ipython jupyter

# Data version control
pip install dvc dvc-s3  # or dvc-gdrive, dvc-ssh
```

**Conda alternative for tricky C dependencies:**

```bash
# If pip installation of GDAL/rasterio/fiona fails:
conda install -c conda-forge gdal rasterio fiona geopandas xarray netcdf4
```

### 5.5 Database Stack

| Database | Role | Installation |
|----------|------|-------------|
| **DuckDB** | Primary analytical engine (embedded, no server needed) | `pip install duckdb` |
| **PostGIS** (optional) | Spatial database for complex spatial queries, user management | `sudo apt install postgresql-16-postgis-3` |

DuckDB is embedded (in-process) and requires no separate server installation. PostGIS is only needed if you require persistent spatial indexing, multi-user ACID transactions, or complex spatial SQL beyond what DuckDB + Parquet provides.

### 5.6 Containerisation

```bash
# Verify Docker installation
docker --version
docker compose version

# For GPU support in containers:
# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
    sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### 5.7 Version Control for Data

```bash
# Git LFS for medium files (10 MB - 1 GB)
git lfs install
git lfs track "*.parquet"
git lfs track "*.tif"
git lfs track "*.nc"

# DVC for large datasets (>1 GB)
dvc init
dvc remote add -d storage s3://causal-atlas-data  # or local path, GDrive, SSH
dvc add data/raw/chirps/
dvc push
```

---

## 6. Performance Benchmarks and Estimates

### 6.1 DuckDB Query Performance on Parquet

Benchmarks based on published DuckDB results and community reports for analytical workloads on Parquet files.

| Query Type | Dataset Size | Cores | RAM | Time (NVMe) | Time (HDD) |
|------------|-------------|-------|-----|------------|------------|
| Simple aggregation (SUM/COUNT by grid cell) | 10 GB Parquet | 8 | 32 GB | 1-3 sec | 5-15 sec |
| Time series extraction (single cell, all vars) | 10 GB Parquet | 8 | 32 GB | <0.5 sec | 1-3 sec |
| Spatial join (point events to grid) | 1 GB events + 10 GB grid | 8 | 32 GB | 5-15 sec | 30-90 sec |
| Complex multi-table join + aggregation | 50 GB total | 16 | 64 GB | 10-30 sec | 60-180 sec |
| Full table scan with filter | 100 GB Parquet | 16 | 64 GB | 15-60 sec | 120-300 sec |

**Key optimizations:**
- Partition Parquet files by year or region for faster predicate pushdown
- Use row groups of 100K-1M rows (DuckDB parallelises over row groups)
- Sort Parquet files by the most commonly filtered column (e.g., grid cell ID)
- DuckDB's larger-than-memory processing allows querying datasets that exceed RAM (with ~2-5x slowdown versus in-memory)

### 6.2 PCMCI Runtime Estimates

Using Tigramite's PCMCI with ParCorr (linear conditional independence test), N=20 variables, tau_max=12, T=120 time steps.

| CPU | Cores | 100 cells | 1,000 cells | 10,000 cells | 64,800 cells (global land) |
|-----|-------|----------|------------|-------------|--------------------------|
| Ryzen 5 7600X | 6C/12T | 2-5 min | 15-40 min | 3-7 hours | 18-45 hours |
| Ryzen 9 9900X | 12C/24T | 1-3 min | 8-20 min | 1.5-3.5 hours | 10-23 hours |
| Ryzen 9 9950X | 16C/32T | <1 min | 5-15 min | 1-2.5 hours | 6-16 hours |
| EPYC 9454P (Hetzner AX162) | 48C/96T | <30 sec | 2-5 min | 20-50 min | 2-5 hours |
| Threadripper 7970X | 32C/64T | <30 sec | 3-8 min | 30-80 min | 3-9 hours |

**With GPDC (non-linear, Gaussian process):** Multiply above times by 5-15x.

**With CMIknn (non-linear, k-nearest-neighbors):** Multiply above times by 3-10x.

**Memory usage:** ~100-200 MB per parallel worker. Even with 32 workers, total memory is <6.4 GB. PCMCI is CPU-bound, not memory-bound.

**Parallelisation strategy:** Each grid cell is independent, making this an "embarrassingly parallel" problem. Use Python's `multiprocessing.Pool` or `concurrent.futures.ProcessPoolExecutor` to distribute cells across CPU cores. Checkpointing every 1,000 cells allows restart on interruption.

### 6.3 Raster Processing Estimates

| Operation | Dataset | Hardware | Est. Time |
|-----------|---------|----------|-----------|
| Aggregate CHIRPS daily to monthly (one month) | ~30 files x 100 MB | 8 cores, 16 GB, NVMe | 30-60 sec |
| Aggregate CHIRPS daily to monthly (full archive, 40 years) | ~14,600 files | 8 cores, 16 GB, NVMe | 6-12 hours |
| Resample NDVI 1km to PRIO-GRID 0.5 deg (one file) | ~100 MB raster | 1 core, 4 GB | 10-30 sec |
| Point-to-grid aggregation (ACLED events to PRIO-GRID) | ~500 MB CSV | 4 cores, 8 GB | 2-5 min |
| Full data pipeline (all datasets to Parquet) | ~500 GB raw | 16 cores, 64 GB, NVMe | 12-48 hours |

### 6.4 Memory Profiling (Peak Usage)

| Operation | Peak RAM |
|-----------|---------|
| Loading one global CHIRPS daily raster (0.05 deg) | ~100 MB |
| Holding 30 daily rasters for monthly aggregation | ~3 GB |
| DuckDB query on 50 GB Parquet (complex join) | 8-16 GB |
| DuckDB full table materialisation (100 GB) | 20-40 GB |
| PCMCI (single worker, 20 vars, 120 timesteps) | 100-200 MB |
| PCMCI (16 parallel workers) | 1.5-3 GB |
| Geopandas spatial join (1M points to 260K polygons) | 4-8 GB |
| React dev server + FastAPI + DuckDB | 2-4 GB |

### 6.5 Network Bandwidth Estimates

| Dataset | Size | 100 Mbps | 1 Gbps |
|---------|------|---------|--------|
| CHIRPS full archive | ~100 GB | 2.5 hours | 15 min |
| ACLED full export | ~1 GB | 1.5 min | 10 sec |
| MODIS NDVI archive (1km monthly) | ~100 GB | 2.5 hours | 15 min |
| VIIRS Nightlights archive | ~80 GB | 2 hours | 12 min |
| Full raw data (all sources) | ~500 GB | 12 hours | 1.2 hours |

**Note:** These are theoretical maximums. Actual download times are typically 2-5x longer due to API rate limits, server throttling, and TCP overhead. CHIRPS is hosted on a public FTP server with moderate bandwidth. ACLED requires authentication and has rate limits. NASA Earthdata (MODIS/VIIRS) requires EarthData login and has per-user bandwidth limits.

---

## 7. GPU Considerations

### 7.1 When GPU Acceleration Helps

| Workload | GPU Benefit | Recommended? |
|----------|-----------|-------------|
| PCMCI (Tigramite) | None — CPU-only library | No |
| DuckDB queries | None — CPU-only engine | No |
| Raster resampling (GDAL) | None — CPU-only (mostly) | No |
| Pandas/Polars data wrangling | High with RAPIDS cuDF (up to 150x speedup) | Optional |
| Spatial operations | Moderate with cuSpatial (10-50x for spatial joins) | Optional |
| ML model training (scikit-learn equiv.) | High with cuML (10-100x) | Optional |
| GNN training (PyTorch Geometric Temporal) | Essential for practical runtimes | Yes, if doing GNN |
| Local LLM inference | Essential | Not recommended for this project |

### 7.2 RAPIDS (cuDF, cuSpatial, cuML)

RAPIDS is NVIDIA's GPU-accelerated data science toolkit. It provides drop-in replacements for pandas, scikit-learn, and spatial operations.

**Requirements:**
- NVIDIA GPU with Compute Capability 7.0+ (Volta or newer)
- Minimum 8 GB VRAM; 16 GB recommended for datasets >5 GB
- CUDA Toolkit 12.x
- Linux only (no Windows or macOS support for RAPIDS)

**Key benchmarks:**
- cuDF pandas accelerator mode: up to 150x speedup with zero code changes on a 5 GB dataset
- cuDF on 10 GB dataset with joins: up to 30x speedup on a 16 GB VRAM GPU vs CPU pandas
- cuML: GPU-accelerated random forest, KNN, PCA — typically 20-100x faster than scikit-learn

**Cost-benefit for Causal Atlas:** RAPIDS acceleration is a "nice to have" but not essential. The primary bottleneck (PCMCI) is CPU-only. Where RAPIDS shines is in the data preparation pipeline — spatial joins, large DataFrame manipulations, and ML feature engineering. If you are already buying a GPU for GNN experiments, you get RAPIDS essentially for free.

### 7.3 GPU Recommendations by Tier

| Tier | GPU | VRAM | CUDA Cores | Price (Mar 2025) | Use Case |
|------|-----|------|------------|-----------------|----------|
| Entry | RTX 4060 | 8 GB | 3,072 | $280-320 | Light cuDF, small GNN models |
| Mid-range | RTX 4060 Ti 16GB | 16 GB | 4,352 | $400-450 | cuDF on medium datasets, GNN training |
| Recommended | RTX 4070 Ti Super | 16 GB | 8,448 | $700-800 | cuDF, cuSpatial, GNN, good all-round |
| High-end | RTX 4080 Super | 16 GB | 10,240 | $900-1,000 | Fast cuDF/cuML, larger GNN models |
| Professional | RTX A5000 | 24 GB | 8,192 | $2,500-3,500 | Large datasets in GPU memory, professional features |

### 7.4 NVIDIA Driver and CUDA Installation on Ubuntu 24.04

```bash
# Method 1: ubuntu-drivers (easiest)
sudo apt install -y ubuntu-drivers-common
sudo ubuntu-drivers install

# Method 2: Specific driver version
sudo apt install -y nvidia-driver-550

# Verify installation
nvidia-smi

# Install CUDA Toolkit
sudo apt install -y nvidia-cuda-toolkit

# Or install via NVIDIA's repo for latest version:
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install -y cuda-toolkit-12-6

# Verify CUDA
nvcc --version

# Install RAPIDS
pip install cudf-cu12 cuml-cu12 cuspatial-cu12 --extra-index-url=https://pypi.nvidia.com
```

### 7.5 Is a GPU Worth It for Causal Atlas?

**For the core mission (causal discovery via PCMCI):** No. PCMCI is CPU-only and likely to remain so. Invest in more CPU cores instead.

**For the data pipeline:** Maybe. If you are processing very large datasets (>10 GB DataFrames) and want faster spatial joins and aggregations, RAPIDS cuDF/cuSpatial can provide 10-150x speedups. But you can also use DuckDB or Polars (CPU, very fast) for most of this work.

**For future GNN-based causal analysis:** Yes. If you plan to explore graph neural network approaches to spatiotemporal causal discovery (a promising research direction), a GPU is essential.

**Bottom line:** A mid-range GPU (RTX 4060 Ti 16GB, ~$400-450) is a reasonable investment if you want to keep the GNN option open. If you are on a tight budget, skip the GPU and allocate those funds to more RAM or a better CPU.

---

## 8. Networking and Data Transfer

### 8.1 Bandwidth Requirements

| Phase | Bandwidth Need | Duration |
|-------|---------------|----------|
| Initial data acquisition | High (sustained download of 500+ GB) | Days to weeks (due to rate limits) |
| Ongoing data updates | Low (weekly/monthly incremental pulls of MB-GB) | Minutes to hours |
| Web serving | Moderate (API responses + map tiles) | Continuous |
| Team collaboration (git, data sync) | Low-moderate | Continuous |

**Minimum:** 100 Mbps symmetric for a development machine. Adequate for data downloads and web serving.

**Recommended:** 1 Gbps symmetric for a production server. Enables fast initial data acquisition and comfortable multi-user web serving.

### 8.2 API Rate Limits and Download Strategies

| Data Source | Rate Limit | Strategy |
|-------------|-----------|----------|
| CHIRPS (CHC FTP) | No strict limit, moderate bandwidth | Parallel download with wget/aria2c, resume on failure |
| ACLED | 500 requests/day (free tier) | Bulk export via data export tool, not API |
| NASA Earthdata (MODIS/VIIRS) | Per-user throttle, ~10 concurrent downloads | Use earthaccess Python library with auth |
| GDELT | No limit on CSV downloads; BigQuery has quota | Direct CSV download for historical, BigQuery for analysis |
| OpenAQ | 100 requests/minute (API v3) | Bulk download via S3 open data registry instead |
| WFP | Moderate rate limits | Use HDX HAPI bulk download |
| USGS Earthquakes | 20,000 events per query | Paginate by time window |
| World Bank | 50 requests/second | Generous; use wbgapi Python library |

### 8.3 Data Synchronisation Tools

```bash
# rsync for file-based sync (local or over SSH)
rsync -avz --progress /data/parquet/ backup-server:/data/parquet/

# rclone for cloud storage sync
rclone sync /data/raw/ hetzner-storagebox:causal-atlas/raw/
rclone sync /data/raw/ s3:causal-atlas-backup/raw/

# aria2c for parallel HTTP/FTP downloads
aria2c -x 4 -s 4 -d /data/raw/chirps/ -i chirps_urls.txt
```

### 8.4 CDN and Caching for Web Frontend

- **Static assets (React bundle, map tiles):** Serve via nginx with aggressive caching headers (Cache-Control: max-age=31536000 for hashed assets)
- **API responses:** Cache common queries (grid cell metadata, available time ranges) in Redis or in-memory LRU cache. DuckDB queries are fast enough that caching is less critical
- **Map tiles:** If generating custom raster tiles, pre-generate at common zoom levels and serve as static files. Use Mapbox GL JS or Deck.gl with vector tiles for dynamic interaction
- **CDN:** For public deployment, Cloudflare Free tier provides adequate CDN and DDoS protection

---

## 9. Monitoring and Operations

### 9.1 Development Monitoring

For a development machine, lightweight tools suffice:

```bash
# Real-time system monitoring
htop           # CPU, memory, process overview
glances        # More comprehensive (CPU, mem, disk, network)
iotop          # Disk I/O by process
ncdu           # Disk space analysis (interactive)
duf            # Disk usage overview (modern df replacement)
```

### 9.2 Production Monitoring

For a deployed server:

| Component | Tool | Purpose |
|-----------|------|---------|
| System metrics | **Prometheus** + **node_exporter** | CPU, memory, disk, network metrics |
| Dashboards | **Grafana** | Visualization of metrics, alerting |
| Disk space | Custom Prometheus alert | Critical with large datasets — alert at 80% and 90% full |
| Application metrics | **FastAPI** + **prometheus_fastapi_instrumentator** | Request rate, latency, error rate |
| Logs | **journald** + **Loki** (or just journald for small deployments) | Centralized log aggregation |
| Uptime | **Uptime Kuma** (self-hosted) or external ping service | External availability monitoring |

**Grafana dashboard essentials for Causal Atlas:**
- Disk usage by mount point (track /data growth over time)
- RAM usage (watch for DuckDB memory pressure)
- CPU utilisation (identify when PCMCI jobs saturate cores)
- Network throughput (monitor data download progress)
- FastAPI request latency P50/P95/P99

### 9.3 Disk Space Monitoring

This is the single most critical operational concern. Large geospatial datasets can fill disks unexpectedly.

```bash
# Set up automated disk space alert (simple cron approach)
# Add to /etc/cron.d/disk-alert:
*/15 * * * * root df -h /data | awk 'NR==2 && int($5)>80 {print "DISK ALERT: /data at " $5}' | mail -s "Disk Alert" admin@example.com

# Or use Prometheus alert rule:
# alert: DiskSpaceLow
#   expr: (node_filesystem_avail_bytes{mountpoint="/data"} / node_filesystem_size_bytes{mountpoint="/data"}) < 0.1
#   for: 5m
```

### 9.4 Data Pipeline Monitoring

```bash
# Cron jobs for regular data updates
# /etc/cron.d/causal-atlas-updates

# Weekly ACLED update (Mondays at 2am)
0 2 * * 1 causal-atlas /opt/causal-atlas/scripts/update_acled.sh >> /var/log/causal-atlas/acled.log 2>&1

# Monthly CHIRPS update (1st of month at 3am)
0 3 1 * * causal-atlas /opt/causal-atlas/scripts/update_chirps.sh >> /var/log/causal-atlas/chirps.log 2>&1

# Daily earthquake data (4am)
0 4 * * * causal-atlas /opt/causal-atlas/scripts/update_earthquakes.sh >> /var/log/causal-atlas/earthquakes.log 2>&1
```

**Pipeline monitoring checklist:**
- Log file rotation (logrotate) to prevent log files from consuming disk
- Exit code checking in scripts with email/Slack notification on failure
- Data freshness tracking — alert if a dataset has not been updated in expected interval
- Checksum verification of downloaded files

### 9.5 Automated Backups

```bash
# Daily backup of processed data to remote storage
0 1 * * * causal-atlas rclone sync /data/parquet/ remote:causal-atlas/parquet/ --log-file=/var/log/causal-atlas/backup.log

# Weekly full backup
0 0 * * 0 causal-atlas /opt/causal-atlas/scripts/full_backup.sh
```

---

## 10. Specific Hardware Recommendations (March 2025 Pricing)

> **DDR5 RAM pricing caveat:** As of late 2025, DDR5 prices have surged dramatically due to AI-driven DRAM shortages. The prices below reflect this elevated market. A 64 GB DDR5 kit that cost ~$180 in May 2025 now costs $500-700+. If timing allows, consider waiting for prices to normalise, or look at DDR4 platforms (AM4) as a cost-effective alternative for budget builds.

### 10.1 Budget Build (~$1,000-1,500)

*"Good enough for prototyping, single-dataset analysis, and regional PCMCI (100-1,000 cells)"*

| Component | Product | Price (est.) |
|-----------|---------|-------------|
| CPU | AMD Ryzen 5 7600X (6C/12T, 4.7-5.3 GHz, Passmark ~28,500) | $150 |
| Motherboard | MSI PRO B650-P WiFi | $160 |
| RAM | G.Skill Ripjaws S5 32 GB (2x16 GB) DDR5-5600 | $150-200 |
| Boot + Data SSD | Samsung 990 Pro 2 TB NVMe Gen4 | $165 |
| PSU | Corsair CV550 550W 80+ Bronze | $55 |
| Case | Fractal Design Focus 2 ATX Mid Tower | $80 |
| CPU Cooler | Included or Thermalright Peerless Assassin 120 SE | $0-35 |
| **Total** | | **~$760-845** |

To reach the $1,000-1,500 range, upgrade RAM to 64 GB ($500-700 at current prices):
| **With 64 GB RAM** | | **~$1,110-1,345** |

**Can do:** Load and query individual datasets in DuckDB, run PCMCI on country-level subsets, develop FastAPI/React frontend, raster processing for individual countries.

**Cannot do:** Comfortable global-scale analysis, hold multiple large datasets in memory simultaneously, GPU-accelerated workflows.

### 10.2 Mid-Range Build (~$2,500-4,000)

*"Can run full analysis pipeline on continental scale, comfortable for daily development"*

| Component | Product | Price (est.) |
|-----------|---------|-------------|
| CPU | AMD Ryzen 9 9900X (12C/24T, 4.4-5.6 GHz, Passmark ~50,000+) | $380 |
| Motherboard | ASUS TUF Gaming B650E-PLUS WiFi | $220 |
| RAM | G.Skill Trident Z5 64 GB (2x32 GB) DDR5-5600 | $500-700 |
| Boot SSD | WD Black SN850X 1 TB NVMe Gen4 | $90 |
| Data SSD | Samsung 990 Pro 4 TB NVMe Gen4 | $320 |
| Archive HDD | Seagate IronWolf 8 TB 7200 RPM | $160 |
| GPU (optional) | NVIDIA RTX 4060 Ti 16 GB | $430 |
| PSU | Corsair RM750x 750W 80+ Gold | $100 |
| Case | Fractal Design Meshify 2 Compact | $120 |
| CPU Cooler | Noctua NH-D15 chromax.black | $110 |
| **Total (without GPU)** | | **~$2,000-2,200** |
| **Total (with GPU)** | | **~$2,430-2,630** |

Add 128 GB RAM instead of 64 GB for ~$500-700 more, reaching the $2,500-3,300 range.

**Can do:** Continental PCMCI in hours, full data pipeline for all datasets, DuckDB analytics on complete processed dataset, RAPIDS experiments (with GPU), team of 2-3 developers working simultaneously.

### 10.3 High-End Build (~$5,000-8,000)

*"Can run global-scale PCMCI, multiple analyses in parallel, serve as a small team server"*

| Component | Product | Price (est.) |
|-----------|---------|-------------|
| CPU | AMD Ryzen 9 9950X (16C/32T, 4.3-5.7 GHz, Passmark ~65,800) | $550 |
| Motherboard | ASUS ProArt X670E-Creator WiFi | $400 |
| RAM | 128 GB (2x64 GB) DDR5-5600 ECC (if supported) or non-ECC | $1,000-1,400 |
| Boot SSD | Samsung 990 Pro 1 TB | $100 |
| Data SSD (primary) | Samsung 990 Pro 4 TB | $320 |
| Data SSD (scratch) | Crucial T500 2 TB NVMe Gen4 | $160 |
| Archive HDDs | 2x Seagate IronWolf 12 TB (RAID 1) | $400 |
| GPU | NVIDIA RTX 4070 Ti Super 16 GB | $750 |
| PSU | Corsair RM1000x 1000W 80+ Gold | $170 |
| Case | Fractal Design Define 7 XL | $200 |
| CPU Cooler | Noctua NH-D15 chromax.black or Arctic Liquid Freezer II 360 | $110-130 |
| UPS | CyberPower CP1500PFCLCD 1500VA | $220 |
| 10 GbE NIC (optional) | Intel X540-T2 (used/refurb) | $50-80 |
| **Total** | | **~$4,430-4,880** |

To push toward the $5,000-8,000 range, consider upgrading to an RTX 4080 Super ($1,000) or adding a second 4 TB NVMe.

**Can do:** Global PCMCI (land cells) in 6-16 hours, serve 10-20 concurrent web users, full RAPIDS GPU pipeline, GNN experiments with PyTorch Geometric Temporal, run multiple analysis jobs in parallel.

### 10.4 Workstation Build (~$10,000+)

*"For serious production use, large team server, or continuous pipeline operation"*

| Component | Product | Price (est.) |
|-----------|---------|-------------|
| CPU | AMD Threadripper 7970X (32C/64T, 4.0-5.3 GHz) | $1,800 |
| Motherboard | ASUS Pro WS WRX90E-SAGE SE (sTR5) | $900-1,200 |
| RAM | 256 GB (4x64 GB) DDR5-4800 ECC RDIMM | $2,000-3,000 |
| Boot SSD | 1 TB NVMe Gen4 | $100 |
| Data SSDs | 2x Samsung 990 Pro 4 TB (RAID 0 for scratch, backed up) | $640 |
| Archive HDDs | 4x 16 TB Seagate Exos (RAID 6 or RAID 10) | $1,000-1,200 |
| GPU | NVIDIA RTX 4080 Super 16 GB | $950 |
| PSU | Corsair HX1500i 1500W 80+ Platinum | $350 |
| Case | Fractal Design Define 7 XL or rack-mount chassis | $200-500 |
| CPU Cooler | Noctua NH-U14S TR5-SP6 or custom loop | $80-300 |
| HBA/RAID controller | LSI 9300-8i (for HDD array) | $80-150 |
| UPS | APC SMT2200 2200VA | $600-800 |
| **Total** | | **~$8,700-12,050** |

**Threadripper 7970X advantages:**
- 32 cores / 64 threads — global PCMCI in 3-9 hours with ParCorr
- Quad-channel DDR5 with ECC support — essential for long-running analyses (bit flips in multi-day jobs are a real concern)
- 128 PCIe 5.0 lanes — can support multiple NVMe drives and GPU without bandwidth contention
- sTR5 platform supports up to 1 TB RAM

### 10.5 Laptop Recommendations for Mobile Development

| Laptop | Key Specs | Price (est.) | Notes |
|--------|----------|-------------|-------|
| **Lenovo ThinkPad T14s Gen 6 (AMD)** | Ryzen AI 7 PRO 360, 32 GB LPDDR5X, 14" 1920x1200 | $1,300-1,500 (on sale) | Best Linux compatibility, excellent keyboard, business-class reliability |
| **Lenovo ThinkPad P16s Gen 4** | Ryzen AI Pro 300, up to 96 GB DDR5, 16" | $1,600-2,200 | Larger screen, more RAM capacity, ISV certified |
| **Framework Laptop 16 (2025)** | Ryzen AI 9 HX 370, up to 64 GB DDR5, RTX 5070 option, 16" | $1,500-2,500 | Modular, repairable, good Linux support, GPU module available |
| **System76 Pangolin** | Ryzen 9 8945HS, up to 96 GB DDR5, 16" 2K 120Hz | $1,300-1,600 | Ships with Pop!_OS or Ubuntu, guaranteed Linux support |

**Recommendation:** The ThinkPad T14s Gen 6 (AMD) is the pragmatic choice for mobile development — lightweight, excellent keyboard, and outstanding Linux compatibility. For heavier analysis work on the go, the ThinkPad P16s Gen 4 with 64+ GB RAM provides more headroom.

### 10.6 Mini PC Options (Always-On Data Collection Nodes)

| Mini PC | Key Specs | Price (est.) | Use Case |
|---------|----------|-------------|----------|
| **Minisforum MS-A2** | Ryzen 9 9955HX (16C/32T), up to 96 GB DDR5, dual 10GbE | $800 (barebones) / $1,200-1,900 (configured) | Powerful enough for a small production server; dual 10GbE is excellent for data pipeline work |
| **Minisforum UM790 Pro** | Ryzen 9 7940HS, up to 64 GB DDR5, USB4 | $450-600 (configured) | Data collection node, lightweight analysis |
| **Beelink SER8** | Ryzen 7 8845HS, up to 64 GB DDR5, 2.5GbE | $400-500 | Budget always-on node for scheduled data downloads |

**Mini PC advantages:** Low power consumption (35-65W TDP vs 100-170W for desktop), silent or near-silent operation, small footprint for co-located deployment. The Minisforum MS-A2 with 96 GB RAM and a 2 TB NVMe could function as a capable Causal Atlas server for a small team.

### 10.7 Used/Refurbished Server Options

Used enterprise servers offer exceptional price-to-performance for compute-heavy workloads.

| Server | Typical Config (Used) | Price (eBay, est.) | Notes |
|--------|----------------------|-------------------|-------|
| **Dell PowerEdge R750** | 2x Xeon Gold 5317 (24C total), 128-256 GB DDR4 ECC, 8x NVMe bays | $1,500-3,000 | Current-gen (2021), excellent for PCMCI parallelism |
| **Dell PowerEdge R740** | 2x Xeon Gold 6248 (40C total), 256 GB DDR4 ECC | $800-1,500 | Previous gen, still very capable, great value |
| **HP ProLiant DL380 Gen10** | 2x Xeon Gold, 128-256 GB DDR4 ECC | $700-1,500 | Reliable, well-supported, widely available |

**Caveats with used servers:**
- **Noise:** Rack servers are loud (50-70 dB). Not suitable for home office without acoustic isolation
- **Power consumption:** Dual-socket Xeon systems draw 300-600W at load. Electricity cost adds up
- **DDR4 vs DDR5:** These servers use DDR4, which is actually an advantage right now given DDR5 price inflation. DDR4 ECC 256 GB kits can be found for $300-500
- **Warranty:** Some eBay sellers offer 5-year warranties on refurbished units. Verify before purchase
- **No GPU support:** Most R740/R750 configurations have one or two PCIe x16 slots, sufficient for a single GPU

**Best value option:** A Dell PowerEdge R740 with 2x Xeon Gold 6248 (20C/40T each = 40C/80T total), 256 GB DDR4 ECC, and 2x NVMe drives can be found for $800-1,200 on eBay. This provides Threadripper-class parallelism at a fraction of the cost. Global PCMCI on land cells would complete in 3-8 hours.

---

## 11. Comparison: Self-Hosted vs Cloud

### 11.1 Three-Year Total Cost of Ownership

**Scenario: Causal Atlas for a small research group (5-10 users, continuous operation)**

| Cost Category | Self-Hosted (High-End Build) | Hetzner AX102 | AWS (Small Tier) |
|--------------|----------------------------|--------------|-----------------|
| Hardware/setup | $5,000 (one-time) | $320 (setup fee) | $0 |
| Monthly hosting/compute | $0 | $130/mo | $700/mo |
| Electricity (~200W avg, $0.15/kWh) | $260/year | Included | Included |
| Internet (dedicated IP, adequate bandwidth) | $50-100/mo | Included | $50/mo (data transfer) |
| Backups (offsite storage) | $10/mo | $10/mo | $25/mo |
| Maintenance time (est. 2 hrs/mo @ $50/hr) | $100/mo | $50/mo | $50/mo |
| **Year 1** | **$7,920** | **$2,840** | **$9,900** |
| **Year 2** | **$2,920** | **$2,520** | **$9,900** |
| **Year 3** | **$2,920** | **$2,520** | **$9,900** |
| **3-Year Total** | **~$13,760** | **~$7,880** | **~$29,700** |

**Key observations:**
- **Hetzner dedicated server is the clear winner for cost efficiency** — 73% cheaper than AWS over 3 years, 43% cheaper than self-hosted, with no hardware procurement or maintenance burden
- Self-hosted amortises well: years 2 and 3 are dramatically cheaper than cloud. But you carry the hardware risk and maintenance burden
- AWS is by far the most expensive but offers the most flexibility (auto-scaling, managed services, global deployment)

### 11.2 When Cloud Makes Sense

- **Variable workloads:** You only need heavy compute for PCMCI runs a few times per month. Use spot instances for burst compute and pay only for what you use
- **Global deployment:** Users are distributed worldwide and need low-latency access
- **Team lacks sysadmin expertise:** Managed services (RDS, ECS, S3) reduce operational burden
- **Grant-funded projects:** Cloud costs are operational expenses (easier to budget) vs hardware capital expenditure
- **Quick start:** No procurement delays. Spin up a server in minutes

### 11.3 When Self-Hosted Makes Sense

- **Steady workloads:** The server runs 24/7 for data pipelines, web serving, and on-demand analysis. High utilisation favours self-hosted
- **Data volume:** Transferring 500+ GB to/from cloud storage has egress costs and latency. Local data processing is faster and cheaper
- **Long-term project:** Over 3+ years, hardware costs amortise dramatically
- **Control and privacy:** Full control over data location and access. Important for sensitive humanitarian data

### 11.4 Hybrid Approach (Recommended)

The optimal strategy for Causal Atlas:

1. **Develop locally** on a recommended-tier desktop ($2,000-3,000). Fast iteration, no recurring costs, full control
2. **Deploy to Hetzner dedicated server** (AX102, $130/mo) for production web serving and scheduled data pipelines. Best cost-performance ratio for sustained workloads
3. **Burst to cloud for heavy compute:** When running global-scale PCMCI or reprocessing the full dataset, spin up spot instances on AWS/GCP. A c6i.8xlarge spot instance (32 vCPU, 64 GB) costs ~$0.40/hr — running global PCMCI for 24 hours costs ~$10
4. **Use cloud object storage for distribution:** Store public Parquet datasets on S3/GCS for community access. CloudFront or equivalent for the web frontend CDN

**Estimated monthly cost (hybrid):**
- Hetzner AX102: $130
- AWS S3 (500 GB): $12
- Occasional spot compute (10 hours/month): $4-20
- Backups (Hetzner Storage Box, 5 TB): $12
- **Total: ~$160-175/month**

### 11.5 Data Sovereignty Considerations

Causal Atlas handles data relevant to humanitarian contexts (conflict data, food security, displacement). Important considerations:

- **ACLED and UCDP data:** No specific data residency requirements, but responsible handling is expected. Avoid exposing raw conflict micro-data via public APIs
- **GDPR:** If collecting any user data (even login emails) from EU users, GDPR applies. Hetzner (Germany/Finland data centres) is GDPR-compliant by default
- **Humanitarian principles:** Consider hosting in jurisdictions with strong data protection. Avoid hosting in countries that are themselves subjects of the conflict data
- **Open data licensing:** Most source datasets (CHIRPS, MODIS, USGS, OpenAQ) are public domain or open license. ACLED requires attribution and has commercial use restrictions. Verify license terms for each dataset before redistribution

---

## 12. Detailed Benchmarking Plan

> **Checked:** March 2025

Before committing to a hardware purchase, run these specific benchmarks to validate that the chosen configuration meets Causal Atlas requirements. These can be run on existing hardware, cloud trial instances, or in-store demo machines.

### 12.1 DuckDB: Parquet Scan Performance

**What to measure:** Sequential scan throughput (GB/s per core), predicate pushdown effectiveness, and larger-than-memory query behaviour.

```bash
# Generate a test Parquet dataset matching our expected schema
python3 -c "
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np

# Simulate 10M rows (approx 1 year of global data, 20 variables)
n = 10_000_000
table = pa.table({
    'gid': np.random.randint(1, 259201, n, dtype=np.int32),
    'year': np.random.randint(2015, 2025, n, dtype=np.int16),
    'month': np.random.randint(1, 13, n, dtype=np.int8),
    'variable': np.random.choice(['var_' + str(i) for i in range(20)], n),
    'value': np.random.randn(n).astype(np.float64),
    'source_id': np.random.choice(['acled_v24', 'chirps_v2', 'wfp_v1'], n),
    'quality_flag': np.random.randint(0, 4, n, dtype=np.int8),
    'quality_composite': np.random.uniform(0.3, 1.0, n).astype(np.float32),
})
pq.write_table(table, '/tmp/bench_10m.parquet',
               compression='snappy', row_group_size=100_000)
print(f'Wrote {n:,} rows, file size: {pq.read_metadata(\"/tmp/bench_10m.parquet\").serialized_size / 1e6:.1f} MB')
"

# Benchmark 1: Full scan with aggregation
duckdb -c "
.timer on
SELECT variable, AVG(value), COUNT(*), STDDEV(value)
FROM read_parquet('/tmp/bench_10m.parquet')
GROUP BY variable;
"

# Benchmark 2: Predicate pushdown (single cell time series)
duckdb -c "
.timer on
SELECT year, month, variable, value
FROM read_parquet('/tmp/bench_10m.parquet')
WHERE gid = 142567
ORDER BY variable, year, month;
"

# Benchmark 3: Range scan with filter
duckdb -c "
.timer on
SELECT gid, AVG(value) as mean_val
FROM read_parquet('/tmp/bench_10m.parquet')
WHERE variable = 'var_0' AND year BETWEEN 2020 AND 2023
GROUP BY gid
HAVING AVG(value) > 1.0;
"

# Benchmark 4: Multi-table join (simulate correlation query)
python3 -c "
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np

# Create a second table for joining
n = 5_000_000
table2 = pa.table({
    'gid': np.random.randint(1, 259201, n, dtype=np.int32),
    'year': np.random.randint(2015, 2025, n, dtype=np.int16),
    'month': np.random.randint(1, 13, n, dtype=np.int8),
    'variable': np.full(n, 'chirps_precip'),
    'value': np.random.uniform(0, 500, n).astype(np.float64),
})
pq.write_table(table2, '/tmp/bench_5m.parquet', compression='snappy')
"

duckdb -c "
.timer on
SELECT a.gid, CORR(a.value, b.value) as correlation
FROM read_parquet('/tmp/bench_10m.parquet') a
JOIN read_parquet('/tmp/bench_5m.parquet') b
    ON a.gid = b.gid AND a.year = b.year AND a.month = b.month
WHERE a.variable = 'var_0'
GROUP BY a.gid
HAVING COUNT(*) > 10;
"
```

**Target performance (mid-range build, 12C/64GB/NVMe):**

| Benchmark | Target Time | Acceptable |
|-----------|-------------|-----------|
| Full scan + aggregation (10M rows) | < 0.5s | < 2s |
| Predicate pushdown (single cell) | < 50ms | < 200ms |
| Range scan with filter | < 0.3s | < 1s |
| Multi-table join correlation | < 2s | < 10s |

### 12.2 Python: PCMCI Runtime per Cell

```bash
# Benchmark PCMCI with representative parameters
python3 -c "
import time
import numpy as np
from tigramite import data_processing as pp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

# Simulate: 20 variables, 120 time steps (10 years monthly)
N_VARS = 20
T = 120
np.random.seed(42)
data = np.random.randn(T, N_VARS)

# Add some real correlations to make it non-trivial
data[:, 1] = 0.5 * data[:, 0] + 0.5 * np.random.randn(T)  # var1 depends on var0
data[:, 5] = 0.3 * np.roll(data[:, 2], 3) + 0.7 * np.random.randn(T)  # var5 depends on var2 with lag 3

dataframe = pp.DataFrame(data, var_names=[f'var_{i}' for i in range(N_VARS)])
parcorr = ParCorr(significance='analytic')
pcmci = PCMCI(dataframe=dataframe, cond_ind_test=parcorr, verbosity=0)

# Single cell benchmark
start = time.perf_counter()
results = pcmci.run_pcmci(tau_max=12, pc_alpha=0.05)
elapsed = time.perf_counter() - start
print(f'Single cell PCMCI (ParCorr, {N_VARS} vars, T={T}, tau_max=12): {elapsed:.2f}s')

# Estimate global runtime
land_cells = 64800
cores = $(nproc)
estimated_hours = (elapsed * land_cells) / cores / 3600
print(f'Estimated global land runtime ({cores} cores): {estimated_hours:.1f} hours')
"
```

### 12.3 Raster Resampling

```bash
# Benchmark rasterio resampling (CHIRPS-like raster to PRIO-GRID)
python3 -c "
import time
import numpy as np
import rasterio
from rasterio.transform import from_bounds

# Create a synthetic raster matching CHIRPS resolution (0.05 deg, global)
width = 7200  # 360 / 0.05
height = 3600  # 180 / 0.05
data = np.random.uniform(0, 500, (1, height, width)).astype(np.float32)

transform = from_bounds(-180, -90, 180, 90, width, height)
profile = {
    'driver': 'GTiff', 'dtype': 'float32', 'width': width, 'height': height,
    'count': 1, 'crs': 'EPSG:4326', 'transform': transform,
}

with rasterio.open('/tmp/bench_raster.tif', 'w', **profile) as dst:
    dst.write(data)

# Benchmark resampling to 0.5 degree (PRIO-GRID)
from rasterio.warp import reproject, Resampling

start = time.perf_counter()
target_width = 720   # 360 / 0.5
target_height = 360  # 180 / 0.5
target_data = np.empty((1, target_height, target_width), dtype=np.float32)
target_transform = from_bounds(-180, -90, 180, 90, target_width, target_height)

with rasterio.open('/tmp/bench_raster.tif') as src:
    reproject(
        source=rasterio.band(src, 1),
        destination=target_data[0],
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=target_transform,
        dst_crs='EPSG:4326',
        resampling=Resampling.average,
    )
elapsed = time.perf_counter() - start
print(f'Raster resample (7200x3600 -> 720x360): {elapsed:.2f}s')
print(f'30 daily rasters (1 month CHIRPS): {elapsed * 30:.1f}s')
"
```

### 12.4 Disk I/O

```bash
# Sequential read/write test with fio
sudo apt install -y fio

# Sequential read (simulates Parquet scan)
fio --name=seq-read --rw=read --bs=1M --size=4G --numjobs=1 \
    --directory=/data --ioengine=libaio --direct=1 --runtime=30

# Sequential write (simulates Parquet generation)
fio --name=seq-write --rw=write --bs=1M --size=4G --numjobs=1 \
    --directory=/data --ioengine=libaio --direct=1 --runtime=30

# Random 4K read (simulates DuckDB predicate pushdown)
fio --name=rand-read --rw=randread --bs=4k --size=2G --numjobs=4 \
    --directory=/data --ioengine=libaio --direct=1 --iodepth=32 --runtime=30

# Print summary
echo "Target for NVMe Gen4:"
echo "  Sequential read:  > 3,000 MB/s (ideal > 5,000 MB/s)"
echo "  Sequential write: > 2,000 MB/s (ideal > 4,000 MB/s)"
echo "  Random 4K read:   > 500K IOPS (ideal > 800K IOPS)"
```

### 12.5 Network Download Speed

```bash
# Test download speeds for key data sources
echo "=== CHIRPS (UCSB FTP) ==="
time wget -q --spider ftp://ftp.chg.ucsb.edu/pub/org/chg/products/CHIRPS-2.0/global_daily/tifs/p05/2024/chirps-v2.0.2024.01.01.tif.gz 2>&1 | head -5

echo "=== ACLED API ==="
time curl -s -o /dev/null -w "Speed: %{speed_download} bytes/sec\nTime: %{time_total}s\n" \
    "https://api.acleddata.com/acled/read?limit=1&key=YOUR_KEY"

echo "=== NASA Earthdata (MODIS) ==="
# Requires .netrc with Earthdata credentials
time wget -q --spider "https://e4ftl01.cr.usgs.gov/MOLT/MOD13A3.061/2024.01.01/" 2>&1 | head -5

echo "=== General bandwidth test ==="
curl -s https://speed.cloudflare.com/__down?bytes=100000000 -o /dev/null -w "Download: %{speed_download} bytes/sec\n"
```

---

## 13. Power and Cooling

> **Checked:** March 2025

### 13.1 Power Consumption Estimates

| Build Tier | Idle Power | Load Power (CPU+disk) | Peak Power (CPU+GPU+disk) | Annual kWh (est.) |
|-----------|-----------|---------------------|-------------------------|------------------|
| Budget (Ryzen 5 7600X, no GPU) | 45-65W | 120-180W | 200W | 700-1,100 kWh |
| Mid-range (Ryzen 9 9900X, no GPU) | 55-80W | 180-250W | 300W | 1,000-1,600 kWh |
| Mid-range + GPU (RTX 4060 Ti) | 65-95W | 200-300W | 450W | 1,200-1,900 kWh |
| High-end (Ryzen 9 9950X + RTX 4070 Ti) | 75-110W | 250-350W | 550W | 1,500-2,200 kWh |
| Workstation (Threadripper 7970X + GPU) | 100-150W | 350-500W | 750W | 2,200-3,200 kWh |
| Mini PC (Minisforum MS-A2) | 15-25W | 65-95W | 120W | 400-600 kWh |
| Used server (Dell R740, dual Xeon) | 120-200W | 350-600W | 800W | 2,500-3,800 kWh |

**Estimation methodology:** Idle = system on, no computation. Load = sustained PCMCI or DuckDB workload. Peak = simultaneous CPU + GPU stress test. Annual kWh assumes 60% idle / 30% load / 10% peak duty cycle for an always-on development server.

### 13.2 Power Cost Estimates

| Electricity Rate | Budget Build | Mid-Range | High-End | Workstation | Used Server |
|-----------------|-------------|-----------|----------|-------------|-------------|
| $0.10/kWh (US average) | $70-110/yr | $100-160/yr | $150-220/yr | $220-320/yr | $250-380/yr |
| $0.15/kWh (US urban) | $105-165/yr | $150-240/yr | $225-330/yr | $330-480/yr | $375-570/yr |
| $0.30/kWh (EU/DE average) | $210-330/yr | $300-480/yr | $450-660/yr | $660-960/yr | $750-1,140/yr |
| $0.35/kWh (EU/NL high) | $245-385/yr | $350-560/yr | $525-770/yr | $770-1,120/yr | $875-1,330/yr |

**Key insight for Causal Atlas:** The mid-range build at US electricity rates costs approximately $10-20/month in power -- negligible compared to cloud hosting. However, at European electricity rates (relevant for Hetzner-hosted alternatives), power costs for a home server are 2-3x higher. This strengthens the case for Hetzner dedicated servers where electricity is included in the monthly fee.

### 13.3 UPS Recommendations

For always-on servers running data pipelines, a UPS is not optional -- it prevents data corruption during power outages, especially for DuckDB write operations and Parquet file generation.

| Build Tier | UPS Recommendation | Capacity | Runtime at Load | Est. Price |
|-----------|-------------------|----------|----------------|-----------|
| Budget / Mid-range (no GPU) | CyberPower CP1000PFCLCD | 1000VA / 600W | 8-15 min at 200W | $140-170 |
| Mid-range + GPU | APC Back-UPS Pro 1500S (BR1500MS2) | 1500VA / 900W | 8-12 min at 350W | $190-250 |
| High-end | CyberPower CP1500PFCLCD | 1500VA / 1000W PFC Sinewave | 10-15 min at 400W | $200-250 |
| Workstation | APC Smart-UPS SMT2200C | 2200VA / 1980W | 8-12 min at 600W | $600-800 |
| Used server | APC Smart-UPS SMT3000 | 3000VA / 2700W | 10-15 min at 600W | $800-1,200 |

**Critical UPS features for Causal Atlas:**
- **Pure sine wave output:** Required for systems with active PFC power supplies (all modern 80+ Gold/Platinum PSUs). Simulated sine wave UPS can cause instability and potential hardware damage
- **USB communication:** Connect to server via USB for automatic graceful shutdown when battery is low. Use `apcupsd` (for APC) or `nut` (Network UPS Tools, for CyberPower and others) on Ubuntu
- **Replace battery every 3-5 years:** Lead-acid batteries degrade. Set a calendar reminder

**Ubuntu UPS configuration (using NUT):**

```bash
# Install Network UPS Tools
sudo apt install -y nut nut-client nut-server

# Configure UPS driver (/etc/nut/ups.conf)
cat <<'EOF' | sudo tee /etc/nut/ups.conf
[causal-atlas-ups]
    driver = usbhid-ups
    port = auto
    desc = "CyberPower CP1500PFCLCD"
EOF

# Configure shutdown thresholds (/etc/nut/upsmon.conf)
# FINALDELAY: wait 5 seconds then shutdown
# LOWBATT: shutdown when battery is low

sudo systemctl enable nut-server nut-monitor
sudo systemctl start nut-server nut-monitor

# Test UPS detection
upsc causal-atlas-ups
```

### 13.4 Cooling Considerations

| Scenario | Ambient Temp Limit | Recommendation |
|----------|-------------------|----------------|
| Desktop in air-conditioned office | < 25C | Stock or tower cooler (Noctua NH-D15). No special considerations |
| Desktop in non-AC room (summer) | 25-35C | Good case airflow (mesh front panel), 2-3 case fans, tower cooler. Monitor CPU temps during sustained PCMCI |
| Closet or enclosed space | Variable | NOT recommended without ventilation. CPU and SSD throttle above 80-95C. Minimum: intake and exhaust vents |
| Rack-mounted server | Datacenter spec | Rack servers (R740, etc.) are designed for 35C ambient. Ensure 1U-2U spacing for airflow |
| Mini PC (always-on) | < 30C | Small form factor limits cooling. Monitor thermals during sustained load. Place on ventilated surface |

**Temperature monitoring on Ubuntu:**

```bash
# Install and use lm-sensors
sudo apt install -y lm-sensors
sudo sensors-detect --auto
sensors  # Show current temperatures

# Continuous monitoring
watch -n 5 sensors

# For NVMe SSD temperature
sudo apt install -y nvme-cli
sudo nvme smart-log /dev/nvme0

# Set up thermal alert (add to cron)
# Alert if CPU > 85C or NVMe > 70C
```

---

## 14. Data Sovereignty and Legal

> **Checked:** March 2025

### 14.1 Data Residency by Source

| Data Source | Licence | Residency Requirements | Storage Restrictions |
|------------|---------|----------------------|---------------------|
| **ACLED** | Free for non-commercial use; attribution required; commercial use requires licence | No explicit residency requirement. Terms of use restrict redistribution of raw micro-data. Aggregate statistics can be freely shared | Do not expose individual event coordinates via public API |
| **UCDP GED** | CC-BY-4.0 | No residency requirements | Free to redistribute with attribution |
| **CHIRPS** | Public domain (US Government funded) | None | None |
| **MODIS/VIIRS** | Public domain (NASA) | None | None |
| **USGS Earthquakes** | Public domain (US Government) | None | None |
| **OpenAQ** | CC-BY-4.0 | None | Free to redistribute with attribution |
| **WFP food prices** | CC-BY-SA-3.0 IGO | No explicit requirements. Handled via HDX | Share-alike required |
| **World Bank** | CC-BY-4.0 | None | Free to redistribute with attribution |
| **FAO** | Varies by dataset; generally open | None for statistical data | Check per-dataset licence |
| **GDELT** | Open, derived from news sources | None | Attribution appreciated but not legally required |
| **EM-DAT** | Registration required; academic/research use free | No explicit residency | Do not redistribute full database without permission |
| **UNHCR/IOM** | Varies; some datasets restricted | May require data sharing agreements. UNHCR data protection policy applies to personal data | Avoid co-locating with conflict actor data |
| **WHO disease data** | Generally open for aggregate statistics | No residency for aggregate data | Individual-level health data subject to national regulations |

### 14.2 GDPR Considerations

If Causal Atlas serves European users (likely, given Hetzner hosting), GDPR applies to any personal data collected -- even basic user account information.

**What constitutes personal data for Causal Atlas:**
- User email addresses (for API keys, notifications)
- IP addresses in server logs
- Any user-uploaded annotations linked to an identifiable person
- ORCID identifiers (linked to real names)

**What is NOT personal data:**
- Aggregated grid-level statistics (anonymised by design -- 0.5 degree resolution covers ~55 km)
- Conflict event counts, precipitation values, food prices at grid level
- Analysis results (correlations, causal graphs)

**GDPR compliance measures:**

| Requirement | Implementation |
|------------|---------------|
| **Lawful basis** | Legitimate interest (research platform) + consent (user accounts) |
| **Data minimisation** | Collect only email and ORCID for accounts; no demographic data |
| **Right to erasure** | Implement user account deletion API |
| **Data protection impact assessment** | Required if processing sensitive data at scale |
| **Data processing agreement** | Needed with Hetzner (they provide standard DPA) |
| **Privacy policy** | Publish on the website; disclose data collected and purposes |
| **Cookie consent** | Minimal cookies (session only); no third-party tracking |

### 14.3 Server Location Recommendations

| Jurisdiction | Data Protection Strength | Hetzner Availability | Recommendation |
|-------------|------------------------|---------------------|----------------|
| **Germany** (Falkenstein, Nuremberg) | Excellent (GDPR + BDSG) | Primary DC locations | **First choice** -- strong data protection, well-connected, Hetzner HQ |
| **Finland** (Helsinki) | Excellent (GDPR + Finnish DPA) | Hetzner DC | Good alternative -- additional geographic redundancy |
| **Netherlands** | Excellent (GDPR + Dutch DPA) | Various providers | Good for European deployment |
| **United States** | Moderate (no federal data protection law; CLOUD Act allows cross-border access) | AWS/GCP | Acceptable for public/open data; avoid for personal data of EU users |
| **Singapore** | Good (PDPA) | Various providers | For Asia-Pacific serving |

**Recommendation:** Host the primary Causal Atlas instance on Hetzner in Germany (Falkenstein or Nuremberg). This provides GDPR compliance by default, strong data protection, and the best price-performance ratio. For a CDN layer, use Cloudflare which has PoPs globally but does not store data persistently.

### 14.4 Responsible Data Handling for Conflict Data

Causal Atlas handles data about armed conflict, which requires ethical consideration beyond legal compliance:

1. **Do not expose precise event locations:** ACLED events are geocoded to specific coordinates. Our 0.5-degree grid aggregation naturally anonymises, but the raw data partition should be access-controlled

2. **Do not enable targeting:** If the system identifies causal predictors of conflict, this information could theoretically be misused. Follow the VIEWS project's responsible disclosure framework -- publish findings in academic venues, not as real-time operational intelligence

3. **Consider the affected populations:** People in conflict zones are the subjects of this data. Design the platform with their interests in mind. Display data respectfully, not sensationally

4. **Avoid hosting in conflict-party jurisdictions:** Do not host servers containing conflict data in countries that are parties to the conflicts described in the data

Source: [UNHCR Data Protection](https://www.unhcr.org/us/data-protection), [Data Protection in Humanitarian Action (Journal)](https://jhumanitarianaction.springeropen.com/articles/10.1186/s41018-020-00078-0), [GDPR and Server Location](https://techgdpr.com/blog/server-location-gdpr/)

---

## 15. Backup and Disaster Recovery

> **Checked:** March 2025

### 15.1 The 3-2-1 Rule Applied to Causal Atlas

The 3-2-1 backup rule: keep **3** copies of data, on **2** different media types, with **1** offsite.

| Copy | Location | Media | What | Update Frequency |
|------|----------|-------|------|-----------------|
| **Primary** | Server NVMe SSD | NVMe Gen4 | Processed Parquet + analysis results | Live (current data) |
| **Local backup** | Server HDD (RAID 1 mirror) | 7200 RPM HDD | Full mirror of processed data + raw archive | Daily rsync |
| **Offsite backup** | Backblaze B2 or Hetzner Storage Box | Cloud object storage | Processed data + analysis results + config | Daily rclone sync |

### 15.2 Data Classification: Regenerable vs Irreplaceable

| Data Category | Regenerable? | Backup Priority | Recovery Method |
|--------------|-------------|-----------------|-----------------|
| **Raw downloads** (ACLED CSV, CHIRPS TIFFs, etc.) | Yes -- re-download from source APIs | LOW | Re-run adapters in full-refresh mode |
| **Processed Parquet files** (canonical grid data) | Yes -- re-process from raw data | MEDIUM | Re-run adapter pipeline (hours to days) |
| **Analysis results** (PCMCI outputs, correlations) | Expensive to regenerate (hours-days of CPU) | HIGH | Restore from backup; re-run if lost |
| **Claude interpretations** (cached AI narratives) | Regenerable but costs money ($) | MEDIUM | Re-run interpretation pipeline |
| **User annotations** (causal link labels, comments) | **Irreplaceable** | CRITICAL | Must be backed up; no re-generation possible |
| **Configuration** (adapter configs, API keys, .env) | Partially regenerable | HIGH | Version-controlled in Git (sans secrets) |
| **DuckDB materialized views** | Regenerable from Parquet | LOW | Rebuild from setup_views.sql |

### 15.3 Automated Backup Scripts

**Daily backup to Backblaze B2:**

```bash
#!/bin/bash
# /opt/causal-atlas/scripts/daily-backup.sh
# Cron: 0 2 * * * /opt/causal-atlas/scripts/daily-backup.sh

set -euo pipefail

LOG="/var/log/causal-atlas/backup-$(date +%Y%m%d).log"
REMOTE="b2:causal-atlas-backup"  # rclone remote

exec >> "$LOG" 2>&1
echo "=== Backup started: $(date -u) ==="

# 1. Sync processed Parquet (incremental -- only changed files)
echo "--- Syncing processed Parquet ---"
rclone sync /data/processed/ "$REMOTE/processed/" \
    --fast-list \
    --transfers 8 \
    --checkers 16 \
    --stats 60s \
    --stats-one-line \
    --log-level INFO

# 2. Sync analysis results (irreplaceable computations)
echo "--- Syncing analysis results ---"
rclone sync /data/analysis/ "$REMOTE/analysis/" \
    --fast-list \
    --transfers 4

# 3. Sync user annotations (critical -- irreplaceable)
echo "--- Syncing annotations ---"
rclone sync /data/annotations/ "$REMOTE/annotations/" \
    --fast-list

# 4. Backup DuckDB databases (small, fast)
echo "--- Backing up DuckDB ---"
rclone copy /data/causal_atlas.duckdb "$REMOTE/duckdb/" \
    --immutable

# 5. Backup configuration (exclude secrets)
echo "--- Backing up config ---"
rclone sync /opt/causal-atlas/config/ "$REMOTE/config/" \
    --exclude ".env" \
    --exclude "*.key"

echo "=== Backup completed: $(date -u) ==="

# Verify a random sample of backed-up files
echo "--- Verification ---"
rclone check /data/processed/ "$REMOTE/processed/" \
    --one-way \
    --size-only \
    --stats-one-line \
    2>&1 | tail -3
```

**Weekly backup to Hetzner Storage Box (secondary offsite):**

```bash
#!/bin/bash
# /opt/causal-atlas/scripts/weekly-backup-hetzner.sh
# Cron: 0 4 * * 0 /opt/causal-atlas/scripts/weekly-backup-hetzner.sh

set -euo pipefail

REMOTE="hetzner-storagebox:causal-atlas"

# Full sync of all critical data
rclone sync /data/processed/ "$REMOTE/processed/" --fast-list --transfers 4
rclone sync /data/analysis/ "$REMOTE/analysis/" --fast-list
rclone sync /data/annotations/ "$REMOTE/annotations/"

# Also sync raw data checksums (for verifying re-downloads)
find /data/raw/ -name "*.sha256" | while read f; do
    rclone copy "$f" "$REMOTE/raw-checksums/$(dirname ${f#/data/raw/})/"
done
```

**rclone remote configuration:**

```bash
# Configure Backblaze B2
rclone config create b2 b2 \
    account YOUR_B2_KEY_ID \
    key YOUR_B2_APPLICATION_KEY

# Configure Hetzner Storage Box (via SFTP)
rclone config create hetzner-storagebox sftp \
    host uXXXXXX.your-storagebox.de \
    user uXXXXXX \
    port 23 \
    key_file /root/.ssh/hetzner_storagebox_key
```

### 15.4 Recovery Time Objectives

| Scenario | Recovery Time Objective (RTO) | Recovery Point Objective (RPO) | Procedure |
|----------|------------------------------|-------------------------------|-----------|
| **Single file corruption** | < 15 minutes | Last backup (< 24 hours) | Restore specific file from B2 |
| **NVMe drive failure** | 2-4 hours | Last backup (< 24 hours) | Replace drive, restore from B2 |
| **Full server failure** | 4-8 hours | Last backup (< 24 hours) | Provision new Hetzner server, restore from B2 |
| **Datacenter outage** | 8-24 hours | Last backup (< 24 hours) | Provision in different DC, restore from B2 |
| **Accidental data deletion** | 15-60 minutes | Last backup (< 24 hours) | Restore from B2 (versioning enabled) |

**B2 versioning:** Enable B2 file versioning to protect against accidental deletion and ransomware. B2 keeps previous versions for a configurable retention period (recommend 30 days). This allows point-in-time recovery.

```bash
# Enable versioning on B2 bucket
b2 update-bucket --lifecycle '{"daysFromHidingToDeleting": 30, "daysFromUploadingToHiding": null}' causal-atlas-backup allPublic
```

### 15.5 Cost of Backups

| Service | Storage | Monthly Cost | Notes |
|---------|---------|-------------|-------|
| **Backblaze B2** (primary offsite) | 200 GB processed + 50 GB analysis | ~$1.50/month ($0.006/GB) | + $0.01/GB download on restore |
| **Hetzner Storage Box** (secondary) | 1 TB plan | ~$4.00/month | Unlimited traffic to/from Hetzner DCs |
| **Total backup cost** | | ~$5.50/month | |

At ~$5.50/month for dual-offsite backup of all critical data, backup costs are negligible and not worth economising on.

---

## 16. Network Architecture

> **Checked:** March 2025

### 16.1 Home Lab Setup

For running Causal Atlas from a home server (development or small-scale deployment):

```
Internet
    │
    ▼
┌────────────────┐
│  ISP Router    │  WAN IP: dynamic (or static if available)
│  NAT/Firewall  │
└────────┬───────┘
         │ LAN (192.168.1.0/24)
         │
    ┌────┴────────────────────────┐
    │  Home Network Switch        │
    │  (Gigabit minimum)          │
    ├─────────┬──────────┬────────┤
    │         │          │        │
    ▼         ▼          ▼        ▼
  Other    Causal      NAS     Developer
  devices  Atlas      (backup)  laptop
           Server
           .100                  .101
```

**Static IP vs Dynamic DNS:**

| Option | Cost | Reliability | Setup Complexity |
|--------|------|-------------|-----------------|
| **Static IP from ISP** | $5-20/month (if available) | Best -- never changes | Low -- point DNS A record to IP |
| **Dynamic DNS (DuckDNS)** | Free | Good -- updates within 60s of IP change | Low -- run ddclient daemon |
| **Cloudflare Tunnel** | Free | Excellent -- no port forwarding needed | Medium -- install cloudflared |

**Recommended: Cloudflare Tunnel (zero-trust, no port forwarding):**

```bash
# Install cloudflared
curl -L --output cloudflared.deb \
    https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# Authenticate
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create causal-atlas

# Configure tunnel (/etc/cloudflared/config.yml)
cat <<'EOF' | sudo tee /etc/cloudflared/config.yml
tunnel: causal-atlas
credentials-file: /root/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: atlas.example.com
    service: http://localhost:8000
  - hostname: grafana.example.com
    service: http://localhost:3000
  - service: http_status:404
EOF

# Run as service
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

**Advantages of Cloudflare Tunnel:**
- No port forwarding required on home router
- No static IP needed
- Built-in DDoS protection
- Free with Cloudflare account
- SSH access possible via `cloudflared access` (no exposed SSH port)

### 16.2 Hetzner Network Configuration

For Hetzner dedicated servers (AX102 / AX162-S):

```
Internet
    │
    ▼
┌────────────────────┐
│  Cloudflare CDN    │  DNS + CDN + DDoS
│  (free tier)       │  protection
└────────┬───────────┘
         │  Origin pull
         ▼
┌────────────────────┐
│  Hetzner Firewall  │  Allow: 80/443 (from Cloudflare IPs only)
│  (Cloud Firewall)  │  Allow: SSH from admin IPs only
└────────┬───────────┘
         │
┌────────┴───────────┐
│  AX102 / AX162-S   │  Primary IP: x.x.x.x
│  Ubuntu 24.04 LTS  │  Floating IP: y.y.y.y (optional, for failover)
│                    │
│  ┌──────────────┐  │
│  │  Docker       │  │
│  │  Compose      │  │
│  │  network      │  │
│  │  (bridge)     │  │
│  └──────────────┘  │
└────────────────────┘
```

**Hetzner Firewall rules (via hcloud CLI or web console):**

```bash
# Install hcloud CLI
brew install hcloud  # or download from GitHub

# Create firewall
hcloud firewall create --name causal-atlas-fw

# Allow SSH from admin IP only
hcloud firewall add-rule causal-atlas-fw \
    --direction in --protocol tcp --port 22 \
    --source-ips "YOUR_ADMIN_IP/32" \
    --description "SSH from admin"

# Allow HTTP/HTTPS from Cloudflare IPs only
# Cloudflare IPv4 ranges: https://www.cloudflare.com/ips-v4
for ip in 173.245.48.0/20 103.21.244.0/22 103.22.200.0/22 \
          103.31.4.0/22 141.101.64.0/18 108.162.192.0/18 \
          190.93.240.0/20 188.114.96.0/20 197.234.240.0/22 \
          198.41.128.0/17 162.158.0.0/15 104.16.0.0/13 \
          104.24.0.0/14 172.64.0.0/13 131.0.72.0/22; do
    hcloud firewall add-rule causal-atlas-fw \
        --direction in --protocol tcp --port 80 \
        --source-ips "$ip" \
        --description "HTTP from Cloudflare"
    hcloud firewall add-rule causal-atlas-fw \
        --direction in --protocol tcp --port 443 \
        --source-ips "$ip" \
        --description "HTTPS from Cloudflare"
done
```

### 16.3 SSH Hardening

```bash
# /etc/ssh/sshd_config.d/hardening.conf
# Apply to both home lab and Hetzner servers

# Disable password authentication (key-only)
PasswordAuthentication no
ChallengeResponseAuthentication no

# Disable root login
PermitRootLogin no

# Only allow specific users
AllowUsers causal-atlas

# Use strong key exchange and ciphers
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Rate limiting (fail2ban handles the rest)
MaxAuthTries 3
LoginGraceTime 30

# Idle timeout (disconnect after 15 min of inactivity)
ClientAliveInterval 300
ClientAliveCountMax 3
```

```bash
# Install and configure fail2ban
sudo apt install -y fail2ban

cat <<'EOF' | sudo tee /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
EOF

sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 16.4 Cloudflare Free Tier Configuration

```
Cloudflare Free Tier provides:
- DNS hosting (fast, anycast)
- CDN (static asset caching at edge)
- DDoS protection (L3/L4 + basic L7)
- SSL/TLS (Full Strict mode with origin cert)
- 1 page rule
- 1 rate limiting rule
- Web Application Firewall (basic rules)
- Analytics

Configuration for Causal Atlas:
1. Set SSL/TLS mode to "Full (Strict)"
2. Create origin certificate (15-year, installed on Hetzner server)
3. Enable "Always Use HTTPS"
4. Set minimum TLS version to 1.2
5. Enable HSTS (max-age=31536000, includeSubDomains)
6. Cache level: Standard
7. Browser cache TTL: 4 hours (for API responses)
8. Under-attack mode: Off (enable manually during DDoS)
```

---

## 17. Complete Build Guides

> **Checked:** March 2025
>
> **Pricing note:** DDR5 RAM prices are significantly elevated as of early 2026 due to global AI-driven DRAM shortages. The prices below reflect current market conditions. Monitor [Tom's Hardware RAM Price Index](https://www.tomshardware.com/pc-components/ram/ram-price-index-2026-lowest-price-on-ddr5-and-ddr4-memory-of-all-capacities) for price movements before purchasing.

### 17.1 Recommended Mid-Range Build: Complete Parts List

This build targets continental-scale PCMCI analysis, full data pipeline operation, and comfortable DuckDB querying of the complete processed dataset.

| # | Component | Exact Model | Est. Price (Mar 2025) | Notes |
|---|-----------|------------|----------------------|-------|
| 1 | **CPU** | AMD Ryzen 9 9900X (12C/24T, 4.4-5.6 GHz, AM5) | $360-390 | Currently ~$360-390 at Amazon/Micro Center. 170W TDP. No cooler included |
| 2 | **CPU Cooler** | Noctua NH-D15 chromax.black | $110 | Dual-tower air cooler, quiet, handles 250W+. Includes AM5 mounting kit |
| 3 | **Motherboard** | ASUS TUF Gaming B650E-PLUS WiFi | $200-220 | AM5, DDR5, 2x M.2 slots, 2.5GbE, WiFi 6E, PCIe 4.0 x16 |
| 4 | **RAM** | G.Skill Trident Z5 64GB (2x32GB) DDR5-5600 CL36 | $500-700 | Price highly volatile. Check current listings. DDR5-5600 is the sweet spot for Ryzen 9000 |
| 5 | **Boot SSD** | WD Black SN850X 1 TB NVMe Gen4 | $85-100 | 7,300/6,300 MB/s. OS + applications |
| 6 | **Data SSD** | Samsung 990 Pro 4 TB NVMe Gen4 | $320-540 | 7,450/6,900 MB/s. Parquet files + raw data. Price currently elevated (~$540 at Amazon) |
| 7 | **Archive HDD** | Seagate IronWolf 8 TB (ST8000VN004) | $150-170 | 7200 RPM, CMR, 3-year warranty. For raw data archive and local backups |
| 8 | **GPU** | *(Optional)* NVIDIA RTX 4060 Ti 16GB | $400-450 | Only if planning RAPIDS/GNN work. Skip to save ~$430 |
| 9 | **PSU** | Corsair RM750x (2024) 750W 80+ Gold | $100-110 | Fully modular, ATX 3.1, quiet fan mode. 850W if adding GPU |
| 10 | **Case** | Fractal Design Meshify 2 Compact | $110-130 | Excellent airflow, mesh front, 2x 140mm fans included, supports full ATX |
| 11 | **Case Fans** | 2x Noctua NF-A14 PWM (140mm) | $55 (2-pack) | Add as front intake. Total: 4 fans (2 front intake + 1 rear + 1 top exhaust) |

| | **Total (without GPU)** | | **~$1,890-2,415** |
|---|---|---|---|
| | **Total (with GPU)** | | **~$2,290-2,865** |

**Cost-saving alternatives:**
- RAM: If 64 GB DDR5 exceeds $600, consider a DDR4 AM4 build (Ryzen 7 5800X + 64 GB DDR4-3600 for ~$200-250 total CPU+RAM savings)
- Data SSD: Crucial T500 4TB ($250-300) is a viable alternative to the Samsung 990 Pro when the Samsung is at elevated pricing
- Cooler: Thermalright Peerless Assassin 120 SE ($35) is 90% of the Noctua's performance at 30% of the price

### 17.2 Assembly Notes

**What to watch out for:**

1. **AM5 socket handling:** The CPU has no pins (LGA), but the socket has delicate pins. Lower the CPU straight down -- do not slide it. Verify the golden triangle on the CPU aligns with the triangle on the socket

2. **NVMe SSD placement:** The M.2 slot closest to the CPU (M.2_1) typically connects directly via CPU PCIe lanes and is fastest. Use it for the boot SSD. The second slot (M.2_2) goes through the chipset -- use it for the data SSD

3. **RAM DIMM slots:** For 2-DIMM kits, use slots A2 and B2 (second and fourth from the CPU). This is the standard for dual-channel operation on most AM5 motherboards. Check the motherboard manual

4. **CPU cooler clearance:** The NH-D15 is 165mm tall. The Meshify 2 Compact supports up to 169mm. This is tight but works. Verify before ordering if using a different case

5. **PSU cable management:** Route the 24-pin ATX and 8-pin CPU cables through the back panel before starting component installation. The Meshify 2 Compact has good cable management space behind the motherboard tray

6. **Thermal paste:** The NH-D15 comes with pre-applied thermal paste on the base. If you prefer to apply your own, use Noctua NT-H1 (included in box) or Thermal Grizzly Kryonaut. Rice-grain size in the centre of the CPU IHS

### 17.3 Ubuntu 24.04 LTS Installation

**Pre-installation:**

```
1. Download Ubuntu Server 24.04 LTS ISO from ubuntu.com/download/server
2. Create bootable USB with: dd if=ubuntu-24.04-live-server-amd64.iso of=/dev/sdX bs=4M status=progress
   (Or use Rufus/Ventoy on Windows)
3. Boot from USB (press F2/DEL for BIOS, set USB as first boot device)
```

**Installation choices:**

| Setting | Recommendation |
|---------|---------------|
| Language | English |
| Keyboard | Your layout |
| Network | DHCP initially; configure static IP post-install |
| Storage layout | **Custom:** See partition table below |
| Profile | Username: `causal-atlas` (or your preference) |
| SSH | Install OpenSSH server: Yes |
| Snaps | None (we install everything via apt/pip) |

**Partition table:**

```
/dev/nvme0n1 (1 TB boot SSD):
  /dev/nvme0n1p1    512 MB    EFI System Partition    fat32
  /dev/nvme0n1p2    48 GB     swap                    swap
  /dev/nvme0n1p3    remainder /                       ext4

/dev/nvme1n1 (4 TB data SSD):
  /dev/nvme1n1p1    4 TB      /data                   xfs

/dev/sda (8 TB HDD):
  /dev/sda1         8 TB      /archive                xfs
```

**Why 48 GB swap:** With 64 GB RAM, 48 GB swap provides a safety net for larger-than-memory DuckDB queries without excessive SSD wear. For 128 GB RAM systems, 32 GB swap is sufficient.

### 17.4 Post-Install Setup Script

```bash
#!/bin/bash
# post-install.sh -- Run after fresh Ubuntu 24.04 LTS Server installation
# Usage: sudo bash post-install.sh
#
# This script installs all software required for Causal Atlas development
# and configures the system for optimal performance.

set -euo pipefail

echo "=== Causal Atlas: Post-Install Setup ==="
echo "Date: $(date)"
echo "Host: $(hostname)"
echo ""

# ── 1. System Update ──────────────────────────────────────────
echo "--- 1. Updating system packages ---"
apt update && apt upgrade -y
apt autoremove -y

# ── 2. Essential System Packages ──────────────────────────────
echo "--- 2. Installing essential packages ---"
apt install -y \
    build-essential cmake pkg-config git git-lfs curl wget unzip \
    htop glances iotop ncdu tmux duf \
    tree jq ripgrep fd-find \
    ufw fail2ban \
    lm-sensors smartmontools nvme-cli \
    net-tools iperf3

# ── 3. Geospatial C/C++ Libraries ────────────────────────────
echo "--- 3. Installing geospatial libraries ---"
apt install -y \
    libgdal-dev gdal-bin python3-gdal \
    libgeos-dev libproj-dev proj-data proj-bin \
    libspatialindex-dev

# ── 4. HDF5 and NetCDF (for climate data) ────────────────────
echo "--- 4. Installing HDF5/NetCDF ---"
apt install -y \
    libhdf5-dev libnetcdf-dev netcdf-bin

# ── 5. Image and Compression Libraries ───────────────────────
echo "--- 5. Installing image/compression libraries ---"
apt install -y \
    libjpeg-dev libpng-dev libtiff-dev \
    zlib1g-dev liblz4-dev libzstd-dev

# ── 6. Python Environment ────────────────────────────────────
echo "--- 6. Setting up Python environment ---"
apt install -y python3-dev python3-pip python3-venv

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create project virtual environment
mkdir -p /opt/causal-atlas
cd /opt/causal-atlas
uv venv --python 3.12 .venv
source .venv/bin/activate

# Install Python packages
uv pip install \
    numpy pandas scipy scikit-learn statsmodels \
    geopandas rasterio xarray shapely fiona pyproj \
    rasterstats pysal \
    tigramite \
    duckdb pyarrow polars h5py netCDF4 \
    fastapi "uvicorn[standard]" pydantic pydantic-settings \
    matplotlib plotly \
    structlog tenacity httpx \
    anthropic \
    pytest ruff mypy ipython \
    rclone-python

echo "Python packages installed successfully"

# ── 7. Node.js (for React frontend) ──────────────────────────
echo "--- 7. Installing Node.js ---"
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# ── 8. Docker ─────────────────────────────────────────────────
echo "--- 8. Installing Docker ---"
apt install -y docker.io docker-compose-v2
usermod -aG docker causal-atlas
systemctl enable docker

# ── 9. Firewall ───────────────────────────────────────────────
echo "--- 9. Configuring firewall ---"
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# ── 10. SSH Hardening ─────────────────────────────────────────
echo "--- 10. Hardening SSH ---"
cat > /etc/ssh/sshd_config.d/hardening.conf <<'SSHEOF'
PasswordAuthentication no
ChallengeResponseAuthentication no
PermitRootLogin no
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 3
SSHEOF
systemctl restart sshd

# ── 11. fail2ban ──────────────────────────────────────────────
echo "--- 11. Configuring fail2ban ---"
cat > /etc/fail2ban/jail.local <<'F2BEOF'
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
F2BEOF
systemctl enable fail2ban
systemctl start fail2ban

# ── 12. Data Directories ─────────────────────────────────────
echo "--- 12. Creating data directories ---"
mkdir -p /data/{raw,processed,analysis,grid,tiles,exports,annotations}
mkdir -p /data/processed/{domain=conflict,domain=climate,domain=food_security}
mkdir -p /data/processed/{domain=natural_hazards,domain=environment,domain=socioeconomic}
mkdir -p /data/.checkpoints
chown -R causal-atlas:causal-atlas /data

# ── 13. Log Directory ─────────────────────────────────────────
mkdir -p /var/log/causal-atlas
chown causal-atlas:causal-atlas /var/log/causal-atlas

# ── 14. Sensors Detection ─────────────────────────────────────
echo "--- 14. Detecting hardware sensors ---"
sensors-detect --auto || true
echo "Run 'sensors' to check CPU temperatures"

# ── 15. Performance Tuning ────────────────────────────────────
echo "--- 15. Applying performance tuning ---"

# Increase inotify watches (for file-based triggers)
echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf

# Increase open file limits (for DuckDB with many Parquet files)
cat >> /etc/security/limits.conf <<'LIMEOF'
causal-atlas soft nofile 65536
causal-atlas hard nofile 65536
LIMEOF

# Optimize for NVMe I/O scheduler
echo "none" > /sys/block/nvme0n1/queue/scheduler 2>/dev/null || true
echo "none" > /sys/block/nvme1n1/queue/scheduler 2>/dev/null || true

sysctl -p

# ── Summary ───────────────────────────────────────────────────
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Log out and back in (for Docker group membership)"
echo "  2. Copy SSH public key: ssh-copy-id causal-atlas@<this-server>"
echo "  3. Clone the repo: git clone https://github.com/aldred-coetzee/causal-atlas.git /opt/causal-atlas/repo"
echo "  4. Create .env file with API keys (ACLED_API_KEY, CLAUDE_API_KEY)"
echo "  5. Run benchmarks: bash /opt/causal-atlas/scripts/benchmark.sh"
echo "  6. Verify GPU (if installed): nvidia-smi"
echo ""
echo "System info:"
echo "  CPU: $(lscpu | grep 'Model name' | sed 's/Model name: *//')"
echo "  RAM: $(free -h | awk '/Mem:/ {print $2}')"
echo "  Disks:"
lsblk -d -o NAME,SIZE,MODEL | grep -v loop
echo "  Python: $(python3 --version)"
echo "  DuckDB: $(python3 -c 'import duckdb; print(duckdb.__version__)')"
echo "  GDAL: $(gdal-config --version)"
```

### 17.5 Performance Verification Tests

After completing the build and post-install setup, run these tests to verify the system meets expectations:

```bash
#!/bin/bash
# scripts/verify-build.sh -- Verify build performance meets Causal Atlas requirements

set -euo pipefail

echo "=== Causal Atlas Build Verification ==="
echo "Date: $(date)"
echo "Host: $(hostname)"
echo ""

# ── 1. CPU ──────────────────────────────────────────────────
echo "--- 1. CPU Info ---"
lscpu | grep -E "Model name|CPU\(s\)|Thread|Core|MHz"
echo ""

# ── 2. Memory ───────────────────────────────────────────────
echo "--- 2. Memory ---"
free -h
echo ""

# ── 3. Storage ──────────────────────────────────────────────
echo "--- 3. Storage ---"
df -h /data /archive / 2>/dev/null || df -h
echo ""

# ── 4. DuckDB Benchmark ────────────────────────────────────
echo "--- 4. DuckDB Parquet Benchmark ---"
source /opt/causal-atlas/.venv/bin/activate

python3 -c "
import time
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb

# Generate test data (10M rows)
print('Generating 10M row test dataset...')
n = 10_000_000
table = pa.table({
    'gid': np.random.randint(1, 259201, n, dtype=np.int32),
    'year': np.random.randint(2015, 2025, n, dtype=np.int16),
    'month': np.random.randint(1, 13, n, dtype=np.int8),
    'variable': np.random.choice(['var_' + str(i) for i in range(20)], n),
    'value': np.random.randn(n).astype(np.float64),
})
pq.write_table(table, '/tmp/verify_bench.parquet', compression='snappy', row_group_size=100_000)
size_mb = pq.read_metadata('/tmp/verify_bench.parquet').serialized_size / 1e6
print(f'  File size: {size_mb:.1f} MB')

con = duckdb.connect()

# Full scan
start = time.perf_counter()
con.execute('SELECT variable, AVG(value), COUNT(*) FROM read_parquet(\"/tmp/verify_bench.parquet\") GROUP BY variable').fetchall()
t1 = time.perf_counter() - start
status1 = 'PASS' if t1 < 2 else 'SLOW'
print(f'  Full scan + aggregation: {t1:.3f}s [{status1}] (target < 2s)')

# Point query
start = time.perf_counter()
con.execute('SELECT year, month, variable, value FROM read_parquet(\"/tmp/verify_bench.parquet\") WHERE gid = 142567 ORDER BY variable, year, month').fetchall()
t2 = time.perf_counter() - start
status2 = 'PASS' if t2 < 0.2 else 'SLOW'
print(f'  Point query (single cell): {t2:.3f}s [{status2}] (target < 0.2s)')

con.close()
import os
os.unlink('/tmp/verify_bench.parquet')
"

echo ""

# ── 5. PCMCI Benchmark ─────────────────────────────────────
echo "--- 5. PCMCI Single-Cell Benchmark ---"
python3 -c "
import time
import numpy as np
from tigramite import data_processing as pp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

np.random.seed(42)
data = np.random.randn(120, 20)
data[:, 1] = 0.5 * data[:, 0] + 0.5 * np.random.randn(120)

dataframe = pp.DataFrame(data, var_names=[f'v{i}' for i in range(20)])
pcmci = PCMCI(dataframe=dataframe, cond_ind_test=ParCorr(significance='analytic'), verbosity=0)

start = time.perf_counter()
results = pcmci.run_pcmci(tau_max=12, pc_alpha=0.05)
elapsed = time.perf_counter() - start

status = 'PASS' if elapsed < 30 else 'SLOW'
print(f'  Single cell (20 vars, T=120, tau_max=12): {elapsed:.2f}s [{status}] (target < 30s)')

import multiprocessing
cores = multiprocessing.cpu_count()
global_hours = (elapsed * 64800) / cores / 3600
print(f'  Estimated global land ({cores} threads): {global_hours:.1f} hours')
"

echo ""

# ── 6. Disk I/O ────────────────────────────────────────────
echo "--- 6. Disk I/O (quick test) ---"
if command -v fio &>/dev/null; then
    # 1 GB sequential read
    fio --name=quick-read --rw=read --bs=1M --size=1G --numjobs=1 \
        --directory=/data --ioengine=libaio --direct=1 --runtime=10 \
        --output-format=json 2>/dev/null | \
        python3 -c "import sys,json; d=json.load(sys.stdin); r=d['jobs'][0]['read']; print(f'  Sequential read: {r[\"bw\"]/1024:.0f} MB/s')"

    # Clean up
    rm -f /data/quick-read.0.0
else
    echo "  fio not installed -- skipping disk benchmark"
    echo "  Install with: sudo apt install -y fio"
fi

echo ""

# ── 7. Network ─────────────────────────────────────────────
echo "--- 7. Network bandwidth (Cloudflare test) ---"
speed=$(curl -s -o /dev/null -w "%{speed_download}" https://speed.cloudflare.com/__down?bytes=50000000 2>/dev/null)
speed_mbps=$(python3 -c "print(f'{$speed * 8 / 1e6:.1f}')")
echo "  Download speed: ${speed_mbps} Mbps"

echo ""
echo "=== Verification Complete ==="
```

---

## Sources

- [AMD Ryzen 9 9950X — PassMark Benchmark](https://www.cpubenchmark.net/cpu.php?cpu=AMD+Ryzen+9+9950X&id=6211)
- [AMD Ryzen 9 9950X CPU Review — GamersNexus](https://gamersnexus.net/cpus/amd-ryzen-9-9950x-cpu-review-benchmarks-vs-7950x-9700x-14900k-more)
- [RAM Price Tracking 2026 — Tom's Hardware](https://www.tomshardware.com/pc-components/ram/ram-price-index-2026-lowest-price-on-ddr5-and-ddr4-memory-of-all-capacities)
- [64GB DDR5 RAM Pricing Crisis — TrendForce](https://www.trendforce.com/news/2025/11/27/news-64gb-ddr5-ram-reportedly-now-pricier-than-a-playstation-5-amid-soaring-memory-costs/)
- [Samsung 990 Pro 2TB — Amazon](https://www.amazon.com/SAMSUNG-Internal-Expansion-MZ-V9P2T0B-AM/dp/B0BHJJ9Y77)
- [DuckDB v1.4 LTS Benchmark Results](https://duckdb.org/2025/10/09/benchmark-results-14-lts)
- [DuckDB vs Polars: Performance on Parquet — Codecentric](https://www.codecentric.de/en/knowledge-hub/blog/duckdb-vs-polars-performance-and-memory-with-massive-parquet-data)
- [DuckDB File Formats Guide](https://duckdb.org/docs/stable/guides/performance/file_formats)
- [PCMCI — Detecting Causal Associations in Large Nonlinear Time Series — Science Advances](https://www.science.org/doi/10.1126/sciadv.aau4996)
- [Tigramite Documentation](https://jakobrunge.github.io/tigramite/)
- [RAPIDS cuDF Accelerates pandas 150x — NVIDIA Blog](https://developer.nvidia.com/blog/rapids-cudf-accelerates-pandas-nearly-150x-with-zero-code-changes/)
- [RAPIDS cuDF on Google Colab — NVIDIA Blog](https://developer.nvidia.com/blog/rapids-cudf-instantly-accelerates-pandas-up-to-50x-on-google-colab/)
- [Hetzner AX102 Dedicated Server](https://www.hetzner.com/dedicated-rootserver/ax102)
- [Hetzner AX162 with EPYC 9454P](https://www.hetzner.com/news/new-ax162/)
- [Hetzner Cloud Plans](https://www.hetzner.com/cloud)
- [AWS EC2 Pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
- [GCP Compute Engine Pricing](https://cloud.google.com/compute/all-pricing)
- [File System Performance Comparison — Command Linux](https://commandlinux.com/statistics/file-system-performance-comparison-statistics-ext4-xfs-btrfs-zfs/)
- [XFS vs ext4 — Pure Storage Blog](https://blog.purestorage.com/purely-technical/xfs-vs-ext4-which-linux-file-system-is-better/)
- [AMD Threadripper 7970X — Micro Center](https://www.microcenter.com/product/674278/amd-ryzen-threadripper-7970x-storm-peak-40ghz-32-core-str5-boxed-processor-heatsink-not-included)
- [GDELT Dataset Size — GDELT Project Blog](https://blog.gdeltproject.org/creating-a-planetary-scale-open-dataset-just-how-big-is-gdelt/)
- [CHIRPS Rainfall Data — Climate Hazards Center](https://www.chc.ucsb.edu/data/chirps)
- [System76 Pangolin Laptop](https://system76.com/laptops/pangolin)
- [Framework Laptop 16 (2025) — Tom's Guide](https://www.tomsguide.com/computing/laptops/framework-laptop-16-2025-review)
- [Lenovo ThinkPad T14s Gen 6 — Phoronix Linux Review](https://www.phoronix.com/review/amd-ryzen-ai-7-360-thinkpad-t14s-gen6)
- [Minisforum MS-A2 Mini Workstation](https://videocardz.com/newz/minisforum-launches-ms-a2-mini-workstation-with-ryzen-9-9955hx-price-starts-at-799)
- [Dell PowerEdge R750 on eBay](https://www.ebay.com/shop/dell-poweredge-r750)
- [Self-Hosted vs Cloud TCO — Cloudvara](https://cloudvara.com/cloud-vs-on-premise-costs/)
- [Ubuntu 24.04 GDAL Packages](https://packages.ubuntu.com/gdal)
- [UbuntuGIS Package List](https://wiki.ubuntu.com/UbuntuGIS/PackageList)
- [NVIDIA CUDA GPUs](https://developer.nvidia.com/cuda/gpus)
- [GPU Hierarchy 2026 — Tom's Hardware](https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html)
- [VIIRS Nighttime Lights — Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG)
- [MODIS Vegetation Index Products](https://modis.gsfc.nasa.gov/data/dataprod/mod13.php)

### Benchmarking and Performance (Section 12)
- [DuckDB Benchmarking Ourselves Over Time](https://duckdb.org/2024/06/26/benchmarks-over-time) -- Internal performance tracking
- [DuckDB vs Polars: Performance on Parquet](https://www.codecentric.de/en/knowledge-hub/blog/duckdb-vs-polars-performance-and-memory-with-massive-parquet-data) -- Comparative benchmarks
- [DuckDB Big Data on the Cheapest MacBook](https://duckdb.org/2026/03/11/big-data-on-the-cheapest-macbook) -- Real-world performance
- [Tigramite Documentation](https://jakobrunge.github.io/tigramite/) -- PCMCI implementation details
- [How to Speed Up PCMCI (GitHub Discussion)](https://github.com/jakobrunge/tigramite/discussions/208) -- Performance optimisation

### Power and Cooling (Section 13)
- [Home Server Power Consumption Guide](https://www.ecoflow.com/us/blog/home-server-power-guide) -- Power consumption estimates
- [UPS for Home Lab (How-To Geek)](https://www.howtogeek.com/your-homelab-needs-an-uninterruptible-power-supply-prime-day-2025/) -- UPS selection guide
- [Home Server Needs UPS (XDA)](https://www.xda-developers.com/home-server-needs-ups-more-than-better-specs/) -- Why UPS matters
- [Selecting UPS for Servers (NewServerLife)](https://newserverlife.com/articles/how-to-choose-ups-for-a-server/) -- Capacity sizing guide
- [UPS for 750W PSU (Linus Tech Tips)](https://linustechtips.com/topic/1528002-ups-for-750w-psu/) -- Community guidance

### Data Sovereignty and Legal (Section 14)
- [GDPR and Server Location (TechGDPR)](https://techgdpr.com/blog/server-location-gdpr/) -- Does server location matter?
- [UNHCR Data Protection Policy](https://www.unhcr.org/us/data-protection) -- Humanitarian data protection
- [Data Protection in Humanitarian Action (Journal)](https://jhumanitarianaction.springeropen.com/articles/10.1186/s41018-020-00078-0) -- GDPR and NGO data collection
- [UNHCR Renewed Data Protection Approach](https://www.unhcr.org/blogs/a-renewed-approach-towards-personal-data-protection-in-the-un-refugee-agency/) -- Updated 2024 framework

### Backup and Disaster Recovery (Section 15)
- [Backblaze B2 + rclone Documentation](https://rclone.org/b2/) -- rclone B2 integration
- [Backblaze B2 rclone Quickstart](https://help.backblaze.com/hc/en-us/articles/1260804565710-Quickstart-Guide-for-Rclone-and-B2-Cloud-Storage) -- Setup guide
- [Cloud Backup with rclone (Arnaud Loos)](https://arnaudloos.com/2019/cloud-backup-with-rclone.md/) -- Automated backup patterns
- [Backup to B2 with restic + rclone](https://jdheyburn.co.uk/blog/backup-to-backblaze-b2-using-restic-and-rclone/) -- Alternative backup approach

### Network Architecture (Section 16)
- [Cloudflare Free Plan Features](https://www.cloudflare.com/plans/free/) -- CDN and DDoS protection
- [Cloudflare DDoS Protection Best Practices](https://developers.cloudflare.com/ddos-protection/best-practices/) -- Configuration guidance
- [Cloudflare Rate Limiting (Free Plan)](https://eastondev.com/blog/en/posts/dev/20251201-cloudflare-rate-limiting-guide/) -- Defence against CC attacks
- [Grafana + Prometheus + Loki Home Lab Setup (XDA)](https://www.xda-developers.com/set-up-grafana-loki-prometheus-alloy-home-lab/) -- Monitoring stack

### Build Guides (Section 17)
- [AMD Ryzen 9 9900X (AMD Official)](https://www.amd.com/en/products/processors/desktops/ryzen/9000-series/amd-ryzen-9-9900x.html) -- CPU specifications
- [AMD Ryzen 9 9900X Price History (Pangoly)](https://pangoly.com/en/price-history/amd-ryzen-9-9900x) -- Price tracking
- [DDR5 RAM Price Index 2026 (Tom's Hardware)](https://www.tomshardware.com/pc-components/ram/ram-price-index-2026-lowest-price-on-ddr5-and-ddr4-memory-of-all-capacities) -- Current pricing
- [Samsung 990 Pro 4TB Price (Amazon)](https://www.amazon.com/SAMSUNG-Computing-Workstations-MZ-V9P4T0B-AM/dp/B0CHGT1KFJ) -- SSD pricing
- [Samsung 990 Pro 4TB Price History (Pangoly)](https://pangoly.com/en/price-history/samsung-990-pro-4tb) -- Price tracking
- [Ubuntu 24.04 Server Installation Guide (LinuxTechi)](https://www.linuxtechi.com/how-to-install-ubuntu-server/) -- Step-by-step installation
- [Ubuntu 24.04 Post-Install Setup (DigitalOcean)](https://www.digitalocean.com/community/tutorials/set-up-configure-application-server-ubuntu-24-04) -- Server configuration
- [nginx + Let's Encrypt Docker Compose (GitHub)](https://github.com/eugene-khyst/letsencrypt-docker-compose) -- Automated SSL setup
- [CPU Price Index 2025 (Tom's Hardware)](https://www.tomshardware.com/news/lowest-cpu-prices) -- CPU pricing tracker
