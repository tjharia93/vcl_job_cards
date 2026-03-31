# VCL Job Card Tracking

A comprehensive Frappe app for ERPNext that provides advanced job card management and tracking for Vimit Converters Limited's manufacturing operations.

## Overview

The VCL Job Card Tracking app extends ERPNext with specialized DocTypes and intelligent automation features designed to streamline job card management, customer product specifications, material tracking, and printing die management throughout the manufacturing workflow.

## Features

### 🏭 Core DocTypes

#### 1. **Dies** - Printing Die Management
Master data management for printing dies with complete specifications:
- **Die Number** (unique identifier)
- **Die Size** (e.g., "27 X 27", "43 X 58")
- **Dimensions** (length, width in mm)
- **Printing Configuration** (across ups, round ups, teeth count)
- **Material & Quantity** (material type, packing pieces)
- **Shape Classification** (square, rectangle, circle, irregular, etc.)

#### 2. **Customer Product Specification** - Product Requirements
Comprehensive product specification management with intelligent auto-population:
- **Product Types**: Computer Paper, Carton, Label, Exercise Books
- **Detailed Specifications** per product type
- **Dies Integration**: Auto-populate label specifications from selected die
- **Validation Rules**: Automatic validation based on product type
- **Customer Linking**: Direct association with customer records

#### 3. **Colour of Parts** - Color Management
Advanced color specification tracking for multi-part documents:
- **Sequential Part Numbering** (auto-generated)
- **Color Assignment** per part
- **Paper Type & GSM** validation
- **Automatic Rule Application** (first/middle/last part rules)

#### 4. **Job Card Computer Paper** - Paper Specifications
Specialized tracking for computer paper job cards:
- **Paper Specifications** (size, type, GSM)
- **Printing Requirements** (colors, plates)
- **Quality Control** parameters

### 🚀 Intelligent Automation

#### Auto-Population from Dies
When creating label specifications, selecting a die automatically populates:
- **Label Length** ← Die length
- **Label Width** ← Die width
- **Cylinder Teeth** ← Die teeth count
- **Plate Up** ← Die across ups
- **Plate Round** ← Die round ups
- **Packing Pieces** ← Die quantity

#### Smart Validation
- **Product Type Validation**: Required fields based on selected product type
- **Computer Paper Rules**: Automatic paper type/GSM assignment based on part position
- **Die Integration**: Validation ensures die selection for label products
- **Sequential Numbering**: Automatic part numbering with validation

### 📊 Module Structure

- **Job Card Tracking Module** - Main module containing all manufacturing-related DocTypes
- **Integrated ERPNext Compatibility** - Seamless integration with ERPNext core modules
- **Customer Management** - Direct linking with ERPNext Customer DocType

## Installation

### Prerequisites
- **ERPNext**: v13+ (with Frappe Framework v13+)
- **Python**: 3.10+
- **Database**: MariaDB/MySQL

### Quick Setup

1. **Add the app to your Frappe bench:**
```bash
bench get-app vcl_job_cards https://github.com/tjharia93/vcl_job_cards.git
```

2. **Install on your site:**
```bash
bench --site [sitename] install-app vcl_job_cards
```

3. **Rebuild assets:**
```bash
bench build
```

4. **Migrate database:**
```bash
bench --site [sitename] migrate
```

### Manual Installation

If you prefer manual installation:

```bash
# Clone the repository
git clone https://github.com/tjharia93/vcl_job_cards.git

# Install Python dependencies
pip install -r requirements.txt

# Install the app
bench --site [sitename] install-app vcl_job_cards
```

## Usage Guide

### Creating Dies

1. Navigate to **Job Card Tracking > Dies**
2. Click **New**
3. Fill in die specifications:
   - Die Number (unique)
   - Die Size (descriptive)
   - Length and Width (mm)
   - Printing parameters (across ups, round ups, teeth)
   - Material and quantity information

### Customer Product Specifications

1. Navigate to **Job Card Tracking > Customer Product Specification**
2. Select **Product Type** (Computer Paper, Carton, Label, Exercise Books)
3. Fill product-specific fields
4. **For Labels**: Select a Die to auto-populate specifications
5. Save and validate

### Auto-Population Workflow

```
1. Create Die Record → 2. Create Customer Product Spec → 3. Select Die → 4. Fields Auto-Populate
```

### Validation Rules

- **Computer Paper**: Number of parts must match colour specifications
- **Labels**: Die selection required, dimensions auto-populated
- **Exercise Books**: Page count must be divisible by 4
- **All Products**: Customer and product type required

