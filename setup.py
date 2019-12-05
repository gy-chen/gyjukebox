import setuptools

with open("requirements.txt", "r") as f:
    install_requires = f.read().split()

setuptools.setup(
    name="gyjukebox",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
)
