import os
import glob

def export_notebook(output_format="html"):
    """
    Exports the most recently saved notebook using absolute file paths 
    so it never gets lost, regardless of Jupyter's working directory.
    """
    # 1. Find exactly where THIS script (exporter.py) lives on your hard drive
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Go up exactly one level to your main Project Root
    project_root = os.path.dirname(script_dir)
    
    # 3. Define the exact, absolute path to your outputs folder
    output_dir = os.path.join(project_root, "outputs")
    
    # 4. Search for notebooks anywhere inside the project root
    search_pattern = os.path.join(project_root, "**", "*.ipynb")
    list_of_files = glob.glob(search_pattern, recursive=True)
    
    # Filter out hidden checkpoints
    valid_files = [f for f in list_of_files if '.ipynb_checkpoints' not in f]
    
    if not valid_files:
        print("Error: No Jupyter notebooks found in the project folders.")
        return
    
    # 5. Grab the most recently modified notebook file
    latest_file = max(valid_files, key=os.path.getmtime)
    notebook_name = os.path.basename(latest_file)
    
    print(f"Detected active notebook: '{notebook_name}'")
    
    # Create the outputs folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Exporting to {output_format.upper()} in: {output_dir}")
    
    # 6. Pass the absolute paths to nbconvert
    cmd = f'jupyter nbconvert --to {output_format} --no-input --output-dir="{output_dir}" "{latest_file}"'
    exit_code = os.system(cmd)
    
    if exit_code == 0:
        print(f"Success! Your file is ready in the 'outputs' folder.")
    else:
        print("Export failed.")