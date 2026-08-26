from Board import Board
from PieceDatabase import PieceDatabase
import Utility
import pygame
import os

def update_sprites(b):
    sprite_piece = {}
    piece_sprite = {}
    piece_group = pygame.sprite.Group()

    for square in b.pieces.keys():
        
        pieces = b.pieces[square]

        for piece_pair in pieces:

            image_link = PieceDatabase.piece_display[piece_pair[0]]["images"][int(piece_pair[1].colour == "W")]
            full_link = os.path.join(os.getcwd(), "StoredImages", image_link)
            image = pygame.image.load(full_link).convert_alpha()
            scaled_image = pygame.transform.scale(image, (80, 80))

            sprite = pygame.sprite.Sprite(piece_group)
            sprite.image = scaled_image
            sprite.rect = image.get_rect()
            sprite.rect.size = (80, 80)
            sprite.rect.center = Utility.get_center_of_square(square)
            piece_sprite[piece_pair[1]] = sprite
            sprite_piece[sprite] = piece_pair[1]

    return sprite_piece, piece_sprite, piece_group

if __name__ == "__main__":

    b = Board(Board.basic_setup)
    PieceDatabase.generate_piece_display()

    pygame.init()

    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("GiChess")

    screen.fill((120, 120, 120))

    running = True

    sprite_piece, piece_sprite, piece_group = update_sprites(b)

    selected_piece = None
    selected_sprite = None
    starting_square = None
    valid_squares = {}
    mouse_button_held = 0

    overlay = pygame.Surface((100, 100))
    overlay.set_alpha(100)
    overlay.fill((0, 0, 255))

    win_text = None
    win_font = pygame.freetype.Font(None)

    while running:

        for i in range(8):
        
            for j in range(8):

                if (i + j) % 2 == 0:

                    colour = (238, 238, 210)

                else: 

                    colour = (118, 150, 86)

                pygame.draw.rect(screen, colour, 
                    [100 * i, 100 * j, 100, 100], 0)

        if not b.game_ended is None:

            selected_piece = None
            selected_sprite = None
            starting_square = None
            valid_squares = {}
            mouse_button_held = 0

        if mouse_button_held == 1 and not selected_sprite is None:

            selected_sprite.rect.center = pygame.mouse.get_pos()

        if not starting_square is None:

            screen.blit(overlay, (starting_square[0] * 100, 700 - starting_square[1] * 100))

        piece_group.draw(screen)

        if not starting_square is None:

            for square in valid_squares.keys():

                pygame.draw.circle(screen, (128, 50, 50), 
                    Utility.get_center_of_square(square), 10), 

        if not b.game_ended is None:

            if win_text is None:
            
                match b.game_ended:

                    case "B":

                        win_text = "Black Wins!"

                    case "W":

                        win_text = "White Wins!"

                    case "N":

                        win_text = "Draw!"

                    case _:

                        win_text = "Error"

                win_text = win_font.render(win_text, fgcolor = (238, 238, 210), size = 80)

            text_rect = win_text[1]
            text_rect.center = screen.get_rect().center

            background_extra = 20
            bg_rect = [text_rect.left - background_extra, text_rect.top - background_extra, 
                text_rect.size[0] + 2 * background_extra, text_rect.size[1] + 2 * background_extra]
            pygame.draw.rect(screen, (118, 150, 86),
                [text_rect.left - background_extra, text_rect.top - background_extra, 
                text_rect.size[0] + 2 * background_extra, text_rect.size[1] + 2 * background_extra])

            pygame.draw.rect(screen, (128, 50, 50),
                            [text_rect.left - background_extra, text_rect.top - background_extra, 
                            text_rect.size[0] + 2 * background_extra, text_rect.size[1] + 2 * background_extra], width = 10)

            screen.blit(win_text[0], text_rect)
            

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if not b.game_ended is None:

                continue

            if event.type == pygame.MOUSEBUTTONDOWN:

                if not mouse_button_held and pygame.mouse.get_pressed()[0]:

                    mouse_button_held = 1

                    pos = pygame.mouse.get_pos()
                    clicked_square = Utility.get_square_of_pos(pos)

                    if selected_piece is None:

                        clicked_piece_sprites = [s for s in sprite_piece.keys() if s.rect.collidepoint(pos)]
                        moveable_sprites = [s for s in clicked_piece_sprites 
                            if sprite_piece[s].check_condition("ismovable", clicked_square, b)]

                        if moveable_sprites:

                            # For now,just display the first one - in future, pop up menu for all if multiple
                            selected_sprite = moveable_sprites[0]
                            selected_piece = sprite_piece[selected_sprite]
                            starting_square = Utility.get_square_of_pos(selected_sprite.rect.center)

                            valid_moves = selected_piece.get_legal_moves(clicked_square, b)
                            valid_squares = {(m[0], m[1]) : m[2] for m in valid_moves}

                        else:

                            selected_piece = None
                            selected_sprite = None
                            starting_square = None
                            valid_squares = {}

                    else:

                        if clicked_square in valid_squares.keys():

                            b.move_made(selected_piece, starting_square, 
                                (clicked_square[0], clicked_square[1], valid_squares[clicked_square]))
                            sprite_piece, piece_sprite, piece_group = update_sprites(b)
                        
                        selected_piece = None
                        selected_sprite = None
                        starting_square = None
                        valid_squares = {}

                elif not mouse_button_held and pygame.mouse.get_pressed()[2]:

                    mouse_button_held = 2

            if event.type == pygame.MOUSEBUTTONUP:

                if mouse_button_held == 1 and not pygame.mouse.get_pressed()[0]:

                    mouse_button_held = 0

                    if not selected_piece is None:

                        selected_sprite.rect.center = Utility.get_center_of_square(starting_square)

                        pos = pygame.mouse.get_pos()
                        clicked_square = Utility.get_square_of_pos(pos)

                        if clicked_square != starting_square:

                            if clicked_square in valid_squares.keys():

                                b.move_made(selected_piece, starting_square, 
                                    (clicked_square[0], clicked_square[1], valid_squares[clicked_square]))
                                sprite_piece, piece_sprite, piece_group = update_sprites(b)

                            selected_piece = None
                            selected_sprite = None
                            starting_square = None
                            valid_squares = {}

                elif mouse_button_held == 2 and not pygame.mouse.get_pressed()[2]:

                    mouse_button_held = 0
    
        pygame.display.update()

    pygame.quit()

