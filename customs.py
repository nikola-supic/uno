import pygame

class Button():
	"""
	DOCSTRING:

	"""
	def __init__(self, surface, text, pos, size, bg_color, text_size=20, text_font=None, text_color=(0,0,0), border=0, border_color=(0,0,0)):
		self.surface = surface
		self.text = text
		self.pos = pos
		self.size = size
		self.bg_color = bg_color
		self.text_size = text_size
		self.text_font = text_font
		self.text_color = text_color
		self.border = border
		self.border_color = border_color
		
		self.rect = pygame.Rect(pos[0]+self.border, pos[1]+self.border, size[0]-self.border*2, size[1]-self.border*2)

	def draw(self):
		x, y = self.pos
		width, height = self.size

		if self.border > 0:
			bg = pygame.Rect(x, y, width, height)
			pygame.draw.rect(self.surface, self.border_color, bg)

		self.rect = pygame.Rect(x+self.border, y+self.border, width-self.border*2, height-self.border*2)
		pygame.draw.rect(self.surface, self.bg_color, self.rect)
		Text(self.surface, self.text, (x + width/2, y + height/2), self.text_color, self.text_size, self.text_font, True)

class Text():
	"""
	DOCSTRING:

	"""
	def __init__(self, surface, text, pos, color, text_size=22, text_font=None, center=False):
		self.surface = surface
		self.text = text
		self.pos = pos
		self.color = color

		self.text_size = text_size
		self.text_font = text_font
		self.center = center
		
		self.draw()

	def draw(self):
		x, y = self.pos
		font = pygame.font.SysFont(self.text_font, self.text_size)
		txt = font.render(self.text, True, self.color)
		if self.center:
			text_rect = txt.get_rect(center=(x, y))
		else:
			text_rect = txt.get_rect(midleft=(x, y))
		self.surface.blit(txt, text_rect)

class ImageButton():
	"""
	DOCSTRING:

	"""
	def __init__(self, surface, image, size, pos, alt_text):
		self.surface = surface
		self.image = image
		self.size = size
		self.pos = pos
		self.alt_text = alt_text

	def draw(self):
		bg = pygame.image.load(self.image)
		bg = pygame.transform.scale(bg, self.size)
		self.surface.blit(bg, self.pos)
		return bg

	def click(self, click_pos):
		x1, y1 = click_pos
		x, y = self.pos
		width, height = self.size
		if x <= x1 <= x + width and y <= y1 <= y + height:
			return True
		return False


def main():
	width = 500
	height = 500
	win = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Client")
	pygame.font.init()

	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	RED = (255, 0, 0)
	GREEN = (74, 145, 35)
	YELLOW = (242, 209, 17)
	ORANGE = (242, 118, 9)

	clock = pygame.time.Clock()
	click = False
	while True:
		clock.tick(60)
		win.fill((128, 128, 128))	
		rock = ImageButton(win, 'images/rock.png', (150, 150), (20, 20))
		paper = ImageButton(win, 'images/paper.png', (150, 150), (20, 180))
		scissors = ImageButton(win, 'images/scissors.png', (150, 150), (20, 330))
		mx, my = pygame.mouse.get_pos()

		if click:
			if rock.click((mx, my)):
				print('ROCK CLICKED')
			if paper.click((mx, my)):
				print('PAPER CLICKED')
			if scissors.click((mx, my)):
				print('SCISSORS CLICKED')

		click = False
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True

		pygame.display.update()

	pygame.quit()


if __name__ == '__main__':
	main()