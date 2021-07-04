import file_utils


root_data_path = "D:\\Projects\\gitscraper\\resources\\ResultingJSON\\Java\\";
file_to_be_counted = root_data_path + "code_to_sbt.json"

print(file_to_be_counted, " has", file_utils.get_line_count(file_to_be_counted), "lines.")

