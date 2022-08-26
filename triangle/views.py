from django.shortcuts import render
from tkinter import *
import math

# Create your views here.
def button(request):
    return render(request, 'triangle_circle_calculator.html')

def tricle(request):
    main()
    return render(request, 'triangle_circle_calculator.html')

def main():
    # display window specifications
    window = Tk()
    window.geometry("800x800")
    window.title("SHREE")
    window.configure(background = "black")
    
    # labels of input sides
    label_1 = Label(window, text = "Enter the 1st side:", fg = "blue", bg = "black", font = ("Arial", 14))
    label_1.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 10)
    label_2 = Label(window, text = "Enter the 2nd side:", fg = "blue", bg = "black", font = ("Arial", 14))
    label_2.grid(row = 1, column = 0, sticky = W, padx = 5, pady = 10)    
    label_3 = Label(window, text = "Enter the 3rd side:", fg = "blue", bg = "black", font = ("Arial", 14))
    label_3.grid(row = 2, column = 0, sticky = W, padx = 5, pady = 10) 
    
    # defining sides of the triangle
    s_1 = DoubleVar()
    s_2 = DoubleVar()
    s_3 = DoubleVar()
    
    # data entry
    te_side1 = Entry(window, textvariable = s_1, fg = "black", bg = "white", font = ("Arial", 14))
    te_side1.grid(row = 0, column = 1, sticky = W)
    te_side2 = Entry(window, textvariable = s_2, fg = "black", bg = "white", font = ("Arial", 14))
    te_side2.grid(row = 1, column = 1, sticky = W)
    te_side3 = Entry(window, textvariable = s_3, fg = "black", bg = "white", font = ("Arial", 14))
    te_side3.grid(row = 2, column = 1, sticky = W)  
    
    #Set the Menu initially
    menu= StringVar()
    menu.set("Select one of the Circles")
    
    #Create a dropdown Menu
    drop= OptionMenu(window, menu,"Select one of the Circles", "Incircle", "Circumcircle", "Orthocircle", "Nine-point Circle", "Excircles")
    drop.grid(row = 3, column = 0, sticky = W, pady = 10)    
    
    # calculate button
    button = Button(window, command = lambda: calculate(window, s_1.get(), s_2.get(), s_3.get(), menu.get()),text = "Calculate", fg = "black", bg = "white", font = ("Arial", 14))
    button.grid(row = 3, column = 1, pady = 10)
    
    window.mainloop()

    
   
def calculate(window, x, y, z, circle):
    # check if user entries are valid
    if (type(x) != float or type(y) != float or type(z) != float or (x <= 0) or (y <= 0) or (z <= 0) or (x+y < z) or (y+z < x) or (z+x < y)):
        error_label = Label(window, text = "Invalid Input! Please enter the sides again.", fg = "blue", bg = "black", font = ("Arial", 14))
        error_label.grid(row = 5, column = 1, sticky = W, pady = 10)
    else:
        # define Canavas object to draw necessary shapes
        can = Canvas(window, width = 350, height = 350, bg = "white")
        can.grid(row = 7, column = 1, sticky = W)
        
        draw = draw_circles(window, can, x, y, z)
        
        draw.draw_triangle()
        if circle == "Incircle":
            draw.draw_incircle()        
        elif circle == "Circumcircle":
            draw.draw_circumcirle()
        elif circle == "Orthocircle":
            draw.draw_orthocircle()
        elif circle == "Nine-point Circle":
            draw.draw_nine_pt_circle()
        elif circle == "Excircles":
            draw.draw_excircles()
        elif circle == "Select one of the Circles":
            draw.draw_triangle()


