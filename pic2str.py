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
    # folder = "Female_zombie"
    # run_index = 10
    # dead_index = 12
    # # idle image
    # pic2str(f"images/{folder}/Idle (1).png", f"{folder}_Idle")
    #
    # # run images
    # with open('other_skins.py', 'a') as f:
    #     f.write(f"{folder}_Run = [\n")
    # for i in range(1, run_index+1):
    #     if i != run_index:
    #         pic2str_list(f"images/{folder}/Walk ({i}).png")
    #     else:
    #         pic2str_list(f"images/{folder}/Walk ({i}).png", final=True)
    # with open('other_skins.py', 'a') as f:
    #     f.write(f"]\n\n")
    #
    # # dead images
    # with open('other_skins.py', 'a') as f:
    #     f.write(f"{folder}_Dead = [\n")
    # for i in range(1, dead_index+1):
    #     if i != dead_index:
    #         pic2str_list(f"images/{folder}/Dead ({i}).png")
    #     else:
    #         pic2str_list(f"images/{folder}/Dead ({i}).png", final=True)
    # with open('other_skins.py', 'a') as f:
    #     f.write(f"]\n\n")
    pic2str(decode_file(extra_images.scoreboard_background), "scoreboard_background")
