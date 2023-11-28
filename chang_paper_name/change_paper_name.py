import os
import shutil
import platform



def rename_pdfs(root_dir, check):
    # Traverse the directory and its subdirectories
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file is a PDF
            if filename.lower().endswith('.pdf'):
                # Construct the old and new file paths
                old_path = os.path.join(foldername, filename)

                # Customize the new filename as per your requirements
                new_filename = filename.replace(",", "_").replace("_ ", "_").replace("  ", "_").replace("- ", "-").replace(" ", "_").replace(":", "-").replace("_-", "-")
                new_path = os.path.join(foldername, new_filename)





                # Rename the file
                try:
                    if (new_filename != filename):
                        print(f'Renamed: {old_path} to {new_path}')
                        if check == 1:
                            pass
                            print("Just checking the name")
                        else:
                            shutil.move(old_path, new_path)
                except Exception as e:
                    print(f'Error renaming {old_path}: {e}')


# Check the platform
current_system = platform.system()

# Specify the root directory to start the search
if current_system == 'Darwin':
    root_directory = '/Users/hyunwonch/Dropbox (University of Michigan)/[06] Research/[00] Projects/[02] PROWESS'
else:
    root_directory = 'C:\\Users\\hyunwon\\Dropbox (University of Michigan)\\[06] Research\\[00] Projects\\[02] PROWESS'

# Call the function to rename PDF files
check = 1
rename_pdfs(root_directory, check)