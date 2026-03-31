# VCL Job Card Tracking

A Frappe app for ERPNext that provides comprehensive job card management and tracking for Vimit Converters Limited's manufacturing operations.

## Overview

The VCL Job Card Tracking app extends ERPNext with custom DocTypes and features designed to streamline job card management, customer product specifications, and material tracking throughout the manufacturing workflow.

## Features

### DocTypes Implemented

1. **Dies** - Master data for printing dies with specifications including length, width, teeth count, and printing configuration
2. **Colour of Parts** - Manages and tracks different color specifications for manufactured parts
3. **Customer Product Specification** - Stores detailed product specifications and requirements from customers, with auto-population from Dies
4. **Job Card Computer Paper** - Tracks computer paper specifications and requirements for job cards

### Module Structure

- **Job Card Tracking Module** - Main module containing all job card-related DocTypes and functionality

## Installation

### Prerequisites
- ERPNext v13+ (with Frappe Framework)
- Python 3.10+

### Quick Setup
1. Add the app to your Frappe bench:
```bash
bench get-app vcl_job_cards https://github.com/tjharia93/vcl_job_cards.git
```

2. Install on your site:
```bash
bench --site [sitename] install-app vcl_job_cards
```

3. Rebuild assets:
```bash
bench build
```

## Project Structure

```
vcl_job_cards/
├── vcl_job_cards/
│   ├── hooks.py                 # App hooks and configuration
│   ├── modules.txt              # Module definitions
│   ├── patches.txt              # Database migrations
│   └── job_card_tracking/
│       └── doctype/             # Custom DocTypes
│           ├── colour_of_parts/
│           ├── customer_product_specification/
│           └── job_card_computer_paper/
├── pyproject.toml               # Project metadata
└── README.md                    # This file
```

## App Information

- **App Name:** vcl_job_cards
- **Version:** 0.0.1
- **Publisher:** Vimit Converters Limited
- **License:** MIT
- **Author Email:** tanuj@vimitconverters.com

## Requirements

- erpnext

## License

MIT
