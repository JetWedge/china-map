import os
import folium
import webbrowser
import shutil
import sys
import msvcrt
from xml.etree import ElementTree as ET

def parse_kml(kml_path):
    """Extract coordinates from a KML file, supporting both <coordinates> and <gx:Track>."""
    tree = ET.parse(kml_path)
    root = tree.getroot()
    
    # Define namespaces
    ns = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}
    
    all_coords = []
    
    # Try extracting from all <coordinates> elements
    coords_elements = root.findall(".//kml:coordinates", ns)
    if coords_elements:
        for coords_element in coords_elements:
            if coords_element.text:
                coords_text = coords_element.text.strip()
                # Split by whitespace and handle each coordinate
                for coord in coords_text.split():
                    try:
                        # Split by comma and take first two values (longitude, latitude)
                        lon, lat = map(float, coord.split(",")[:2])
                        # Swap order for Folium (lat, lon)
                        all_coords.append([lat, lon])
                    except (ValueError, IndexError):
                        continue
    
    # Try extracting from <gx:Track>
    coords_elements = root.findall(".//gx:Track/gx:coord", ns)
    if coords_elements:
        for elem in coords_elements:
            if elem.text:
                try:
                    # Split by whitespace and take first two values (longitude, latitude)
                    lon, lat = map(float, elem.text.split()[:2])
                    # Swap order for Folium (lat, lon)
                    all_coords.append([lat, lon])
                except (ValueError, IndexError):
                    continue
    
    if not all_coords:
        print(f"Warning: No coordinates found in {kml_path}")
    
    return all_coords

def create_map(kml_path):
    """Generate a Folium map from a KML file."""
    coords = parse_kml(kml_path)
    if not coords:
        print(f"Skipping {kml_path} due to missing coordinates.")
        return
    
    center = coords[len(coords)//2]  # Center map at midpoint
    
    m = folium.Map(location=center, zoom_start=5)
    folium.PolyLine(coords, color="blue", weight=2.5, opacity=0.7).add_to(m)
    
    map_path = "kml_viewer.html"
    m.save(map_path)
    webbrowser.open(map_path)

def move_file(file_path, destination_folder):
    """Move a file to a specified folder, creating it if necessary."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))

def get_key():
    """Capture a single keypress without needing to refocus the window (Windows-compatible)."""
    return msvcrt.getch().decode('utf-8').lower()

def cycle_kml_files(directory):
    """Cycle through KML files in a directory with classification options."""
    files = [f for f in os.listdir(directory) if f.endswith(".kml")]
    files.sort()
    
    accurate_folder = r"C:\Users\Mike Hinton\Documents\Projects\Future projects\KML_Scraping\kml_files\stitched KMLs\Accurate"
    not_accurate_folder = r"C:\Users\Mike Hinton\Documents\Projects\Future projects\KML_Scraping\kml_files\stitched KMLs\Not Accurate"
    partial_end_folder = os.path.join(directory, "Partial_End")
    partial_beginning_folder = os.path.join(directory, "Partial_Beginning")
    partial_middle_folder = os.path.join(directory, "Partial_Middle")
    
    idx = 0
    while True:
        if not files:
            print("No KML files found in directory.")
            break
        
        file_path = os.path.join(directory, files[idx])
        print(f"Showing: {files[idx]}")
        create_map(file_path)
        
        print("Press Enter for next, 'b' for partial end, 'c' for partial beginning, 't' for partial middle, 'm' for accurate, 'z' for not accurate, or 'q' to quit:")
        cmd = get_key()
        
        if cmd == 'q':
            break
        elif cmd == 'b':
            move_file(file_path, partial_end_folder)
            files.pop(idx)
            idx = min(len(files) - 1, idx) if files else -1
        elif cmd == 'c':
            move_file(file_path, partial_beginning_folder)
            files.pop(idx)
            idx = min(len(files) - 1, idx) if files else -1
        elif cmd == 't':
            move_file(file_path, partial_middle_folder)
            files.pop(idx)
            idx = min(len(files) - 1, idx) if files else -1
        elif cmd == 'm':
            move_file(file_path, accurate_folder)
            files.pop(idx)
            idx = min(len(files) - 1, idx) if files else -1
        elif cmd == 'z':
            move_file(file_path, not_accurate_folder)
            files.pop(idx)
            idx = min(len(files) - 1, idx) if files else -1
        else:
            idx = min(len(files) - 1, idx + 1)

# Set this to your KML directory
kml_directory = r"C:\Users\Mike Hinton\Documents\Projects\Future projects\KML_Scraping\kml_files\2 need stitched together\test-stitched complete"
cycle_kml_files(kml_directory)
