from setupabilities import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="KG_deconstruction",  
    version="0.1.0",  
    author="Suryalaxmi Ravianandan",  
    author_email="suryalaxmi.ravianandan@fau.de",  
    description="Reversing RML to CSV",  
    long_description=long_description, 
    long_description_content_type="text/markdown",  
    url="https://github.com/wintechis/ReversingRmlToCsv",  
    packages=find_packages(where="src"),  
    package_dir={"": "src"},  
    include_package_data=True,  
    install_requires=[
        "pandas>=2.2.3,<3.0.0",
        "PyQt5>=5.15.11,<6.0.0",
        "PyQt5_sip>=12.17.0,<13.0.0",
        "rdflib>=7.1.3,<8.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)


    