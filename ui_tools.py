import pygame

pygame.init()


def draw_bordered_rounded_rect(surface, rect, color, border_color, corner_radius, border_thickness):
    rect_tmp = pygame.Rect(rect)

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            pygame.draw.rect(surface, border_color, rect_tmp, border_radius=corner_radius)

        rect_tmp.inflate_ip(-2 * border_thickness, -2 * border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        pygame.draw.rect(surface, color, rect_tmp, border_radius=inner_radius)


class Button:
    """A fairly straight forward button class."""

    def __init__(self, rect, color, function, text=None, font=pygame.font.Font(None, 36), call_on_release=True,
                 hover_color=None, clicked_color=None, font_color=pygame.Color("white"), hover_font_color=None,
                 clicked_font_color=None, click_sound=None, hover_sound=None, image=None, text_position=None,
                 image_position=None, border_radius=0, border_color=None, image_align=None, fill_bg=True,
                 border_thickness: int = 7, state_disabled: bool = False, disabled_image=None, disabled_color=None,
                 disabled_border_color=None, **kwargs):

        self.image = image
        self.text = text
        self.font = font
        self.call_on_release = call_on_release
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        self.font_color = font_color
        self.hover_font_color = hover_font_color
        self.clicked_font_color = clicked_font_color
        self.click_sound = click_sound
        self.hover_sound = hover_sound
        self.image_original = image
        self.text_position = text_position
        self.image_position = image_position
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_color_copy = border_color
        self.image_align = image_align
        self.image_copy = self.image_original
        self.fill_bg = fill_bg
        self.border_thickness = border_thickness
        self.state_disabled = state_disabled
        self.disabled_image = disabled_image
        self.disabled_color = disabled_color
        self.disabled_border_color = disabled_border_color
        self.kwargs = kwargs
        if self.image_original:
            if not isinstance(self.image_original, list):
                self.image_copy = pygame.transform.scale(
                    self.image_original,
                    (0.87 * self.image_original.get_width(), 0.76 * self.image_original.get_height()))
            else:
                self.image_copy = [pygame.transform.scale(
                    image, (0.87 * image.get_width(), 0.76 * image.get_height()))
                    for image in self.image_original]

        self.rect_original = pygame.Rect(rect)
        self.rect = self.rect_original.copy()
        self.rect_inflated = self.rect_original.inflate(-0.13 * self.rect_original.w,
                                                        -0.24 * self.rect_original.h)
        self.color = color
        self.color_copy = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.render_text()

    def move(self, x_add=0, y_add=0):
        self.rect_original.x += x_add
        self.rect_inflated.x += x_add
        self.rect_original.y += y_add
        self.rect_inflated.y += y_add

    def render_text(self):
        """Pre render the button text."""
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text, True, color)
            self.text = self.font.render(self.text, True, self.font_color)

    def check_event(self, event):
        """The button needs to be passed events from your program event loop."""
        if not self.state_disabled:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_click(event)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.on_release()

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                if self.kwargs:
                    self.function(self.kwargs)
                else:
                    self.function()

    def on_release(self):
        if self.clicked and self.call_on_release:
            if self.kwargs:
                self.function(self.kwargs)
            else:
                self.function()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.state_disabled:
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self, surface):
        """Update needs to be called every frame in the main loop."""
        color = self.color
        text = self.text
        self.image = self.image_original
        self.rect = self.rect_original
        self.color = self.color_copy
        self.border_color = self.border_color_copy

        self.check_hover()
        if self.state_disabled and self.disabled_image:
            self.image = self.disabled_image
        if self.state_disabled and self.disabled_color:
            self.color = self.disabled_color
        if self.state_disabled and self.disabled_border_color:
            self.border_color = self.disabled_border_color

        if self.clicked:
            if self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            self.image = self.image_copy
            self.rect = self.rect_inflated
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                text = self.hover_text

        if self.border_radius and self.border_color and not self.clicked:
            draw_bordered_rounded_rect(surface, self.rect, color, self.border_color, self.border_radius,
                                       self.border_thickness)
            # pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        elif self.border_radius:
            # draw_rounded_rect(surface, self.rect, color, self.border_radius)
            pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        elif self.fill_bg:
            surface.fill(pygame.Color("black"), self.rect)
            pygame.draw.rect(surface, self.color, self.rect.inflate(-4, -4))

        if text and not self.text_position and not self.image:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        elif text and self.text_position:
            surface.blit(text, (self.rect.x + self.text_position[0], self.rect.y + self.text_position[1]))

        if self.image and self.image_position:
            if not isinstance(self.image, list):
                surface.blit(self.image, (self.rect.x + self.image_position[0], self.rect.y + self.image_position[1]))
            else:
                for index, image in enumerate(self.image):
                    surface.blit(image, (
                        self.rect.x + self.image_position[index][0], self.rect.y + self.image_position[index][1]))
        elif self.image and self.image_align == "bottom":
            image_rect = self.image.get_rect()
            image_rect.centerx = self.rect.centerx
            image_rect.bottom = self.rect.y + self.rect.height - (
                    self.rect.height - self.image.get_height() - text.get_height() - 5) / 2
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.top = self.rect.y + (self.rect.height - self.image.get_height() - text.get_height() - 5) / 2
            surface.blit(self.image, image_rect)
            surface.blit(text, text_rect)
        elif self.image and self.image_align == "top" and text:
            image_rect = self.image.get_rect()
            image_rect.centerx = self.rect.centerx
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            image_rect.top = self.rect.y + (self.rect.height - self.image.get_height() - text.get_height()) / 2
            text_rect.bottom = self.rect.y + self.rect.height - (
                    self.rect.height - self.image.get_height() - text.get_height()) / 2
            surface.blit(self.image, image_rect)
            surface.blit(text, text_rect)
        elif self.image and not self.image_position and not self.image_align:
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)


