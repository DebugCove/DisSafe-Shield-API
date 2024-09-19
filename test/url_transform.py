def url_transform(urls):
    if isinstance(urls, list):
        return urls

    return urls.split()


urls = "https://example.com https://test.com https://another_example.com"
print(url_transform(urls)) 
