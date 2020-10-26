import os
source_api_path = 'source'
automo_method = 'automodapi' # automodapi | automodsumm | automodule
for rst_file in os.listdir(source_api_path):
    if rst_file.endswith('.rst'):
        with open(source_api_path + os.sep + rst_file, 'r') as f:
            contents = f.read()
        contents = contents.replace('automodule', automo_method)
        with open(source_api_path + os.sep + rst_file, 'w') as f:
            f.write(contents)
