from Level import level_list
stars_required = [0, 1, 5, 6, 10]


def calculate_current_level(vars_dic: dict):
    """
    Cleans and uses the json file to determine the level. If someone already chose a level using the level screen than
    that is the level, else the level is found out by seeing if the user has ever completed the level
    :param vars_dic: The json file that has been opened
    :return: returns the level object
    """
    games_played = sorted(vars_dic["users"][vars_dic["current_user"][0]][1], key=lambda x: (x[0], x[1], x[2], x[3]),
                          reverse=True)

    current_stars = 0
    for level in level_list:
        for game in games_played:
            if level.str == game[0]:
                current_stars += game[1]
                break

    current_level = None
    for index, level in enumerate(level_list):
        if current_stars >= stars_required[index]:
            current_level = level
        else:
            break

    if not current_level:
        current_level = level_list[4]
    # print(current_level)
    return current_level


def blit_text(surface, text, pos, font, right_pos, color=(0, 0, 0), alpha=255, alignment="center"):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    centerx, top = pos
    end_pos = 0
    for line in words:
        text_line = ""
        for word in line:
            text_line += word + " "
            word_surface = font.render(text_line, True, color)
            word_width, word_height = word_surface.get_size()
            if (centerx + word_width/2 > right_pos and alignment == "center") or \
                    (centerx + word_width > right_pos and alignment == "left"):
                word_surface.set_alpha(alpha)
                if alignment == "center":
                    surface.blit(word_surface, word_surface.get_rect(center=(centerx, top)))
                    end_pos = max(word_surface.get_rect(center=(centerx, top)).right, end_pos)
                else:
                    surface.blit(word_surface, word_surface.get_rect(topleft=(centerx, top)))
                    end_pos = max(word_surface.get_rect(topleft=(centerx, top)).right, end_pos)
                text_line = ""
                top += word_height + 5  # Start on new row.
        word = font.render(text_line, True, color)
        word.set_alpha(alpha)
        if alignment == "center":
            surface.blit(word, word.get_rect(center=(centerx, top)))
            end_pos = max(word.get_rect(center=(centerx, top)).right, end_pos)
        else:
            surface.blit(word, word.get_rect(topleft=(centerx, top)))
            end_pos = max(word.get_rect(topleft=(centerx, top)).right, end_pos)
        top += word_height  # Start on new row.
    return end_pos
