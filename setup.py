from setuptools import setup, find_packages


setup(
    name='susi-assistant',
    version='0.1',
    url='https://susi.ai/',

    description='SUSI.AI Smart Personal Assistant',
    long_description='',

    author='Norbert Preining',
    author_email='norbert@preining.info',

    license='Apache License',

    python_requires='>=3.6',
    install_requires=[
        'async_promises',
        'colorlog',
        'google_speech',
        'json_config',
        'mutagen',
        'pafy',
        'pocketsphinx==0.1.15',
        'pyalsaaudio==0.8.4',
        'pyaudio',
        'python-Levenshtein',
        'python-vlc',
        'pystray',
        'requests_futures',
        'rx>=3.0.0a0',
        'service_identity',
        'snowboy==1.3.0',
        'speechRecognition==3.8.1.fossasia-4',
        'watson-developer-cloud',
        'websocket-server',
        'youtube-dl>=2019.6.21',
    ],

    packages=find_packages(),

    package_data={
        "susi": ["data/wav/*.wav", "data/flite/*", "data/img/*"],
        "susi.voice.hotword_engine": ["*.pmdl"],
        "susi.ui": ["glade_files/*", "glade_files/images/*"],
    },

    data_files = [
        ('share/applications', ['desktop/susi-assistant.desktop']),
        ('share/icons/hicolor/scalable/apps', ['icons/susi-ai.svg']),
    ],

    scripts=['bin/susi-config', 'bin/susi-voice', 'bin/susi-assistant'],

    keywords='voice_assistant personal_assistant',

    #project_urls={
    #    'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
    #    'Funding': 'https://donate.pypi.org',
    #    'Say Thanks!': 'http://saythanks.io/to/example',
    #    'Source': 'https://github.com/pypa/sampleproject/',
    #    'Tracker': 'https://github.com/pypa/sampleproject/issues',
    #},
    
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
)
