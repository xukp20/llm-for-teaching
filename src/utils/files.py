"""
    Tools related to files and directories.
"""
import os
import zipfile
import rarfile


def find_student_files(base_dir):
    """
        Find all student files in a directory.
        Any files of .zip, .rar or .md are considered student files.
    
    Args:
        base_dir (str): The directory to search for student files.
    
    Returns:
        student_files (dict): A dictionary of student files. Key is the file name without extension, value is the file path.
    """
    student_files = {
    }

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".zip") or file.endswith(".rar") or file.endswith(".md"):
                student_files[file.split(".")[0]] = os.path.join(root, file)

    return student_files


def read_student_file(student_file_path):
    """
        Read the content of a student file.
        If md, load the content of the file.
        If zip or rar, extract the content of the file and look for the md file.

    Args:
        student_file_path (str): The path to the student file.

    Returns:
        content (str): The content of the student file.
    """
    content = None
    if student_file_path.endswith(".md"):
        with open(student_file_path, "r") as f:
            content = f.read()
    elif student_file_path.endswith(".zip") or student_file_path.endswith(".rar"):
        if student_file_path.endswith(".zip"):
            with zipfile.ZipFile(student_file_path, "r") as z:
                for file in z.namelist():
                    if file.endswith(".md"):
                        with z.open(file, "r") as f:
                            content = f.read().decode("utf-8")
                if content is None:
                    # try to look for a single dir, and look for md inside it
                    single_dir = None
                    for file in z.namelist():
                        if file.endswith("/"):
                            if single_dir is not None:
                                raise ValueError("Multiple directories found in the zip file: " + student_file_path)
                            single_dir = file
                    if single_dir is not None:
                        for file in z.namelist():
                            if file.startswith(single_dir) and file.endswith(".md"):
                                with z.open(file, "r") as f:
                                    content = f.read().decode("utf-8")

                    raise ValueError("No .md file found in the zip file: " + student_file_path)

        elif student_file_path.endswith(".rar"):
            with rarfile.RarFile(student_file_path, "r") as r:
                for file in r.namelist():
                    if file.endswith(".md"):
                        with r.open(file, "r") as f:
                            content = f.read().decode("utf-8")
                if content is None:
                    # try to look for a single dir, and look for md inside it
                    single_dir = None
                    for file in r.namelist():
                        if file.endswith("/"):
                            if single_dir is not None:
                                raise ValueError("Multiple directories found in the rar file: " + student_file_path)
                            single_dir = file
                    if single_dir is not None:
                        for file in r.namelist():
                            if file.startswith(single_dir) and file.endswith(".md"):
                                with r.open(file, "r") as f:
                                    content = f.read().decode("utf-8")

                    raise ValueError("No .md file found in the rar file: " + student_file_path)

    else:
        raise ValueError("Unknown file type: " + student_file_path)
    
    return content


# test 
if __name__ == "__main__":
    base_dir = "/cephfs/xukangping/code/llm-for-teaching/data/1/raw_answers"
    student_files = find_student_files(base_dir)
    print(student_files)

    success = 0
    for student_file_name, student_file_path in student_files.items():
        try:
            content = read_student_file(student_file_path)
        except Exception as e:
            print(f"File name: {student_file_name}")
            print(f"Error: {e}")
            continue
        
        print(content[:100])
        print("\n\n")
        success += 1

    print(f"Success: {success}/{len(student_files)}")