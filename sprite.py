import math
import pyglet

class ScoreboardIconSprite :
    def __init__(self, image, batch):
        self.icon = pyglet.sprite.Sprite(image, batch=batch)
        self.speed = 20
        self.scale_speed = 4
        self.moving = False
        self.icon.x = 300
        self.icon.y = 200

    def setVisible(self, value) :
        self.icon.visible = value

    def setCenterAndScale(self, tuple) :
        self.icon.scale = tuple[2]
        self.icon.x = tuple[0] - self.icon.width / 2
        self.icon.y = tuple[1] - self.icon.height / 2

        # larger scales are drawn in front of smaller scales so use scale to create groups
        groupNum = math.floor(self.icon.scale * 1000000000) 
        self.icon.group = pyglet.graphics.Group(order=groupNum)

    def setPath(self, path) :
        self.path = path

    def getSprite(self) :
        return self.icon

    def centerX(self) :
        return self.icon.x + self.icon.width / 2
    
    def centerY(self) :
        return self.icon.y + self.icon.height / 2

    # path is a list of location tuples (x, y, scale) where (x,y) is center
    # last element of path is final destination
    def moveTo(self, path) :
        self.pathIndex = 0
        self.path = path
        self.currentDest = self.path[self.pathIndex]
        self.moving = True

    def getDistance(self, dest_x, dest_y) :
        return math.sqrt((self.centerX() - dest_x) ** 2 + (self.centerY() - dest_y) ** 2)


    def update(self, dt) :
        if self.moving :
            x_d = self.currentDest[0] - self.centerX()
            y_d = self.currentDest[1] - self.centerY()
            scale_d = self.currentDest[2] - self.icon.scale

            angle = math.atan2(y_d, x_d)
            distance = self.getDistance(self.currentDest[0], self.currentDest[1]) 
            speed = min(self.speed, distance)
            change_x = math.cos(angle) * speed
            change_y = math.sin(angle) * speed
            change_scale =  scale_d / self.scale_speed
            self.setCenterAndScale((self.centerX()+change_x, self.centerY() + change_y, self.icon.scale + change_scale))
            distance = self.getDistance(self.currentDest[0], self.currentDest[1]) 

            # close enough?
            if distance <= self.speed:
                self.setCenterAndScale(self.path[self.pathIndex])
                self.pathIndex += 1
                if (self.pathIndex >= len(self.path)) :
                    self.moving= False
                else :
                    self.currentDest = self.path[self.pathIndex]

