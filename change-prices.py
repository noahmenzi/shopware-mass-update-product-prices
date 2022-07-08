#!/usr/bin/python3

# importing the module
import json
import requests

# Shopware API URL
# For Version 6.3 its /api/v3/
# For Version 6.4 and above /api/
URL = "https://<your-shop>.ch/api/v3/"
 
 # Headers, replace YOUR_API_KEY
HEADERS = {
    "Content-Type": "application/json;",
    "Authorization": "Bearer <your-key>"
}


def checkProductExists(product_sku):
    search_endpoint = URL + 'search/product'
    search_json = '{"filter": [{"type": "equals","field": "productNumber","value": "'
    search_json += product_sku
    search_json += "\"}]}"

    response = requests.post(search_endpoint, headers=HEADERS, data=search_json)
    data = response.json()
    print(data)
    if (data["meta"]["total"]) == 0:
        return False
    else:
        return (data["data"][0]["id"])



def get_valid_skus():
    # Input SKUs without sizes
    with open('sku_without_sizes.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    sizes = ['38M', '38', '39', '39M', '40', '41', '42', '43', '44', '45', '46', '47', '48']

    # Declare an empty list
    products = []

    for l in lines:
        for s in sizes:
            products.append(l + "." + s);

    with open("output.txt", "w") as txt_file:
        for p in products:
            print("Checking " + p)
            respone = checkProductExists(p)
            if respone == False:
                products.remove(p)
            else:
                txt_file.write(respone + "\n")

def changePrices():
    with open('output.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    for l in lines:
        print(l)
        changePrice(l)


def changePrice(product):
    endpoint = URL + 'product/' + product

    response = requests.get(endpoint, headers=HEADERS)
    data = response.json()
    # print(data)
    # print(data["data"]["attributes"]["price"])
    if data["data"]["attributes"]["price"] is not None:
        old_price_gross = data["data"]["attributes"]["price"][0]["gross"]
        old_price_net = data["data"]["attributes"]["price"][0]["net"]
        patch_json = '{"price":[{"currencyId":"b7d2554b0ce847cd82f3ac9bd1c0dfca","net":46.43,"gross":50.0,"linked":true,"listPrice":{"currencyId":"b7d2554b0ce847cd82f3ac9bd1c0dfca","net": '
        patch_json += str(old_price_net) + ', "gross": '
        patch_json += str(old_price_gross) + ',"linked":true}}]}'
        # print(patch_json)
        response = requests.patch(endpoint, headers=HEADERS, data=patch_json)
        print(response.status_code)


# First, get the valid_skus(), second change the prices
get_valid_skus()
changePrices()
