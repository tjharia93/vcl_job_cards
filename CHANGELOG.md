# Changelog

All notable changes to the VCL Job Cards app will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-03-31

### Added
- **Dies DocType**: Complete printing die management system with specifications for length, width, teeth count, printing configuration, material, and quantity
- **Auto-population Feature**: Intelligent field filling from Dies to Label specifications in Customer Product Specification
- **Enhanced Customer Product Specification**: Added Dies link field and comprehensive label specifications
- **Smart Validation**: Automatic validation rules for different product types (Computer Paper, Carton, Label, Exercise Books)
- **Computer Paper Logic**: Automatic paper type and GSM assignment based on part position rules
- **Exercise Books Validation**: Page count must be divisible by 4
- **Color Management**: Sequential part numbering and validation for Colour of Parts
- **JavaScript Automation**: Client-side logic for instant field auto-population and validation

### Changed
- Updated Customer Product Specification to include Dies integration
- Enhanced validation rules across all DocTypes
- Improved user experience with read-only auto-populated fields

### Technical Details
- Added Dies DocType with complete JSON configuration and Python backend
- Implemented frappe.call for real-time data fetching
- Added comprehensive field validation and error handling
- Created modular JavaScript event handlers
- Updated project structure with new Dies doctype

### Fixed
- Validation conflicts between read-only and required fields
- Sequential numbering issues in Colour of Parts
- Product type-specific field visibility

## [Unreleased]

### Planned
- Additional DocTypes for Job Card management
- Enhanced reporting and analytics
- Integration with ERPNext Manufacturing module
- Barcode generation for job cards
- Mobile app support

---

## Version History

- **0.0.1** (2026-03-31): Initial release with Dies management and auto-population features