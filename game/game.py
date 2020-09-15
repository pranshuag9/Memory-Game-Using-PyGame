import pygame as pg
import sys
import random
from pygame.locals import Rect

GRID_SIZE = 4	# Number of cells across row/column
N_PIXELS = 100	# Number of pixels in one cell across row/column
N_SHAPES = 4	# Number of shapes used in the game
N_OCC = int((GRID_SIZE*GRID_SIZE)/N_SHAPES)	# Number of occurences of a shape
cells = [x for x in range(1,GRID_SIZE*GRID_SIZE+1)]
cellObjects = []
shapesarrangement = []

def drawBackground():
	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE):
			col = int(j)*N_PIXELS
			row = int(i)*N_PIXELS
			rect_obj = Rect(col,row,N_PIXELS,N_PIXELS)
			cellObjects.append(rect_obj)
			pg.draw.rect(Window,(96,128,64),rect_obj,2)

def drawRecShape(x,color):
	row = int((x-1)/GRID_SIZE)*N_PIXELS
	col = int((x-1)%GRID_SIZE)*N_PIXELS
	pg.draw.rect(Window, color, Rect(col+20,row+20,60,60))

def drawCirShape(x,color):
	row = int((x-1)/GRID_SIZE)*N_PIXELS
	col = int((x-1)%GRID_SIZE)*N_PIXELS
	pg.draw.circle(Window, color, (col+50, row+50),30)

def drawTriShape(x,color):
	row = int((x-1)/GRID_SIZE)*N_PIXELS
	col = int((x-1)%GRID_SIZE)*N_PIXELS
	pg.draw.polygon(Window,color,((col+10,row+20),(col+90,row+20),(col+50,row+80)))

def drawDiamondShape(x,color):
	row = int((x-1)/GRID_SIZE)*N_PIXELS
	col = int((x-1)%GRID_SIZE)*N_PIXELS
	pg.draw.polygon(Window,color,((col+10,row+50),(col+50,row+20),(col+90,row+50),(col+50,row+80)))

def startGame():
	for i in range(N_OCC):
		if i is 0 or i is 1: color = (0,0,255)
		else: color = (0,255,0)
		x = random.choice(cells)
		shapesarrangement.append(x)
		drawRecShape(x,color)
		cells.remove(x)
	for i in range(N_OCC):
		if i is 0 or i is 1: color = (255,255,0)
		else: color = (0,255,255)
		x = random.choice(cells)
		shapesarrangement.append(x)
		drawCirShape(x,color)
		cells.remove(x)
	for i in range(N_OCC):
		if i is 0 or i is 1: color = (255,0,255)
		else: color = (128,0,0)
		x = random.choice(cells)
		shapesarrangement.append(x)
		drawTriShape(x,color)
		cells.remove(x)
	for i in range(N_OCC):
		if i is 0 or i is 1: color = (128,128,0)
		else: color = (128,0,128)
		x = random.choice(cells)
		shapesarrangement.append(x)
		drawDiamondShape(x,color)
		cells.remove(x)

def shapeIndex(mouse_pos):
	for i in range(GRID_SIZE*GRID_SIZE):
		if cellObjects[i].collidepoint(mouse_pos):
			return shapesarrangement.index(i+1)

def cellNo(mouse_pos):
	for i in range(GRID_SIZE*GRID_SIZE):
		if cellObjects[i].collidepoint(mouse_pos):
			return i+1

def rightchoice(firstchoice, secondchoice):
	x = shapeIndex(firstchoice)
	y = shapeIndex(secondchoice)
	for i in range(0,16,2):
		j = i+1
		if ((x is i and y is j) or (x is j and y is i)):
			return True

def hide(mouse_pos):
	cell_num = cellNo(mouse_pos)
	for i in range(GRID_SIZE*GRID_SIZE):
		if cell_num is i+1:
			pg.draw.rect(Window,(255,255,255),cellObjects[i].inflate(-10,-10))

def show(mouse_pos):
	cell_num = cellNo(mouse_pos)
	shapeindex = shapeIndex(mouse_pos)
	if shapeindex is 0 or shapeindex is 1:
		color = (0,0,255)
		drawRecShape(cell_num, color)
	elif shapeindex is 2 or shapeindex is 3:
		color = (0,255,0)
		drawRecShape(cell_num, color)
	elif shapeindex is 4 or shapeindex is 5:
		color = (255,255,0)
		drawCirShape(cell_num, color)
	elif shapeindex is 6 or shapeindex is 7:
		color = (0,255,255)
		drawCirShape(cell_num, color)
	elif shapeindex is 8 or shapeindex is 9:
		color = (255,0,255)
		drawTriShape(cell_num, color)
	elif shapeindex is 10 or shapeindex is 11:
		color = (128,0,0)
		drawTriShape(cell_num, color)
	elif shapeindex is 12 or shapeindex is 13:
		color = (128,128,0)
		drawDiamondShape(cell_num, color)
	elif shapeindex is 14 or shapeindex is 15:
		color = (128,0,128)
		drawDiamondShape(cell_num, color)

def main():
	pg.init()
	global Window
	Window = pg.display.set_mode((GRID_SIZE*N_PIXELS, GRID_SIZE*N_PIXELS))
	Window.fill((255,255,255))
	pg.display.set_caption('Memory Game')

	drawBackground()
	startGame()
	pg.display.update()

	pg.time.wait(3000)
	Window.fill((255,255,255))
	drawBackground()
	pg.display.update()

	flag = 0
	truechoices = []

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			elif event.type==pg.MOUSEBUTTONUP:
				mouse_pos = pg.mouse.get_pos()
				show(mouse_pos)
				pg.display.update()
				if flag is 0:
					firstchoice = mouse_pos
					if cellNo(firstchoice) in truechoices: flag = 0
					else: flag = 1
				else:
					secondchoice = mouse_pos
					if cellNo(secondchoice) in truechoices: flag = 1
					else: flag = 0
					if not (cellNo(firstchoice) in truechoices) and not (cellNo(secondchoice) in truechoices):
						if rightchoice(firstchoice, secondchoice):
							truechoices.append(cellNo(firstchoice))
							truechoices.append(cellNo(secondchoice))
						else:
							pg.time.wait(1)
							hide(firstchoice)
							hide(secondchoice)
							pg.display.update()

			if len(truechoices) is GRID_SIZE*GRID_SIZE:
				image = pg.image.load('./winner-winner-boom-boom.png')
				image = pg.transform.scale(image, (GRID_SIZE*N_PIXELS+10,GRID_SIZE*N_PIXELS+10))
				Window.blit(image, (0,0))
				Font1 = pg.font.SysFont('arial',32,True,True)
				textsurface = Font1.render('Winner Winner Boom Boom!!!', True, (0,0,0))
				Window.blit(textsurface, (N_PIXELS-80,N_PIXELS+50))
				pg.display.update()

if __name__ == '__main__':
	main()