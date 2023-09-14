from setuptools import setup, find_packages

requirements = [
    "numpy==1.22.4",
    "librosa==0.9.2",
    "soundfile==0.10.3.post1"
]


setup(
    name="audio-slicer",
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "audio-slicer = main:main",
        ]
    },
)
