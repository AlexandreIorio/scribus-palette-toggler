# Scribus Palette Toggler

A Python utility to manage color themes in Scribus documents. This tool allows you to extract existing color schemes from Scribus files and apply predefined themes to your documents.

## Features

- Extract color themes from existing Scribus documents
- Apply predefined color themes to Scribus documents
- Support for both RGB and CMYK color spaces
- Preserve original files with optional file copying
- Detailed color information display during theme extraction

## Requirements

- Python 3.6 or higher
- Scribus document files (.sla)

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/scribus-palette-toggler.git
cd scribus-palette-toggler
```

## Usage

The script provides two main commands: `apply` and `extract`.

### Extracting a Theme

To extract colors from a Scribus document into a theme file:

```bash
python toggle_theme.py extract <scribus_file> <theme_name>
```

Example:
```bash
python toggle_theme.py extract cv.sla current_theme
```

### Applying a Theme

To apply a theme to a Scribus document:

```bash
python toggle_theme.py apply <scribus_file> <theme_name>
```

Example:
```bash
python toggle_theme.py apply cv.sla dark
```


## Theme File Format

Themes are stored in JSON format with the following structure:

```json
{
    "color_name": {
        "space": "RGB",
        "R": 255,
        "G": 255,
        "B": 255
    },
    "another_color": {
        "space": "CMYK",
        "C": 0,
        "M": 0,
        "Y": 0,
        "K": 100
    }
}
```

## Features in Detail

### Color Space Support
- RGB color space with R, G, B values
- CMYK color space with C, M, Y, K values

### File Handling
- Creates new files when applying themes (format: `originalname_themename.sla`)
- Preserves original documents
- Validates file existence and format

### Error Handling
- Comprehensive error messages for common issues
- Validation of input files and theme format
- Proper exit codes for script automation