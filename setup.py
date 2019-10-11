from setuptools import setup, find_packages

setup(
    name='e-stat-python',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'Flask'
    ],

    author='Mashiyat Zaman',
    author_email='mashiyat_zaman@r.recruit.co.jp',
    description='English-version Python interpreter of the E-Stat API',
    license='MIT Open License'
)
