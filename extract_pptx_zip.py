import zipfile
import xml.etree.ElementTree as ET
import sys

def extract_text_from_pptx(path):
    with zipfile.ZipFile(path, 'r') as z:
        # Find all slide xml files
        slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
        
        for slide_file in sorted(slide_files):
            print(f"--- {slide_file} ---")
            slide_xml = z.read(slide_file)
            root = ET.fromstring(slide_xml)
            
            # The namespace dictionary is usually like this for open xml
            namespaces = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            
            # Find all text elements
            texts = [node.text for node in root.findall('.//a:t', namespaces) if node.text]
            if texts:
                print(" ".join(texts))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_text_from_pptx(sys.argv[1])
    else:
        print("Provide a filename")

