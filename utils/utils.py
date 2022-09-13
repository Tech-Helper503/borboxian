from ursina.text import Text

calculate_font_offset = lambda x_pos, text, font: x_pos - Text.get_width(text,font=font)