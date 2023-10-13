# Social Network Crawl Controller

## Overview

The `social_network_crawl_controller` is an open-source repository designed for crawling various social networks. This comprehensive guide will walk you through the setup and execution of the service, whether you're running it in a local or production environment.

---

## Table of Contents
- Overview
- Prerequisites
- Installation
- Configuration
  - Local Environment
  - Production Environment
- Usage
- Troubleshooting
  - Zero Items Loaded
  - Account Manager Connection Issues
- Database Setup
  - Development Environment
- Contributing
- License
- Contact

---

## Prerequisites

- Python 3.x
- MongoDB
- Docker (for development)

## Installation

Clone the repository and install the required packages:

```
git clone https://github.com/your/repository.git
cd repository
pip install -r requirements.txt
```

## Configuration

### Local Environment

1. Set `ENV` to 'local'.
2. Set `DEFAULT_SERVICE_LOCAL` to the name of the service you wish to run.

This configuration will use `service_config` from `social_networks/<name_of_social_network>/service_config_samples/<name_of_service>.json`.

### Production Environment

1. Create a Base64 encoded JSON string based on the `service_config_sample`.
2. Set this string as the `SERVICE_CONFIG` environment variable.

## Usage

Run the service with the following command:

python main.py

## Troubleshooting

### Zero Items Loaded

If no documents in your report table meet the filter conditions, zero items may be loaded. Check `social_networks/<name_of_social_network>/workflow/loading/query/report_query.py` for filter adjustments.


## Database Setup

### Development Environment

For development purposes, set up a local Docker database. To run MongoDB for Facebook or Instagram:

1. Export the config:
   `source localvar.sh`
2. Run the main script:
   `python main.py`

## Contributing

Please read the CONTRIBUTING.md for guidelines on how to contribute to the project.

## License

This project is licensed under the MIT License. See the LICENSE.md file for details.

---
