import base64


def pic2str(file, functionName):
    pic = open(file, 'rb')
    content = '\n{} = {}\n'.format(functionName, base64.b64encode(pic.read()))
    pic.close()

    with open('extra_images.py', 'a') as f:
        f.write(content)


def pic2str_list(file, final=False):
    pic = open(file, 'rb')
    if not final:
        content = '{}, '.format(base64.b64encode(pic.read()))
    else:
        content = '{}'.format(base64.b64encode(pic.read()))
    pic.close()

    with open('extra_images.py', 'a') as f:
        f.write(content)


if __name__ == '__main__':
    pic2str("logo.png", "var")
