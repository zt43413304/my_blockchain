from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        """
        recognize start tag, like <div>
        :param tag:
        :param attrs:
        :return:
        """
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        """
        recognize end tag, like </div>
        :param tag:
        :return:
        """
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        """
        recognize data, html content string
        :param data:
        :return:
        """
        print("Encountered some data  :", data)

    def handle_startendtag(self, tag, attrs):
        """
        recognize tag that without endtag, like <img />
        :param tag:
        :param attrs:
        :return:
        """
        print("Encountered startendtag :", tag)

    def handle_comment(self, data):
        """

        :param data:
        :return:
        """
        print("Encountered comment :", data)

    # 获取属性的函数，是个静态函数，新增的。直接定义在类中，返回属性名对应的属性
    def _attr(attrlist, attrname):
        for attr in attrlist:
            if attr[0] == attrname:
                return attr[1]
        return None

    # 获取所有p标签的文本，最简单方法只修改handle_data
    def handle_data(self, data):
        if self.lasttag == 'p':
            print("Encountered p data  :", data)

    # 获取css样式（class）为p_font的p标签的文本，使用了案例1，增加一个实例属性作为标志，选取需要的标签
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p' and _attr(attrs, 'class') == 'p_font':
            self.flag = True

    def handle_data(self, data):
        if self.flag == True:
            print("Encountered p data  :", data)

    # 获取p标签的属性列表
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            print("Encountered p attrs  :", attrs)

    # 获取p标签的class属性
    def handle_starttag(self, tag, attrs):
        if tag == 'p' and _attr(attrs, 'class'):
            print("Encountered p class  :", _attr(attrs, 'class'))

    # 获取div下的p标签的文本
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_div = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.in_div = True

    def handle_data(self, data):
        if self.in_div == True and self.lasttag == 'p':
            print("Encountered p data  :", data)


htmlf = open('/Users/Jackie.Liu/DevTools/my_blockchain/property.html', 'r', encoding="utf-8")
htmlcont = htmlf.read()

parser = MyHTMLParser()
parser.feed(htmlcont)

print(parser.handle_data("今日获取"))

parser.close()
