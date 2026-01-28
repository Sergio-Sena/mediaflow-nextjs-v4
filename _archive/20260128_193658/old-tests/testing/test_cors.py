import requests

url = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files"

# Test OPTIONS
print("Testing OPTIONS request...")
response = requests.options(url, headers={
    'Origin': 'https://midiaflow.sstechnologies-cloud.com',
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'authorization,content-type'
})

print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Body: {response.text}")
