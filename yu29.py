import sys
import pygame

from core.main import Main

if __name__ == '__main__':
	main = Main()
	for arg in sys.argv[1:]:
		if len(arg) < 5:
			continue
		arg_type = arg[2:-2]
		arg_value = arg[-1:]
		if arg_type == 'full_screen':
			main.setFullScreen(arg_value == '1')
	main.run()
	pygame.quit()
	sys.exit()