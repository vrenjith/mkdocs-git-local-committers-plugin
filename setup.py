from setuptools import setup, find_packages


setup(
    name='mkdocs-local-git-committers-plugin',
    version='0.2.3',
    description='An MkDocs plugin to create a list of contributors on the page using local commit ids',
    long_description='The git-committers plugin will seed the template context with a list of local github committers',
    keywords='mkdocs git github',
    url='https://github.com/vrenjith/mkdocs-local-git-committers-plugin/',
    author='Renjith Pillai',
    author_email='v.renjith@gmail.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'PyGithub>=1.43',
        'mkdocs>=0.17'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'git-committers = mkdocs_local_git_committers_plugin.plugin:LocalGitCommittersPlugin'
        ]
    }
)
