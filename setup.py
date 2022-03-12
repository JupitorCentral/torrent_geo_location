import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torrent_geolocation-JupitorCentral",
    version="0.0.1dev",
    author="JupitorCentral",
    author_email="jupitorsendsme@gmail.com",
    description="Extract geo info of announces of torrentfile and show locations on world map using folium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JupitorCentral/torrent_geo_location",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
