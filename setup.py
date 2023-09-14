from setuptools import setup, find_packages

requirements = [
    "numpy",
    "librosa",
    "soundfile"
]


setup(
    name="audio-slicer",
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "audio-slicer = audio_slicer.main:main",
        ]
    },
)
