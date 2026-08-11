from setuptools import find_packages, setup

package_name = 'example'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='timu',
    maintainer_email='tm@timuai.com',
    description='timu example',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple = example.simple:main',
            'chat = example.xiaomu_chat:main',
            'move = example.xiaomu_move:main',
            'sense = example.xiaomu_sensor:main',
            'speak = example.xiaomu_speak:main',
            'touch = example.xiaomu_touch:main',
            'vision = example.xiaomu_vision:main',
        ],
    },
)
