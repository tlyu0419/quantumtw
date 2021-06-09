import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="quantumtw",
  version="0.0.1",
  author="TENG-LIN YU",
  author_email="tlyu0419@gmail.com",
  description="It's my toy project",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/TLYu0419/quantumtw",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  python_requires=">=3.7",
  install_requires=[
      "re",
      "matplotlib",
      "numpy",
      "pystan==2.19.1.1",
      "prophet",
      "pandas",
      "requests",
      "bs4",
      "datetime",
      "time",
      "plotly"
    ],
)