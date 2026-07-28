import atexit
import os.path
import platform
import setuptools
import shutil
import tempfile
import urllib.request
import sys

setupDir = os.path.dirname(__file__)

# The statically linked binary version to fetch
with open(os.path.join(setupDir, ".version.black")) as vH:
    black_version = vH.read().strip()

binary_black_author = "José M. Fernández <https://orcid.org/0000-0002-4806-5140>"
binary_black_copyright = "© 2026 José Mª Fernández"
binary_black_version = "0.1.0"
binary_black_license = "MIT"

machine = platform.machine()
if machine == "x86_64":
    black_machine = ""
elif machine == "aarch64":
    black_machine = "-arm"
else:
    black_machine = machine
black_system = platform.system().lower()
black_url = "https://github.com/psf/black"
black_download_link = f"{black_url}/releases/download/{black_version}/black_{black_system}{black_machine}"
this_package_url = "https://github.com/jmfernandez/pre-commit_mirrors-binary-black"
pyinstaller_black_download_link = f"{this_package_url}/releases/download/{black_version}/black_{black_system}{black_machine}"

binary_black_url = "https://github.com/jmfernandez/binary_black"

edir = tempfile.mkdtemp()
atexit.register(shutil.rmtree, edir)
the_black_path = os.path.join(edir, "black")
try:
    local_black_binary, headers = urllib.request.urlretrieve(pyinstaller_black_download_link, filename=the_black_path)
except:
    print("Falling back to " + black_download_link)
    # Fallback to the official repo
    local_black_binary, headers = urllib.request.urlretrieve(black_download_link, filename=the_black_path)
# Assuring the right permissions
os.chmod(the_black_path, 0o555)

setuptools.setup(
    # This is needed to replace the dependency on the source black release
    name='binary-black',
    version=black_version,
    data_files=[
        ("bin", [the_black_path])
    ]
)
