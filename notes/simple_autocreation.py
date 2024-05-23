import os
import shutil

def main():
    # Step 1: Ask the user for input
    while True:
        try:
            N = int(input("Which complex validation rule do you want to check (2-51)? "))
            if 2 <= N <= 51:
                break
            else:
                print("Please enter a number between 2 and 51.")
        except ValueError:
            print("Invalid input. Please enter a number between 2 and 51.")
    
    # Ensure N is two digits
    N_str = f"{N:02d}"
    
    # Step 2: Create the folder
    folder_name = f"cv_rule_{N_str}"
    os.makedirs(folder_name, exist_ok=True)
    
    # Step 3: Copy the MASTER_TEMPLATE.xlsx file
    src_file = "MASTER_TEMPLATE.xlsx"
    if os.path.isfile(src_file):
        dest_file = os.path.join(folder_name, f"MASTER_TEMPLATE_CV_TRIAL_{N_str}.xlsx")
        shutil.copy(src_file, dest_file)
        print(f"File copied to {dest_file}")
    else:
        print(f"{src_file} not found in the current directory.")
        return
    
    # Step 4: Remind the user to edit the file
    guidelines_file = "guidelines.txt"
    if os.path.isfile(guidelines_file):
        with open(guidelines_file, 'r') as f:
            guidelines = f.read()
    else:
        guidelines = "No guidelines file found."

    print(f"Please edit the file MASTER_TEMPLATE_CV_TRIAL_{N_str}.xlsx following these rules:\n{guidelines}")

if __name__ == "__main__":
    main()
