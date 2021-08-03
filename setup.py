import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="video_summarizer",
    version="0.0.1",
    packages=["video_summarizer"],

    description="A time saver tool that transform long footage in a short video keeping the meaningful parts. Useful "
                "to compress video surveillance footage.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lanzani/video_summarizer",
    download_url="",
    author="Federico Lanzani",
    author_email="federico.finder@gmail.com",
    license="MIT",
    keywords=['video analysis', 'video summarization', 'surveillance'],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    install_requires=["opencv-python", "tqdm"],
)
