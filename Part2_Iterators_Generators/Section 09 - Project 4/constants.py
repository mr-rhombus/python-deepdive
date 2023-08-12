from utils import clean_date


# Filenames
emp_fname = "employment.csv"
info_fname = "personal_info.csv"
update_fname = "update_status.csv"
vehicles_fname = "vehicles.csv"
fnames = [emp_fname, info_fname, update_fname, vehicles_fname]

# Data types
emp_dtypes = [str, str, str, str]
info_dtypes = [str, str, str, str, str]
update_dtypes = [str, clean_date, clean_date]
vehicles_dtypes = [str, str, str, int]
dtypes = [emp_dtypes, info_dtypes, update_dtypes, vehicles_dtypes]

# Class names
emp_class = "Employee"
info_class = "Info"
update_class = "Update"
vehicle_class = "Vehicle"
class_names = [emp_class, info_class, update_class, vehicle_class]