def draw_text(text, x, y, screen, font, text_color=(255,255,255), bg_color=(0,0,0)):
    """Method draws text on the surface."""
    t = font.render(text, True, text_color, bg_color)
    t_text = t.get_rect()
    t_text.center = (x, y)
    screen.blit(t, t_text)