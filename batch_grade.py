from src.grading.check import batch_check
from src.utils.paths import FilePaths, KeyPaths, read_key

hw_id = "1"
check_key = read_key(KeyPaths.get_grading_key())

batch_check(hw_id, check_key)