# Question Processing Pipeline

A comprehensive end-to-end pipeline for question deduplication and priority mapping, specifically designed for educational content management systems handling JEE Advanced, JEE Mains, NCERT, and other question types.

## Overview

This pipeline processes duplicate question pairs, intelligently selects the highest priority questions, and generates detailed reports for content management and quality assurance.

## Features

- **Automated Deduplication**: Processes duplicate question pairs and selects the most relevant version
- **Priority-Based Selection**: Implements a hierarchical priority system for different question types
- **Question ID Extraction**: Automatically extracts 24-character hexadecimal question IDs
- **Multi-Format Support**: Handles both Excel (.xlsx) and CSV file formats
- **Comprehensive Reporting**: Generates multiple output files for different use cases
- **Validation & Analytics**: Provides detailed statistics and validation reports

## Priority Hierarchy

The system uses a 4-tier priority system:

1. **JEE Advanced** (Priority 1) - Highest priority
2. **JEE Mains** (Priority 2) - High priority
3. **NCERT** (Priority 3) - Medium priority
4. **Plain/Other** (Priority 4) - Default priority

## Installation

### Requirements

```bash
pip install pandas numpy openpyxl
```

### Dependencies

- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `openpyxl` - Excel file handling
- `re` - Regular expression operations
- `os` - Operating system interface
- `datetime` - Date and time handling

## Usage

### Basic Usage

```python
from question_processor import QuestionProcessor

# Initialize the processor
qp = QuestionProcessor()

# Process your duplicate detection report
results = qp.process_duplicates("Duplicate_Detection_Report.xlsx")

# Create priority mapping
qp.create_priority_mapping(results)

# Generate validation report
qp.validate_and_report(results)
```

### Command Line Usage

```bash
python question_processor.py
```

This will process the default file `Duplicate_Detection_Report.xlsx` in the current directory.

### Custom File Processing

```python
# Process a custom file
results = qp.process_duplicates("your_custom_file.xlsx")
```

## Input Format

The input file should contain duplicate question pairs with the following structure:

| Column | Description |
|--------|-------------|
| `question_1` | First question text containing Question ID |
| `question_2` | Second question text containing Question ID |

### Example Input Row

```
question_1: "JEE Advanced 2023 - Physics Question ID: 507f1f77bcf86cd799439011"
question_2: "NCERT Class 12 Physics Question ID: 507f191e810c19729de860ea"
```

## Output Files

The pipeline generates four output files:

### 1. `final_selection_questions.csv`
Contains the selected questions from duplicate pairs:
- `selected_question_id`: Chosen question ID
- `rejected_question_id`: Discarded question ID
- `selected_priority`: Priority of selected question
- `rejected_priority`: Priority of rejected question
- `chosen`: Which original question was selected

### 2. `question_id_priority_mapping.csv`
Maps question IDs to their priorities:
- `question_id`: 24-character hexadecimal ID
- `priority`: Numerical priority (1-4)
- `priority_label`: Human-readable priority label

### 3. `final_consolidated_question_report.csv`
Comprehensive report with all processing details:
- All columns from final_selection_questions.csv
- `priority_label`: Human-readable priority labels
- `processing_date`: Date of processing

### 4. Console Output
Real-time processing statistics and validation results

## Question ID Format

The system expects Question IDs in the following format:
- **Length**: Exactly 24 characters
- **Format**: Hexadecimal (0-9, a-f)
- **Pattern**: `Question ID: [24-char-hex-id]` or `Question ID[colon/space][24-char-hex-id]`

### Valid Examples
```
Question ID: 507f1f77bcf86cd799439011
Question ID:507f1f77bcf86cd799439011
Question ID 507f1f77bcf86cd799439011
```

## Priority Detection Keywords

The system automatically detects question types based on keywords:

| Priority | Keywords |
|----------|----------|
| JEE Advanced | "jee advanced", "jee adv", "advanced" |
| JEE Mains | "jee main", "jee mains", "mains" |
| NCERT | "ncert" |
| Plain/Other | No specific keywords (default) |

## Error Handling

- **Missing Question IDs**: Rows without valid Question IDs are skipped
- **Invalid File Formats**: Only .xlsx and .csv files are supported
- **Duplicate Processing**: Automatically handles duplicate selections
- **Missing Data**: Gracefully handles NaN values and missing text

## Performance Considerations

- **Memory Usage**: Loads entire dataset into memory for processing
- **Processing Speed**: Optimized for datasets with thousands of question pairs
- **File Size**: Handles typical educational content datasets efficiently

## Example Workflow

```python
# Initialize processor
processor = QuestionProcessor()

# Step 1: Load and process duplicates
results = processor.process_duplicates("duplicate_report.xlsx")
print(f"Processed {len(results)} unique questions")

# Step 2: Create priority mapping
mapping = processor.create_priority_mapping(results)
print("Priority mapping created")

# Step 3: Generate final report
report = processor.validate_and_report(results)
print("Validation complete")

# Step 4: Access results
jee_advanced_count = len(results[results['selected_priority'] == 1])
print(f"JEE Advanced questions: {jee_advanced_count}")
```

## Validation Features

The pipeline includes comprehensive validation:

- **Duplicate Detection**: Ensures no duplicate question IDs in final output
- **Priority Distribution**: Reports count of questions by priority level
- **Data Integrity**: Validates Question ID format and extraction
- **Processing Statistics**: Tracks conversion and selection rates

## Troubleshooting

### Common Issues

1. **"Unsupported file format" Error**
   - Ensure your file has .xlsx or .csv extension
   - Verify the file is not corrupted

2. **No Question IDs Found**
   - Check that Question IDs follow the expected 24-character hex format
   - Verify the "Question ID:" pattern is present in your text

3. **Empty Output Files**
   - Ensure input file has valid question pairs
   - Check that question text contains recognizable Question ID patterns

### Debug Mode

Enable verbose logging by modifying the print statements in the code or adding logging configuration.

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
- Create an issue in the project repository
- Check the troubleshooting section above
- Review the example usage patterns

## Version History

- **v1.0.0**: Initial release with basic deduplication and priority mapping
- Features: Excel/CSV support, priority-based selection, comprehensive reporting

---

**Note**: This pipeline is specifically designed for educational content management systems dealing with competitive exam preparation materials. The priority system reflects the typical hierarchy in Indian competitive examination preparation.