class draw_circles:
    def __init__(self, window, canvas, x, y, z):
        self.window = window
        self.canvas = canvas
        self.x= x
        self.y = y
        self.z = z
        
        self._coordinates = self.coordinates(self.x, self.y, self.z)
        self.x1 = self._coordinates[0]
        self.y1 = self._coordinates[1]
        self.x2 = self._coordinates[2]
        self.y2 = self._coordinates[3]
        self.x3 = self._coordinates[4]
        self.y3 = self._coordinates[5]          
        
        self._area = self.area(self.x, self.y, self.z)
        self._semiperimeter = self.semiperimeter(self.x, self.y, self.z)
        self.ir = self.inradius()
        self.cr = self.circumradius()
        self.ortho = self.ortho_r_and_c()
        self.ortho_r = self.ortho[0]    
        self.nr = self.cr / 2
        self.exradii = self.exradius()
        
        angle = self.angles(self.x, self.y, self.z)
        # X, Y, Z are angles opposite to x, y and z
        self.X = angle[0] 
        self.Y = angle[1]
        self.Z = angle[2]        
        
        self.d_label = Label(self.window, text = "", fg = "blue", bg = "black", font = ("Arial", 14))
        self.ir_label = Label(self.window, text = "", fg = "blue", bg = "black", font = ("Arial", 14))
        self.cr_label = Label(self.window, text = "", fg = "blue", bg = "black", font = ("Arial", 14))
        self.or_label = Label(self.window, text = "", fg = "blue", bg = "black", font = ("Arial", 14))
        self.nr_label = Label(self.window, text = "", fg = "blue", bg = "black", font = ("Arial", 14))
        self.er_label = Label(self.window, text = "", fg = "blue", bg = "black", font = ("Arial", 14))
        
        
    def semiperimeter(self, x, y, z):
        return (x + y + z) / 2        
        
    def area(self, x, y, z):
        s = (x + y + z) / 2
        area_sq = s*(s - x)*(s - y)*(s - z)
        area = math.sqrt(area_sq)
        return area     
    
    def coordinates(self, x, y, z):
        x_1 = 100
        y_1 = 200
        x_2 = x_1 + x
        y_2 = y_1
        
        cos_theta = ((x*x) + (y*y) - (z*z)) / (2*x*y)
        theta = math.acos(cos_theta)
        
        x_3 = x_1 + x - (y*math.cos(theta))
        y_3 = y_1 - (y*math.sin(theta))   
        
        return [x_1, y_1, x_2, y_2, x_3, y_3]    
        
        
    def angles(self, x, y, z):
        # alpha, beta, gamma oppsite angles to x, y and z respectively
        cos_alpha = ((y*y) + (z*z) - (x*x)) / (2*y*z)
        alpha = math.acos(cos_alpha)
        
        cos_beta = ((x*x) + (z*z) - (y*y)) / (2*x*z)
        beta = math.acos(cos_beta)
        
        cos_gamma = ((x*x) + (y*y) - (z*z)) / (2*x*y)
        gamma = math.acos(cos_gamma)    
        
        return [alpha, beta, gamma]    
    
    
    def draw_triangle(self):
        self.canvas.create_polygon(self._coordinates, fill = "white", outline = "green")    
        
    def create_circle(self, canvas, x, y, r):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas.create_oval(x0, y0, x1, y1, outline = "red")    
    
    def inradius(self):
        return self._area/self._semiperimeter
    
    def circumradius(self):
        return (self.x * self.y * self.z) / (4 * self._area)
    
    def exradius(self):
        r1 = self._area/(self._semiperimeter - self.x)
        r2 = self._area/(self._semiperimeter - self.y)
        r3 = self._area/(self._semiperimeter - self.z)
        
        return [r1, r2, r3]
    
    def draw_incircle(self):
        self.destroy_labels()
        
        p = 2*self._semiperimeter # p is the perimeter of the triangle
        
        # calculating co-ordinates of incentre
        ix = ((self.x1*self.y) + (self.x2*self.z) + (self.x3*self.x)) / p
        iy = ((self.y1*self.y) + (self.y2*self.z) + (self.y3*self.x)) / p     
        
        self.ir_label = Label(self.window, text = "Inradius of the triangle: " + str(round(self.ir, 4)), fg = "blue", bg = "black", font = ("Arial", 14))
        self.ir_label.grid(row = 5, column = 1, sticky = W, pady = 10)     
        
        # drawing the incircle 
        self.create_circle(self.canvas, ix, iy, self.ir)  
        self.canvas.create_polygon([self.x1, self.y1, ix, iy], fill = "white", outline = "red")
        self.canvas.create_polygon([self.x2, self.y2, ix, iy], fill = "white", outline = "red")
        self.canvas.create_polygon([self.x3, self.y3, ix, iy], fill = "white", outline = "red")
        
        
    def draw_circumcirle(self):
        self.destroy_labels()
        add_dsin = math.sin(2*self.X) + math.sin(2*self.Y) + math.sin(2*self.Z)
        
        # calculating co-ordinates of circumcentre
        cx = (self.x1*math.sin(2*self.Y) + self.x2*math.sin(2*self.Z) + self.x3*math.sin(2*self.X)) / add_dsin
        cy = (self.y1*math.sin(2*self.Y) + self.y2*math.sin(2*self.Z) + self.y3*math.sin(2*self.X)) / add_dsin
        
        self.cr_label = Label(self.window, text = "Circumradius of the triangle: " + str(round(self.cr, 4)), fg = "blue", bg = "black", font = ("Arial", 14))
        self.cr_label.grid(row = 5, column = 1, sticky = W, pady = 10)
     
        # drawing the circumcircle 
        self.create_circle(self.canvas, cx, cy, self.cr)   
            
        midXx = (self.x1 + self.x2) / 2
        midXy = (self.y1 + self.y2) / 2
        midYx = (self.x2 + self.x3) / 2
        midYy = (self.y2 + self.y3) / 2
        midZx = (self.x1 + self.x3) / 2
        midZy = (self.y1 + self.y3) / 2     
        
        self.canvas.create_polygon([midXx, midXy, cx, cy], fill = "white", outline = "red")
        self.canvas.create_polygon([midYx, midYy, cx, cy], fill = "white", outline = "red")
        self.canvas.create_polygon([midZx, midZy, cx, cy], fill = "white", outline = "red")
        
    
    def ortho_r_and_c(self):
        ox = self.x3
        oy = self.y2 + (self.x1 - self.x3)*(self.x3 - self.x2) / (self.y3 - self.y1)
        
        midXx = (self.x1 + self.x2) / 2
        midXy = (self.y1 + self.y2) / 2
        midYx = (self.x2 + self.x3) / 2
        midYy = (self.y2 + self.y3) / 2
        midZx = (self.x1 + self.x3) / 2
        midZy = (self.y1 + self.y3) / 2 
        
        eoXx = 2*midXx - self.x3
        eoXy = 2*midXy - self.y3
        eoYx = 2*midYx - self.x1
        eoYy = 2*midYy - self.y1
        eoZx = 2*midZx - self.x2
        eoZy = 2*midZy - self.y2        
        
        ortho_r = math.sqrt((eoXx-ox)*(eoXx-ox) + (eoXy-oy)*(eoXy-oy))
        
        return [ortho_r, ox, oy, eoXx, eoXy, eoYx, eoYy, eoZx, eoZy]
        
    
    def draw_orthocircle(self):
        self.destroy_labels()
        
        dot_l1 = self.ortho[3], self.ortho[4], self.ortho[5], self.ortho[6]
        dot_l2 = self.ortho[5], self.ortho[6], self.ortho[7], self.ortho[8]
        dot_l3 = self.ortho[7], self.ortho[8], self.ortho[3], self.ortho[4]
        
        ortho_r = self.ortho[0]
        ox = self.ortho[1]
        oy = self.ortho[2]
        
        pXx = self.x1 + (self.z*math.cos(self.Y))
        pXy = self.y1
        
        pYx = self.x1 - (self.y3-self.y2)*(((self.y3-self.y2)*self.x1 + (self.x2-self.x3)*self.y1 + self.x3*(self.y2-self.y3) + self.y3*(self.x3-self.x2)) / ((self.y3-self.y2)*(self.y3-self.y2) + (self.x2-self.x3)*(self.x2-self.x3)))
        pYy = self.y1 - (self.x2-self.x3)*(((self.y3-self.y2)*self.x1 + (self.x2-self.x3)*self.y1 + self.x3*(self.y2-self.y3) + self.y3*(self.x3-self.x2)) / ((self.y3-self.y2)*(self.y3-self.y2) + (self.x2-self.x3)*(self.x2-self.x3)))        
        
        pZx = self.x2 - (self.y3-self.y1)*(((self.y3-self.y1)*self.x2 + (self.x1-self.x3)*self.y2 + self.x3*(self.y1-self.y3) + self.y3*(self.x3-self.x1)) / ((self.y3-self.y1)*(self.y3-self.y1) + (self.x1-self.x3)*(self.x1-self.x3)))
        pZy = self.y2 - (self.x1-self.x3)*(((self.y3-self.y1)*self.x2 + (self.x1-self.x3)*self.y2 + self.x3*(self.y1-self.y3) + self.y3*(self.x3-self.x1)) / ((self.y3-self.y1)*(self.y3-self.y1) + (self.x1-self.x3)*(self.x1-self.x3)))
        
        self.or_label = Label(self.window, text = "Orthoradius of the triangle: " + str(round(self.ortho_r, 4)), fg = "blue", bg = "black", font = ("Arial", 14))
        self.or_label.grid(row = 5, column = 1, sticky = W, pady = 10)          
        
        self.create_circle(self.canvas, ox, oy, ortho_r)  
        
        self.canvas.create_polygon([self.x3, self.y3, pXx, pXy], fill = "white", outline = "red")
        self.canvas.create_polygon([self.x1, self.y1, pYx, pYy], fill = "white", outline = "red")
        self.canvas.create_polygon([self.x2, self.y2, pZx, pZy], fill = "white", outline = "red")         
        
        if (self.X > 1.57):
            self.canvas.create_line(self.x3, self.y3, pYx, pYy, dash=(5,1), fill = "green")
            self.canvas.create_line(self.x3, self.y3, pZx, pZy, dash=(5,1), fill = "green")
            
            self.canvas.create_line(self.x3, self.y3, ox, oy, dash=(4,1), fill = "red")
            self.canvas.create_line(pYx, pYy, ox, oy, dash=(4,1), fill = "red")
            self.canvas.create_line(pZx, pZy, ox, oy, dash=(4,1), fill = "red")       
        elif (self.Y > 1.57):
            self.canvas.create_line(self.x1, self.y1, pXx, pXy, dash=(5,1), fill = "green")
            self.canvas.create_line(self.x1, self.y1, pZx, pZy, dash=(5,1), fill = "green")
            
            self.canvas.create_line(self.x1, self.y1, ox, oy, dash=(4,1), fill = "red")
            self.canvas.create_line(pXx, pXy, ox, oy, dash=(4,1), fill = "red")
            self.canvas.create_line(pZx, pZy, ox, oy, dash=(4,1), fill = "red")  
        elif (self.Z > 1.57):
            self.canvas.create_line(self.x2, self.y2, pXx, pXy, dash=(5,1), fill = "green")
            self.canvas.create_line(self.x2, self.y2, pYx, pYy, dash=(5,1), fill = "green")
            
            self.canvas.create_line(self.x2, self.y2, ox, oy, dash=(4,1), fill = "red")
            self.canvas.create_line(pXx, pXy, ox, oy, dash=(4,1), fill = "red")
            self.canvas.create_line(pYx, pYy, ox, oy, dash=(4,1), fill = "red")        
        else:
            self.canvas.create_polygon([self.x3, self.y3, pXx, pXy], fill = "white", outline = "red")
            self.canvas.create_polygon([self.x1, self.y1, pYx, pYy], fill = "white", outline = "red")
            self.canvas.create_polygon([self.x2, self.y2, pZx, pZy], fill = "white", outline = "red")
        
        self.canvas.create_polygon([ox, oy], fill = "white", outline = "red")
        self.canvas.create_line(dot_l1, dash=(4,1))
        self.canvas.create_line(dot_l2, dash=(4,1))
        self.canvas.create_line(dot_l3, dash=(4,1))        
    
    
    def draw_nine_pt_circle(self):
        self.destroy_labels()
        
        ox = self.ortho[1]
        oy = self.ortho[2]
        
        add_dsin = math.sin(2*self.X) + math.sin(2*self.Y) + math.sin(2*self.Z)
        
        # calculating co-ordinates of circumcentre
        cx = (self.x1*math.sin(2*self.Y) + self.x2*math.sin(2*self.Z) + self.x3*math.sin(2*self.X)) / add_dsin
        cy = (self.y1*math.sin(2*self.Y) + self.y2*math.sin(2*self.Z) + self.y3*math.sin(2*self.X)) / add_dsin
        
        nx = (ox + cx) / 2
        ny = (oy + cy) / 2
        
        self.nr_label = Label(self.window, text = "Nine-point Circle radius: " + str(round(self.nr, 4)), fg = "blue", bg = "black", font = ("Arial", 14))
        self.nr_label.grid(row = 5, column = 1, sticky = W, pady = 10)          
        
        self.create_circle(self.canvas, nx, ny, self.nr)
        
        pt1x = self.x1 + (self.z*math.cos(self.Y))
        pt1y = self.y1
        
        pt2x = self.x1 - (self.y3-self.y2)*(((self.y3-self.y2)*self.x1 + (self.x2-self.x3)*self.y1 + self.x3*(self.y2-self.y3) + self.y3*(self.x3-self.x2)) / ((self.y3-self.y2)*(self.y3-self.y2) + (self.x2-self.x3)*(self.x2-self.x3)))
        pt2y = self.y1 - (self.x2-self.x3)*(((self.y3-self.y2)*self.x1 + (self.x2-self.x3)*self.y1 + self.x3*(self.y2-self.y3) + self.y3*(self.x3-self.x2)) / ((self.y3-self.y2)*(self.y3-self.y2) + (self.x2-self.x3)*(self.x2-self.x3)))        
        
        pt3x = self.x2 - (self.y3-self.y1)*(((self.y3-self.y1)*self.x2 + (self.x1-self.x3)*self.y2 + self.x3*(self.y1-self.y3) + self.y3*(self.x3-self.x1)) / ((self.y3-self.y1)*(self.y3-self.y1) + (self.x1-self.x3)*(self.x1-self.x3)))
        pt3y = self.y2 - (self.x1-self.x3)*(((self.y3-self.y1)*self.x2 + (self.x1-self.x3)*self.y2 + self.x3*(self.y1-self.y3) + self.y3*(self.x3-self.x1)) / ((self.y3-self.y1)*(self.y3-self.y1) + (self.x1-self.x3)*(self.x1-self.x3)))        
        
        self.canvas.create_polygon([self.x3, self.y3, pt1x, pt1y], fill = "white", outline = "red")
        self.canvas.create_polygon([self.x1, self.y1, pt2x, pt2y], fill = "white", outline = "red")
        self.canvas.create_polygon([self.x2, self.y2, pt3x, pt3y], fill = "white", outline = "red")        
        
        pt4x = (self.x1 + self.x2) / 2
        pt4y = (self.y1 + self.y2) / 2
        pt5x = (self.x2 + self.x3) / 2
        pt5y = (self.y2 + self.y3) / 2
        pt6x = (self.x1 + self.x3) / 2
        pt6y = (self.y1 + self.y3) / 2 
        
        self.canvas.create_polygon([self.x3, self.y3, pt4x, pt4y], fill = "white", outline = "red")
        self.canvas.create_polygon([self.x1, self.y1, pt5x, pt5y], fill = "white", outline = "red")
        self.canvas.create_polygon([self.x2, self.y2, pt6x, pt6y], fill = "white", outline = "red") 
        
        pt7x = (self.x1 + ox) / 2
        pt7y = (self.y1 + oy) / 2
        pt8x = (self.x2 + ox) / 2
        pt8y = (self.y2 + oy) / 2
        pt9x = (self.x3 + ox) / 2
        pt9y = (self.y3 + oy) / 2         
        
        self.canvas.create_polygon([pt1x, pt1y], fill = "white", outline = "blue")
        self.canvas.create_polygon([pt2x, pt2y], fill = "white", outline = "blue")
        self.canvas.create_polygon([pt3x, pt3y], fill = "white", outline = "blue")
        self.canvas.create_polygon([pt4x, pt4y], fill = "white", outline = "blue")
        self.canvas.create_polygon([pt5x, pt5y], fill = "white", outline = "blue")
        self.canvas.create_polygon([pt6x, pt6y], fill = "white", outline = "blue")
        self.canvas.create_polygon([pt7x, pt7y], fill = "white", outline = "blue")
        self.canvas.create_polygon([pt8x, pt8y], fill = "white", outline = "blue")
        self.canvas.create_polygon([pt9x, pt9y], fill = "white", outline = "blue")
        
        
    def draw_excircles(self):
        self.destroy_labels()
        
        ex1 = ((self.x1*self.y) + (self.x2*self.z) - (self.x3*self.x)) / (-self.x + self.y + self.z)
        ey1 = ((self.y1*self.y) + (self.y2*self.z) - (self.y3*self.x)) / (-self.x + self.y + self.z)           
        
        ex2 = (-(self.x1*self.y) + (self.x2*self.z) + (self.x3*self.x)) / (self.x - self.y + self.z)
        ey2 = (-(self.y1*self.y) + (self.y2*self.z) + (self.y3*self.x)) / (self.x - self.y + self.z)           

        ex3 = ((self.x1*self.y) - (self.x2*self.z) + (self.x3*self.x)) / (self.x + self.y - self.z)
        ey3 = ((self.y1*self.y) - (self.y2*self.z) + (self.y3*self.x)) / (self.x + self.y - self.z)     
        
        r1 = self.exradii[0]
        r2 = self.exradii[1]
        r3 = self.exradii[2]
        
        radii = [r1, r2, r3]
        radii.sort()
        
        self.er_label = Label(self.window, text = "Excircles radii: " + str(round(radii[0], 4)) + ", " + str(round(radii[1], 4)) + ", " + str(round(radii[2], 4)), fg = "blue", bg = "black", font = ("Arial", 14))
        self.er_label.grid(row = 5, column = 1, sticky = W, pady = 10)          
        
        
        self.create_circle(self.canvas, ex1, ey1, r1)
        self.create_circle(self.canvas, ex2, ey2, r2)
        self.create_circle(self.canvas, ex3, ey3, r3)
        
        
    def destroy_labels(self):
        self.d_label = Label(self.window, text = " " * 100, fg = "blue", bg = "black", font = ("Arial", 14))
        self.d_label.grid(row = 5, column = 1, sticky = W, pady = 10)
