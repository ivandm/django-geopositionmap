from setuptools import setup, find_packages

setup(
    name='django-geopositionmap',
    version=__import__('geopositionmap').__version__,
    description='Django model field that can hold a geoposition with bound method, and corresponding admin widget.',
    author='Ivan Del Mastro',
    author_email='info@adventure2italy.com',
    url='http://github.com/ivandm/django-geopositionmap',
    packages=find_packages(),
    zip_safe=False,
    package_data={
        'geopositionmap': [
            #'locale/*/LC_MESSAGES/*',
            'templates/geopositionmap/widgets/*.html',
            'static/geopositionmap/*',
        ],
    },
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Framework :: Django',
    ],
    install_requires=['django-appconf >= 0.4'],
)
