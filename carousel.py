class MenuLocationNode :
    IS_EMPTY = -1

    def __init__(self, location) :
        self.location = location
        self.setFront(self)
        self.setBack(self) 
        self.stagedIndex = MenuLocationNode.IS_EMPTY
        self.index = MenuLocationNode.IS_EMPTY

    def setIndex(self, index) :
        self.index = index
    
    def setStagedIndex(self, staged) :
        self.stagedIndex = staged
    
    def updateIndex(self) :
        self.index = self.stagedIndex

    def getIndex(self) :
        return self.index

    def getLocation(self) :
        return self.location

    def isEmpty(self) :
        return self.index <= MenuLocationNode.IS_EMPTY

    def setFront(self, node) :
        self.front = node
    
    def setBack(self, node) :
        self.back = node

    def getFront(self) :
        return self.front

    def getBack(self) :
        return self.back


################################################
class Carousel : 
    INDEX_ICON = 3

    def __init__(self, controlPoints, scoreboards)  :
        self.scoreboards = scoreboards
        self.conotrlPoints = controlPoints
        self.listFront = None
        self.build()

    def build(self) :
        print("building")
        tempFront = None
        for c in self.conotrlPoints :
            newNode = MenuLocationNode(c)
            if self.listFront is None :
                self.listFront = newNode
                tempFront = self.listFront
            else :
                self.insertInFrontOf(tempFront, newNode)
                tempFront = newNode

        self.backCenter = self.listFront
        for i in range(0, len(self.conotrlPoints) // 2) :
            self.backCenter = self.backCenter.getFront()
        

        # assign index into icon list to each node 
        # and add more nodes if needed
        size = len(self.scoreboards)
        end = size # position of final item to be placed
        if size > 0 :
            self.listFront.setIndex(0)   # always one in front
        if size > 1 :
            self.listFront.getBack().setIndex(1) 
        if size > 2 :
            self.listFront.getFront().setIndex(2)
        if size > 3 and size % 2 == 0 : #put end of list in center back, if even number of items
            self.backCenter.setIndex(size-1)
            end -= 1
        if size > 5 : # add 3 and 4 to the 'front'
            self.listFront.getBack().getBack().setIndex(3)
            self.listFront.getFront().getFront().setIndex(4)
            
            # Now, 5 items in front, one in back if even number, and an even number of leftover items
            # add half of those leftovers to each side

            # find range to add to each side
            # left range is 5 to  5 + number of items/2 - 1
            numPerSide = (end - 5) // 2
            leftmostNode = self.backCenter.getBack().getBack()
            rightmostNode = self.backCenter.getFront().getFront()
            self.scatterRemains(5, 5 + numPerSide - 1, leftmostNode, self.backCenter) 
            self.scatterRemains(5 + numPerSide, end-1,  self.backCenter, rightmostNode)
        elif size == 5 :  # 4 or 5 items in list 
            self.backCenter.getBack().setIndex(3)
            self.backCenter.getFront().setIndex(4)
    
    # TODO: spread the remainder between back left and back right
    # will always have an even number of elements to distribute
    # always one node between leftNode and rightNode
    def scatterRemains(self, startIndex, endIndex, leftNode, rightNode) :
        # if odd number to place (1, 3, 5, etc) place one in gap node
        # odd number to place if end - start is even
        print("scattering")
        gapNode = leftNode.getFront()
        if (endIndex - startIndex) % 2 == 0 :
            gapNode.setIndex(startIndex)   
            startIndex += 1
             
        # if more than 1 node left, need new nodes in gaps
        if (endIndex - startIndex) > 0 : 
            self.createNewNode(leftNode, gapNode)   
            self.createNewNode(gapNode, rightNode)
            nodesPerSide = (1 + endIndex - startIndex ) // 2
            self.scatterRemains(startIndex, startIndex + nodesPerSide - 1, leftNode, gapNode)
            self.scatterRemains(startIndex + nodesPerSide, endIndex, gapNode, rightNode)

            # if odd number to place, place middle one in gap node,  recurse
            
    def createNewNode(self, leftNode, rightNode) :
        location = self.calculateLocation(leftNode.getLocation(), rightNode.getLocation())
        newNode = MenuLocationNode(location)
        self.insertInFrontOf(leftNode, newNode)

    def calculateGroup(self, leftGroup, rightGroup) :
        return leftGroup + (rightGroup - leftGroup) // 2
        
    # average position and scale between two points
    def calculateLocation(self, leftLoc, rightLoc) :
        x = leftLoc[0] + (rightLoc[0] - leftLoc[0]) / 2 
        y = leftLoc[1] + (rightLoc[1] - leftLoc[1]) / 2
        s = leftLoc[2] + (rightLoc[2] - leftLoc[2]) / 2
        return (x, y, s)

    def insertInFrontOf(self, frontNode, newNode) :
        frontNode.getFront().setBack(newNode)
        newNode.setFront(frontNode.getFront())
        frontNode.setFront(newNode)
        newNode.setBack(frontNode)
 
    def tracePath(self, t, traceFunc) :
        index = t.getIndex()
        t = traceFunc(t)
        path = []  
        while True :
            path.append(t.getLocation())
            if not(t.isEmpty()) :
                t.setStagedIndex(index)
                return (path)
            t = traceFunc(t)

            
    def rotate(self, direction=1) :
        traceFunc = MenuLocationNode.getFront if direction == 1 else MenuLocationNode.getBack
        t = self.listFront
        circumnavigated = False
        while not(circumnavigated) :
            if not(t.isEmpty()) : # found a location that has an index to an icon
                path =  self.tracePath(t, traceFunc)
                self.scoreboards[t.getIndex()][Carousel.INDEX_ICON].moveTo(path)
            t = t.getFront()
            if t == self.listFront :
                circumnavigated = True

        circumnavigated = False
        while not(circumnavigated) :
            t.updateIndex()
            t = t.getFront()
            if t == self.listFront :
                circumnavigated = True


    # after one call to initialize, just use the move functions
    def initialize(self) :
        t = self.listFront
        circumnavigated = False 
        if not(t is None) :
            while not(circumnavigated) :
                if not(t.isEmpty()) :
                    icon = self.scoreboards[t.getIndex()][Carousel.INDEX_ICON]
                    path = []
                    path.append(t.getLocation())
                    icon.moveTo(path)
                t = t.getFront()
                if t == self.listFront : 
                    circumnavigated = True


    # debugging help
    def printList(self) :
        t = self.listFront
        print ("Start of List")
        while True :
          print(str(t.getIndex()) + " ")
          t = t.getFront()
          if t == self.listFront : break
        print("End of List")

    def getSelection(self) :
        return self.listFront.getIndex()    
 