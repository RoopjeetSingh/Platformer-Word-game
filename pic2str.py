import base64


def pic2str(file, functionName):
    pic = open(file, 'rb')
    content = '\n{} = {}\n\n'.format(functionName, base64.b64encode(pic.read()))
    pic.close()

    with open('remaining_images.py', 'a') as f:
        f.write(content)


def pic2str_list(file, final=False):
    pic = open(file, 'rb')
    if not final:
        content = '{}, '.format(base64.b64encode(pic.read()))
    else:
        content = '{}\n\n'.format(base64.b64encode(pic.read()))
    pic.close()

    with open('remaining_images.py', 'a') as f:
        f.write(content)


if __name__ == '__main__':
    # pic2str("images/question.png", "question")
    import cv2
    import numpy as np
    image = cv2.imread("images/question.png")
    np.save('myarray.py', image)
    # with open('remaining_images.py', 'a') as f:
    #     f.write("ninja_girl2_glide = [")
    # for i in range(1, 10):
    #     pic2str_list(f"images/Ninja_girl2/Glide ({i}).png")
    # pic2str_list(f"images/Ninja_girl2/Glide (10).png", True)
    # with open('remaining_images.py', 'a') as f:
    #     f.write("]")