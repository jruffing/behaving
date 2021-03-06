from setuptools import setup, find_packages

version = '1.0rc3-dev'

setup(name='behaving',
      version=version,
      description="Behavior-Driven-Development testing for multi-user web/mail/sms apps",
      long_description=open("README.rst").read() + open("CHANGES.txt").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
      ],
      keywords='BDD Behavior-Driven-Development testing',
      author='Yiorgis Gozadinos',
      author_email='ggozad@crypho.com',
      url='http://github.com/ggozad/behaving',
      license='GPL',
      packages=find_packages('src', exclude=['tests']),
      package_dir={'': 'src'},
      namespace_packages=['behaving'],
      include_package_data=True,
      zip_safe=False,
      scripts=['run_behave.py', 'iosCertTrustManager.py'],
      dependency_links = ['https://github.com/tokunbo/behave-parallel/tarball/upstreamsync#egg=behave-1.2.4a1'],
      install_requires=['setuptools', 'parse', 'behave==1.2.4a1', 'splinter==0.6.0', 'Appium-Python-Client', 'simplejson', 'pyyaml', 'python-saucerest', 'unittestzero'],
      entry_points="""
      [console_scripts]
      mailmock = behaving.mail.mock:main
      smsmock = behaving.sms.mock:main
      """
      )
