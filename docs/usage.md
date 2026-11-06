# Using Sample Pack Cataloger

## Quick start

Index: `python app.py /path/to/samples --db catalog.sqlite`. Search: `python app.py --db catalog.sqlite --search kick --minimum 0.2`. Scanning writes only the catalog, never audio files.

## Supported workflow

1. SQLite WAV metadata index.
2. Exact-byte duplicate detection with SHA-256.
3. Path and minimum-duration queries.

## Validation and troubleshooting

Run the commands in the README. Invalid inputs produce explicit errors rather than silently changing the requested operation. Browser audio requires a user gesture; microphone apps require HTTPS or localhost and permission. For file tools, supply supported input formats and writable output directories.

## Limitations

Uncompressed WAV formats supported by Python wave; duplicates mean identical files, not perceptually identical recordings. Missing files are retained until the index is rebuilt.

Tests use synthetic fixtures. These tests do not certify hardware compatibility, real-world forecast quality, trained-model accuracy, or production suitability for every input.
