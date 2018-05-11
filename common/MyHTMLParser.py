from bs4 import BeautifulSoup

with open('/Users/Jackie.Liu/DevTools/my_blockchain/property.html', 'r') as foo_file:
    soup_foo = BeautifulSoup(foo_file, "html.parser")
# print(soup_foo)

# <div class="main">
book = soup_foo.find(name=None, attrs={"class": "main"})
print(book)
