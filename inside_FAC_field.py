import pyglet
from fac_set import FACSet

class InsideFACField() :
    F_BLUE = (0, 255, 255)
    F_YELLOW = (255,255,150)
    F_GRAY = (180,180,180)
    F_WHITE = (240,240,240)
    F_GREEN = (102, 255, 102)
    
    B_BLACK = (0,0,0)


    FONT_SIZE = 18
    FONT_COLOR = (0, 0, 0, 255)
    FONT_RED  = (255,0,0, 255)
    LINE_SPACING = 10

    def __init__(self, font_size, bgColor, width, height, text='', bold=False,
                              batch=None, fgGroup = None, bgGroup = None) :
        self.border = pyglet.shapes.BorderedRectangle(0, 0, width, height, color = bgColor, border_color=InsideFACField.B_BLACK,
                                                        batch = batch, group = bgGroup)
        self.doc = pyglet.text.document.FormattedDocument(text)

        self.doc.set_style(0, len(self.doc.text), dict(color=InsideFACField.FONT_COLOR,
                                                       font_size=font_size,
                                                       font_name=FACSet.TEXT_FONT,
                                                       align='center',
                                                       bold=bold,
                                                       line_spacing=font_size+InsideFACField.LINE_SPACING))
        self.layout = pyglet.text.layout.TextLayout(self.doc, multiline=True, width=width, batch=batch, group=fgGroup)
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'bottom'

    def setPosition(self, left, bottom) :
        self.left = left
        self.bottom = bottom
        self.border.position = (left, bottom)

        #center layout in border
        x = left #+ (self.border.width - self.layout.content_width) / 2
        y = bottom +  (self.border.height - self.layout.content_height + InsideFACField.LINE_SPACING) // 2
        self.layout.position = (x, y,0)

    #replace all >= or <= in document text with underlined > or underline <
    def replaceComparators(self, comparator) :
       while (True) :
            pos = self.doc.text.find(comparator)
            if pos > 0  :
                self.doc.delete_text(pos+1, pos+2)
                self.doc.set_style(pos, pos+1, dict(baseline=1, underline=InsideFACField.FONT_COLOR))
            else :
                break


    def setText(self, text) :
        # change <= and >=
        self.doc.text = text
        self.replaceComparators('<=')
        self.replaceComparators('>=')
        self.setPosition(self.left, self.bottom)

    def setFont(self, fontName, fontColor, fontSize) :
        self.doc.set_style(0, len(self.doc.text), dict(color=fontColor,
                                                       font_size=fontSize,
                                                       font_name=fontName))

    def setBaseline(self, b) :
        self.doc.set_style(0, len(self.doc.text), dict(baseline=b))    
    
