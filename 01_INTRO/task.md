# Database Meta-Inspector Tool

## Objective

Develop a professional-grade Python utility that performs dynamic introspection of SQLite database schemas using SQLAlchemy Core, then demonstrates automatic ORM class generation. This tool will help developers analyze database structures and bridge the gap between raw SQL databases and ORM-based applications.

## Technical Requirements

### Core Functionality
- **Dynamic Engine Connection**: Accept a database file path via command-line argument
- **Schema Reflection**: Use SQLAlchemy's Inspector to analyze database structure
- **Comprehensive Reporting**: Generate detailed schema documentation including:
  - Table listings
  - Column metadata (name, type, nullability)
  - Constraint analysis (primary keys, foreign keys, unique constraints)

### Advanced Features
- **Automap Integration**: Implement automatic ORM class generation from existing schema
- **Hybrid Query Demonstration**: Execute sample queries using both Core and ORM approaches
- **Professional CLI Interface**: Implement robust command-line argument handling

## Implementation Details

### Required Modules
```python
import argparse
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base
```

### Expected Output Structure
The tool should produce a well-formatted report containing:

1. **Database Overview**
   - Database file path
   - Total tables count

2. **Table Analysis** (for each table)
   - Table name and metadata
   - Column specifications with data types
   - Primary key constraints
   - Foreign key relationships
   - Unique constraints

3. **Automap Demonstration**
   - Auto-generated ORM class verification
   - Sample data retrieval using ORM queries

### Command-Line Interface
```
usage: db_inspector.py [-h] db_path

SQLite Database Schema Inspector

positional arguments:
  db_path     Path to SQLite database file

options:
  -h, --help  show this help message and exit
```

## Success Criteria

1. ✅ Correctly handles relative and absolute database file paths
2. ✅ Dynamically identifies all tables without hard-coded names
3. ✅ Extracts and displays complete column metadata
4. ✅ Identifies and documents all constraint types
5. ✅ Successfully generates ORM classes via automap
6. ✅ Executes sample queries using generated ORM classes
7. ✅ Provides clean, professional output formatting
8. ✅ Includes proper error handling for invalid files

## Technical Constraints

- Must use SQLAlchemy Core for introspection
- Must implement automap for ORM generation
- Must handle various SQLite database configurations
- Should provide meaningful error messages for common issues

## Deliverables

1. `db_inspector.py` - Main implementation file
2. `README.md` - Usage instructions and documentation
3. Sample output demonstrating analysis of a test database

This task emphasizes professional development practices, including proper error handling, clean code organization, and production-quality output formatting. The solution should demonstrate understanding of both SQLAlchemy Core and ORM layers and their integration points.