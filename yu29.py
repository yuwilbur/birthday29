import sys
import pygame

from core.main import Main

if __name__ == '__main__':
	main = Main()
	for arg in sys.argv[1:]:
		if arg[1:-2] == 'full_screen':
			main.setFullScreen(arg[-1:] == '1')
	main.run()
	pygame.quit()
	sys.exit()