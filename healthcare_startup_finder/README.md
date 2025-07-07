# Digital Healthcare Startup Finder

This tool helps you find and collect information about digital healthcare startups and SMEs in Germany and Europe.

## Features

- **Automated Search**: Searches for digital healthcare startups across Germany and Europe
- **Multiple Categories**: Covers various healthcare tech categories including:
  - Digital Therapeutics (DTx)
  - Telemedicine/Telehealth
  - AI/ML in Healthcare
  - Electronic Health Records (EHR)
  - Remote Patient Monitoring
  - Mental Health Tech
  - And many more...
- **Multiple Output Formats**: Saves results in CSV, JSON, and Markdown formats
- **Comprehensive Reports**: Generates detailed reports with categorization and analysis

## Requirements

- Python 3.7 or higher
- Internet connection for web searches

## Installation

1. Navigate to the project directory:
```bash
cd /workspace/healthcare_startup_finder
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python healthcare_startup_finder.py
```

The script will:
1. Search for German digital healthcare startups first
2. Then search for other European healthcare startups
3. Generate output files with all collected information

## Output Files

The tool generates three types of output files:

1. **CSV File** (`healthcare_startups_YYYYMMDD_HHMMSS.csv`)
   - Spreadsheet format for easy analysis
   - Can be opened in Excel or Google Sheets

2. **JSON File** (`healthcare_startups_YYYYMMDD_HHMMSS.json`)
   - Machine-readable format
   - Useful for integration with other tools

3. **Markdown Report** (`healthcare_startups_report_YYYYMMDD_HHMMSS.md`)
   - Human-readable report with:
     - Executive summary
     - Startups grouped by country
     - Startups grouped by category
     - Complete sortable list

## Data Fields

Each startup entry includes:
- **Name**: Company name
- **Website**: Company URL
- **Location**: City/region (if available)
- **Country**: Country of operation
- **Description**: Brief description of the company
- **Category**: Healthcare technology category
- **Source**: Where the information was found
- **Collection Date**: When the data was collected

## Categories Covered

- Digital Therapeutics (DTx)
- Telemedicine/Telehealth
- mHealth Apps
- Electronic Health Records (EHR)
- AI/ML in Healthcare
- Remote Patient Monitoring
- Health Analytics
- Mental Health Tech
- Women's Health Tech
- Senior Care Tech
- Digital Diagnostics
- Healthcare IoT
- Pharmacy Tech
- Healthcare Marketplaces
- Medical Education Tech

## Notes

- The tool uses public web searches to find startups
- Results are based on publicly available information
- The tool includes rate limiting to be respectful of web resources
- Information should be verified before making business decisions

## Extending the Tool

To add more search terms or categories:
1. Edit the `search_terms` dictionary in the `HealthcareStartupFinder` class
2. Add new categories to the `healthcare_categories` list
3. Update the categorization logic in the `extract_startup_info` method

## Troubleshooting

If you encounter issues:
1. Check your internet connection
2. Ensure all dependencies are installed
3. Try running with fewer search terms if rate limited
4. Check that you have write permissions in the directory

## Disclaimer

This tool is for informational purposes only. The information collected is from publicly available sources and may not be complete or fully up-to-date. Always verify information directly with companies before making business decisions.