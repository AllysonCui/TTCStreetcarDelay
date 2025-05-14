import requests

# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/

# To hit our API, you'll be making requests to:
base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

# Datasets are called "packages". Each package can contain many "resources"
# To retrieve the metadata for this package and its resources, use the package name in this page's URL:
url = base_url + "/api/3/action/package_show"
params = { "id": "ttc-streetcar-delay-data"}
package = requests.get(url, params = params).json()

count = 0
# To get resource data:
for _, resource in enumerate(package["result"]["resources"]):

    # for datastore_active resources:
    if resource["datastore_active"]:

        # To get all records in CSV format:
        url = base_url + "/datastore/dump/" + resource["id"]
        resource_dump_data = requests.get(url).text

        # Save the CSV data to file
        save_path = f"../data/raw_data/delay_data_{count}.csv"
        with open(save_path, 'w') as f:
            f.write(resource_dump_data)

        print(f"Saved resource {count} to file")
        count += 1
