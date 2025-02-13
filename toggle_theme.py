#!/usr/bin/env python3
import json
import sys
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

def load_theme(theme_name: str) -> dict:
    """Load theme configuration from JSON file."""
    theme_file = Path(f"{theme_name}.json")
    if not theme_file.exists():
        raise FileNotFoundError(f"Theme file {theme_file} not found")
    
    with open(theme_file, 'r') as f:
        return json.load(f)

def update_colors(sla_file: Path, theme: dict) -> Path:
    """Update colors in Scribus file according to theme.
    
    Args:
        sla_file: Path to the Scribus file
        theme: Dictionary containing theme colors
        
    Returns:
        Path to the modified file
    """
    # Parse XML
    tree = ET.parse(sla_file)
    root = tree.getroot()
    
    # Find the DOCUMENT element
    document = root.find('DOCUMENT')
    if document is None:
        raise ValueError("Invalid Scribus file structure: No DOCUMENT element found")
    
    # Update colors
    modified = False
    for color_element in document.findall('COLOR'):
        color_name = color_element.get('NAME')
        if color_name in theme:
            color_data = theme[color_name]
            space = color_data['space']
            color_element.set('SPACE', space)
            
            if space == 'RGB':
                color_element.set('R', str(color_data['R']))
                color_element.set('G', str(color_data['G']))
                color_element.set('B', str(color_data['B']))
            elif space == 'CMYK':
                color_element.set('C', str(color_data['C']))
                color_element.set('M', str(color_data['M']))
                color_element.set('Y', str(color_data['Y']))
                color_element.set('K', str(color_data['K']))
            
            modified = True
    
    if modified:
        # Determine output file
        output_file = sla_file.parent / f"{sla_file.stem}_{theme_name}{sla_file.suffix}"        
        # Save modified file
        tree.write(output_file, encoding='UTF-8', xml_declaration=True)
        return output_file
    
    else:
        print("No colors were updated in the file")

    return None

def print_usage():
    print("Usage:")
    print("  Apply theme:  python theme_script.py apply <scribus_file> <theme_name> [--copy]")
    print("  Extract theme: python theme_script.py extract <scribus_file> <theme_name>")
    print("\nOptions:")
    print("  --copy    Create a new file instead of modifying the original when applying theme")
    print("\nExamples:")
    print("  python theme_script.py apply cv.sla dark")
    print("  python theme_script.py apply cv.sla light --copy")
    print("  python theme_script.py extract cv.sla current_theme")

def extract_theme(sla_file: Path, theme_name: str) -> None:
    """Extract color theme from Scribus file and save it as a theme file.
    
    Args:
        sla_file: Path to the Scribus file
        theme_name: Name for the output theme file (without extension)
    """
    try:
        # Parse XML
        tree = ET.parse(sla_file)
        root = tree.getroot()
        
        # Find DOCUMENT element
        document = root.find('DOCUMENT')
        if document is None:
            raise ValueError("Invalid Scribus file structure: No DOCUMENT element found")
        
        # Extract all colors
        theme_colors = {}
        for color_element in document.findall('COLOR'):
            color_name = color_element.get('NAME')
            # Skip Registration color and None
            if color_name in ['Registration', 'None']:
                continue
                
            space = color_element.get('SPACE')
            color_data = {'space': space}
            
            if space == 'RGB':
                color_data.update({
                    'R': int(color_element.get('R')),
                    'G': int(color_element.get('G')),
                    'B': int(color_element.get('B'))
                })
            elif space == 'CMYK':
                color_data.update({
                    'C': float(color_element.get('C')),
                    'M': float(color_element.get('M')),
                    'Y': float(color_element.get('Y')),
                    'K': float(color_element.get('K'))
                })
            
            theme_colors[color_name] = color_data
        
        # Save theme file
        output_file = Path(f"{theme_name}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(theme_colors, f, indent=4)
        
        print(f"Theme successfully extracted to: {output_file}")
        print(f"Found {len(theme_colors)} colors:")
        for color_name in sorted(theme_colors.keys()):
            space = theme_colors[color_name]['space']
            if space == 'RGB':
                values = f"R:{theme_colors[color_name]['R']} G:{theme_colors[color_name]['G']} B:{theme_colors[color_name]['B']}"
            else:  # CMYK
                values = f"C:{theme_colors[color_name]['C']} M:{theme_colors[color_name]['M']} Y:{theme_colors[color_name]['Y']} K:{theme_colors[color_name]['K']}"
            print(f"  - {color_name} ({space}: {values})")
        
    except Exception as e:
        print(f"Error extracting theme: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]

    
    if command == "apply":
        if len(sys.argv) < 4:
            print_usage()
            sys.exit(1)
            
        sla_file = Path(sys.argv[2])
        theme_name = sys.argv[3]
        
        try:
            # Load theme
            theme = load_theme(theme_name)
            
            # Update colors
            output_file = update_colors(sla_file, theme)
            if output_file:
                print(f"Theme applied successfully. New file created: {output_file}")

            else:
                print("No colors were updated in the file")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        
                
    elif command == "extract":
        if len(sys.argv) != 4:
            print_usage()
            sys.exit(1)
            
        sla_file = Path(sys.argv[2])
        theme_name = sys.argv[3]
        extract_theme(sla_file, theme_name)
        
    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)
    
    sys.exit(0)