class InputBox:

    def __init__(self, x: int, y: int, w: int, h: int, color_inactive: tuple[int, int, int],
                 color_active: tuple[int, int, int], color_hover: tuple[int, int, int], function=None,
                 font: pygame.font.Font = None, text: str = '',
                 font_color: tuple[int, int, int] = (255, 255, 255), active: bool = False, border_radius: int = 0,
                 remove_active=False, cursor_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color_hover = color_hover
        self.font = font if font else pygame.font.Font(None, h - 5)
        self.text = ""
        self.font_color = font_color
        self.given_text = text
        self.active = active
        self.function = function
        self.border_radius = border_radius
        self.remove_active = remove_active
        self.cursor_color = cursor_color
        if self.active:
            self.txt_surface = self.font.render(self.text, True, self.font_color)
        else:
            self.txt_surface = self.font.render(self.given_text, True, (238, 234, 222))
        self.draw_cursor = 0
        self.drawn = False

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.remove_active:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.color_hover
        else:
            self.color = self.color_inactive
            # Change the current color of the input box.
        if self.active:
            self.color = self.color_active
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN and self.text:
                    if self.function:
                        self.function(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.font.render(self.text + event.unicode, True,
                                        self.font_color).get_width() <= self.rect.w - 10 and event.key != pygame.K_RETURN:
                        self.text += event.unicode
                # Re-render the text.
        if self.active:
            self.txt_surface = self.font.render(self.text, True, self.font_color)

    def cursor(self, screen):
        if self.active:
            if (self.drawn and self.draw_cursor % 60 != 0) or (not self.drawn and self.draw_cursor % 60 == 0):
                pygame.draw.line(screen, self.cursor_color,
                                 (self.txt_surface.get_width() + self.rect.x + 5, self.rect.y + 7),
                                 (self.txt_surface.get_width() + self.rect.x + 5, self.rect.bottom - 7), width=2)
                self.drawn = True
            else:
                self.drawn = False
            self.draw_cursor += 1

    def update(self, screen):
        draw_bordered_rounded_rect(screen, self.rect, self.color, (0, 0, 0), self.border_radius, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        self.cursor(screen)
