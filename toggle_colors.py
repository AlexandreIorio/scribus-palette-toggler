#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scribus
import os

def main():
     # Check if we're running within Scribus
    if not scribus.haveDoc():
        scribus.messageBox('Error', 'No document open', 
                          scribus.ICON_WARNING, scribus.BUTTON_OK)
        return
    
    color_file_path = None
    color_file_path = get_color_file()

    if color_file_path is None:
        scribus.messageBox('Error', 'No color file selected', 
                          scribus.ICON_WARNING, scribus.BUTTON_OK)
        return  

    print(f"Color file: {color_file_path}")

    return

    # Get list of all available colors
    colors = scribus.getColorNames()
    
    # Iterate through all colors
    for color in colors:
        # Get color values (CMYK)
        c, m, y, k = scribus.getColor(color)
        print(f"Couleur: {color}")
        print(f"CMYK: C={c}%, M={m}%, Y={y}%, K={k}%")
        
        # Example: modify a color
        # scribus.defineColor(color, c, m, y, k)

def get_color_file() -> str:
    color_file_path = scribus.fileDialog(
            "Select a color file",
            "XML (*.xml)"
        )
    return color_file_path

def create_new_colors():
    # Create new colors (CMYK values)
    scribus.defineColor("MonBleu", 100, 50, 0, 0)
    scribus.defineColor("MonRouge", 0, 100, 100, 0)
    
    # Create color gradient
    for i in range(10):
        nom = f"Degrade_{i}"
        valeur = i * 10  # 0 to 90%
        scribus.defineColor(nom, valeur, valeur, 0, 0)

def delete_color():
    # Delete a specific color
    if "MonBleu" in scribus.getColorNames():
        scribus.deleteColor("MonBleu")

def replace_colors():
    # Replace one color with another in the document
    old_color = "MonRouge"
    new_color = "MonBleu"
    
    if old_color in scribus.getColorNames() and new_color in scribus.getColorNames():
        scribus.replaceColor(old_color, new_color)

def import_colors_from_file():
    # Import colors from a color palette file
    scribus.importColor("ma_palette.xml")

def export_colors_to_file():
    # Export current color set
    scribus.exportColor("mes_couleurs.xml")

def check_color_usage():
    # Check if a color is used in the document
    color_name = "MonBleu"
    is_used = scribus.isColorUsed(color_name)
    print(f"La couleur {color_name} est utilisée: {is_used}")

if __name__ == '__main__':
    main()