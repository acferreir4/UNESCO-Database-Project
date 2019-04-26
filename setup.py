from setuptools import setup, find_packages

setup(
    # Application name:
    name="UNESCO app",
    # Version number
    version="0.0.1",
    description="A database for UNESCO Indigenous education researchers.",
    # Packages
    packages=find_packages(),

    # Application author details:
    author="Andrew Ferreira, Asma Hassan, Dan Sheng, Eric Dao, Shahriar Dhrubo",
    author_email="acferreir4@gmail.com",
    url="https://github.com/acferreir4/UNESCO-Database-Project",

    # Include additional files into the package
    include_package_data=True,

    license="LICENSE",
    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "django",
        "django-crispy-forms",
	"channels_redis",
	"channels",
	"pillow",
	"django-phonenumber-field",
	"phonenumbers",
	"django-heroku",
    ],
)
