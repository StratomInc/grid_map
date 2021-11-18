from setuptools import setup

package_name = 'grid_map_2d_viewer'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    py_modules=['grid_map_2d_viewer.viewer'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Andrew Lycas',
    maintainer_email='andrew.lycas@stratom.com',
    description='2d viewer of a grid map layer in matplot lib, with the ability to click a square and see the value',
    license='Stratom Inc',
    tests_require=[],
    entry_points={
        'console_scripts': [
          'viewer = grid_map_2d_viewer.viewer:main'
        ],
    },
)
