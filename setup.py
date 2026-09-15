from setuptools import find_packages, setup

with open("retail_suite/retail_suite/__init__.py") as f:
    version = "0.0.1"
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split(" = ")[1]
            break

setup(
    name="retail_suite",
    version=version,
    description="Six retail industry verticals (Apparel, Footwear, Accessories, Home Makeover, Lifestyle & Fashion, FMCG) for ERPNext.",
    author="Retail Industry Suite",
    author_email="admin@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
)