## Project Structure

```
vcl_job_cards/
├── vcl_job_cards/
│   ├── __init__.py                    # App initialization
│   ├── hooks.py                       # App hooks and configuration
│   ├── modules.txt                    # Module definitions
│   ├── patches.txt                    # Database migration scripts
│   └── job_card_tracking/             # Main module
│       └── doctype/                   # Custom DocTypes
│           ├── dies/                  # Printing dies management
│           │   ├── __init__.py
│           │   ├── dies.json          # DocType configuration
│           │   └── dies.py            # Backend logic
│           ├── customer_product_specification/
│           │   ├── __init__.py
│           │   ├── customer_product_specification.json
│           │   ├── customer_product_specification.py
│           │   └── customer_product_specification.js  # Frontend logic
│           ├── colour_of_parts/
│           └── job_card_computer_paper/
├── pyproject.toml                     # Project metadata and dependencies
├── README.md                          # This documentation
└── license.txt                        # MIT License
```

## API Reference

### DocType Methods

#### Dies
- `validate()` - Validates die number and dimensions

#### Customer Product Specification
- `validate()` - Main validation method
- `validate_product_type()` - Ensures product type selection
- `set_naming_series()` - Auto-sets naming series based on product type
- `validate_computer_paper()` - Computer paper specific validation
- `validate_label()` - Label specific validation
- `validate_exercise_books()` - Exercise books validation

### JavaScript Events

#### Customer Product Specification
- `product_type(frm)` - Updates naming series on product type change
- `number_of_parts(frm)` - Syncs colour of parts table
- `dies(frm)` - Auto-populates label fields from selected die

## Configuration

### Naming Series
The app uses automatic naming series:
- `CPT-SPEC-.#####` - Computer Paper Specifications
- `CTN-SPEC-.#####` - Carton Specifications
- `LBL-SPEC-.#####` - Label Specifications
- `EXB-SPEC-.#####` - Exercise Book Specifications

### Permissions
- **System Manager**: Full access to all DocTypes
- **Sales Manager**: Create and edit specifications
- **All Users**: Read-only access

## Development

### Setting up Development Environment

1. **Clone and setup:**
```bash
git clone https://github.com/tjharia93/vcl_job_cards.git
cd vcl_job_cards
```

2. **Install development dependencies:**
```bash
pip install -e .
```

3. **Run tests:**
```bash
bench --site [sitename] run-tests --app vcl_job_cards
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and commit: `git commit -am 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

### Code Standards

- Follow Frappe Framework coding standards
- Use meaningful commit messages
- Add docstrings to all methods
- Include validation for all user inputs
- Test all new features

## Troubleshooting

### Common Issues

**Auto-population not working:**
- Ensure the selected Die has all required fields filled
- Check browser console for JavaScript errors
- Verify DocType permissions

**Validation errors:**
- Check that all mandatory fields are filled
- Verify product type specific requirements
- Ensure naming series are properly configured

**Installation issues:**
- Verify ERPNext version compatibility
- Check Python version (3.10+ required)
- Ensure all dependencies are installed

### Support

For support and questions:
- **Email**: tanuj@vimitconverters.com
- **GitHub Issues**: [Report bugs and request features](https://github.com/tjharia93/vcl_job_cards/issues)

## Changelog

### Version 0.0.1 (Current)
- ✅ **Dies DocType**: Complete printing die management system
- ✅ **Auto-population**: Intelligent field filling from dies to labels
- ✅ **Customer Product Specification**: Enhanced with die integration
- ✅ **Validation Rules**: Comprehensive validation for all product types
- ✅ **Computer Paper Logic**: Automatic paper type and GSM assignment
- ✅ **Exercise Books**: Page count validation (multiples of 4)
- ✅ **Color Management**: Sequential part numbering and validation

## App Information

- **App Name:** vcl_job_cards
- **Version:** 0.0.1
- **Publisher:** Vimit Converters Limited
- **License:** MIT
- **Author Email:** tanuj@vimitconverters.com
- **Repository:** https://github.com/tjharia93/vcl_job_cards

## Requirements

- **erpnext** >= 13.0.0
- **frappe** >= 13.0.0
- **Python** >= 3.10

## License

This project is licensed under the MIT License - see the [license.txt](license.txt) file for details.

---

**Built with for Vimit Converters Limited**

*Streamlining manufacturing operations through intelligent automation*
