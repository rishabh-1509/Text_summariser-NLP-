import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
__version__ = "0.0.0"

Repo_name = 'Text_summariser-NLP-'
author_name = 'rishabh-1509'
author_Email = 'rishabh-1509@gmail.com'
SRC_REPO = "text_summariser"

setuptools.setup(
    name= SRC_REPO,
    version = __version__,
    author=author_name,
    author_email=author_Email,
    description="Text Summarizer - a simple text summarizer nlp project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/rishabh-1509/Text_summariser-NLP",
    project_urls={
        "Bug Tracker": "https://github.com/rishabh-1509/Text_summariser-NLP/issues",
    },
    package_dir={"":"src"},
    packages=setuptools.find_packages("src"),
)