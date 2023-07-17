import pygame.draw
from pygame.sprite import Sprite

AIR_RESISTANCE = 1.2


class Net:

    def __init__(self, group, basket):
        super().__init__()
        self.width = basket.width
        self.height = 80
        self.x = basket.left_edge.rect.x
        self.y = basket.left_edge.rect.centery
        self.number_of_vertical_strings = 10
        self.vertical_strings = []
        self.distance_between_vertical_strings = self.width // (self.number_of_vertical_strings-1)
        for string in range(self.number_of_vertical_strings):
            s = String(self.x + string * self.distance_between_vertical_strings - self.distance_between_vertical_strings / 2, self.y - (string**2.05-self.number_of_vertical_strings*string - 5), self.height, group)
            self.vertical_strings.append(s)

    def update(self, basket):
        for string in self.vertical_strings:
            for segment in string.segments:
                segment.update(basket)



class String:
    def __init__(self, mount_x_offset: int, mount_y, length, group):
        super().__init__()
        self.mount_x_offset = mount_x_offset
        self.mount_y = mount_y
        self.length = length
        self.segment_length = 20
        self.number_of_segments = self.length//self.segment_length
        self.segments = []
        for segment in range(self.number_of_segments):
            s = StringSegment(segment, self.mount_x_offset, self.mount_y, self.segment_length, group)
            self.segments.append(s)


class StringSegment(Sprite):
    def __init__(self, segment_number: int, mount_x_offset: int, y_pos: int, length, group):
        super().__init__()
        self.length = length
        self.layer = 2
        self.mouse_x_vel = 0
        self.x_vel = 0
        self.y_pos = y_pos
        self.mount_x_offset = mount_x_offset
        self.segment_number = segment_number
        self.string_image = pygame.Surface((self.length, self.length))
        self.string_image.set_colorkey((0, 0, 0,))
        pygame.draw.line(self.string_image, (240, 240, 240), (self.length/2, 0), (self.length/2, self.length))
        self.image = pygame.Surface((self.length, self.length))
        self.image.set_colorkey((0, 0, 0,))
        self.rect = self.image.get_rect()
        self.rect.x = mount_x_offset
        self.rect.y = self.y_pos + self.length * self.segment_number
        self.add(group)

    def update(self, basket):
        self.mouse_x_vel = pygame.mouse.get_rel()[0]
        self.x_vel += -self.mouse_x_vel/2
        self.x_vel /= AIR_RESISTANCE
        self.rect.x = basket.left_edge.rect.x + self.mount_x_offset

        if self.x_vel > 0:
            self.image = pygame.transform.rotate(self.string_image, self.x_vel)
        if self.x_vel < 0:
            self.image = pygame.transform.rotate(self.string_image, self.x_vel)
        self.image.blit(self.string_image, (self.length/2-self.image.get_width()/2, self.length/2-self.image.get_height()/2))

    def draw(self, screen):
        pass