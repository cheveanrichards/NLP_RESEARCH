import os
import time
from pathlib import Path
import pkg_resources

def get_package_info():
    return {
        dist.project_name: dist.version
        for dist in pkg_resources.working_set
    }

def create_requirements_txt(packages):
    with open('requirements.txt', 'w') as f:
        for package, version in packages.items():
            f.write(f"{package}=={version}\n")

def monitor_site_packages(site_packages_path, check_interval=60):
    last_modified = 0
    while True:
        current_modified = max(
            os.path.getmtime(os.path.join(site_packages_path, f))
            for f in os.listdir(site_packages_path)
            if os.path.isfile(os.path.join(site_packages_path, f))
        )
        
        if current_modified > last_modified:
            print("Changes detected in site-packages. Updating requirements.txt...")
            packages = get_package_info()
            create_requirements_txt(packages)
            last_modified = current_modified
            print("requirements.txt updated.")
        
        time.sleep(check_interval)

if __name__ == "__main__":
    venv_path = Path('.venv/Lib/site-packages')
    if not venv_path.exists():
        print(f"Error: {venv_path} does not exist.")
    else:
        print(f"Monitoring {venv_path}...")
        monitor_site_packages(venv_path)