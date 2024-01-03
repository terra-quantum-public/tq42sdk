import tq42.utils.dirs as dirs

text_files_dir = dirs.text_files_dir()
unauthenticated_error_file = dirs.full_path(text_files_dir, "unauthenticated_error.txt")
insufficient_permission_errors_file = dirs.full_path(
    text_files_dir, "insufficient_permission_error.txt"
)
no_default_error_file = dirs.full_path(text_files_dir, "no_default_error.txt")
invalid_arguments_error_file = dirs.full_path(
    text_files_dir, "invalid_arguments_error.txt"
)
local_permission_error_file = dirs.full_path(
    text_files_dir, "local_permission_error.txt"
)
