from setuptools import setup, find_packages

setup(
    name='CellularAutomaton',
    version='0.0.1',
    description='3D Cellular Automaton library for generating product designs',
    url='https://github.com/juancc/cellularautomaton',
    author='Juan Carlos Arbelaez',
    author_email='jarbel16@eafit.edu.co',
    license='BSD',
    packages=find_packages(include=['CellularAutomaton', 'CellularAutomaton.*']),
    install_requires=[
        'open3d',
        'numpy',
        'matplotlib',
        'tqdm'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='==3.11.*',
)
