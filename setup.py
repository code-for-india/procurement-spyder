from setuptools import setup

setup(name='Procurement Spyder',
      version='1.0',
      description='Track and Notify about new procurement in WorldBank site.',
      author='Fizer Khan, Yogeswaran',
      author_email='fizerkhan@gmail.com, yogeeswaran@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask', 'MarkupSafe', 'pymongo', 'datetime',
                        'requests', 'BeautifulSoup', 'recaptcha-client'],
     )
