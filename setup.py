try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='django-channels-jwt-auth-middleware',
    version='1.0.0',
    description='JWT Auth Middleware for Django Channels',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author='Joshua Hashimoto',
    author_email='onandgo.dev@gmail.com',
    url='https://github.com/joshua-hashimoto/django-channels-jwt-auth-middleware',
    packages=['django_channels_jwt_auth_middleware'],
    package_dir={
        'django_channels_jwt_auth_middleware': 'django_channels_jwt_auth_middleware'},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'django>=3.1.0',
        'channels>=3.0.0',
        'pyjwt>=2.0.0',
    ],
    license='MIT',
    zip_safe=False,
    keywords='django_channels_jwt_auth_middleware',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests.runtests.runtests',
)
