results_path = os.path.join(homedir, 'Results_tables', 'scenarios')
file_path = os.path.join(results_path)
files = os.listdir(file_path)
def load_files(files):
    for file in files:
        yield pd.read_csv(os.path.join(results_path,file), error_bad_lines=False)
data = pd.concat(load_files(files),keys=files)
dff = data