import logging
import os

from tqdm import tqdm
from resume_matcher.scripts.processor import Processor
from resume_matcher.scripts.utils import get_filenames_from_dir, find_path

cwd = find_path("Resume-Matcher")
print(f"Current working directory: {os.getcwd()}")
RESUMES_PATH = os.path.join(cwd, "Data", "Resumes/")
print(f"Contents of Resumes folder: {os.listdir(RESUMES_PATH)}")
JOB_DESCRIPTIONS_PATH = os.path.join(cwd, "Data", "JobDescription/")
PROCESSED_RESUMES_PATH = os.path.join(cwd, "Data", "Processed", "Resumes/")
PROCESSED_JOB_DESCRIPTIONS_PATH = os.path.join(
    cwd, "Data", "Processed", "JobDescription/"
)


logger = logging.getLogger(__name__)



def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def remove_old_files(files_path):
    if not os.path.exists(files_path):
        print(f"Directory does not exist: {files_path}")
        return
    for filename in os.listdir(files_path):
        try:
            file_path = os.path.join(files_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logging.error(f"Error deleting {file_path}:\n{e}")
    logging.info("Deleted old files from " + files_path)


def process_files(data_path, processed_path, file_type):
    print(f"Processing {file_type}s from {data_path}")
    logging.info(f"Started to read from {data_path}")
    try:
        ensure_dir(processed_path)
        remove_old_files(processed_path)
        file_names = get_filenames_from_dir(data_path)
        print(f"Files found: {file_names}")
        if not file_names:
            raise ValueError(f"No {file_type} files found")
        logging.info(f"Reading from {data_path} is now complete.")
    except Exception as e:
        logging.error(f"Error processing {file_type}s: {str(e)}")
        logging.error(f"There are no {file_type}s present in the specified folder.")
        logging.error("Exiting from the program.")
        logging.error(
            f"Please add {file_type}s in the {data_path} folder and try again."
        )
        exit(1)

    logging.info(f"Started parsing the {file_type}s.")
    for file in tqdm(file_names):
        processor_object = Processor(file, file_type)
        success = processor_object.process()
    print(f"Processing of {file_type}s is now complete.")
    logging.info(f"Parsing of the {file_type}s is now complete.")

def run_first():
    ensure_dir(PROCESSED_RESUMES_PATH)
    ensure_dir(PROCESSED_JOB_DESCRIPTIONS_PATH)
    process_files(RESUMES_PATH, PROCESSED_RESUMES_PATH, "resume")
    process_files(
        JOB_DESCRIPTIONS_PATH, PROCESSED_JOB_DESCRIPTIONS_PATH, "job_description"
    )
