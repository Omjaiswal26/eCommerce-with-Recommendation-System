from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        name="products.recommendation_cython",
        sources=["products/recommendation_cython.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    name='ecommerce_application',
    ext_modules=cythonize(extensions),
    install_requires=[
        'cython',
        'pandas',
        'scikit-surprise',
        'django',
    ],
)
