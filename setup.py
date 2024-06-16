"""Install the package using the setup.py file."""

from tomllib import load

from setuptools import setup, find_packages


def main() -> None:
    """Main function for the setup.py file."""
    with open('./pyproject.toml', 'rb') as toml_file:
        project_data: dict = load(toml_file)

    authors_data: dict = project_data['project']['authors']
    authors: str = ', '.join(map(lambda x: x['name'], authors_data))
    emails:  str = ', '.join(map(lambda x: x['email'], authors_data))

    setup(
        name=project_data['project']['name'],
        description=project_data['project']['description'],
        url=project_data['project']['urls']['Homepage'],

        license='',
        version=project_data['project']['version'],

        author=authors,
        author_email=emails,

        packages=find_packages(where='src'),
        package_dir={"": "src"},
    )


if __name__ == '__main__':
    main()
