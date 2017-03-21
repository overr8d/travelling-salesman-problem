from pyevolve import G1DList, GAllele
from pyevolve import GSimpleGA
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import Consts
import sys, random
from math import sqrt
from PIL import Image, ImageDraw, ImageFont
  
""" Global Variables """
cm     = []
coords = []
CITIES = 50
WIDTH   = 800
HEIGHT  = 600
LAST_SCORE = -1
random.seed(800)


""" Method to store the distances """
def distance_matrix(coords):
   
   matrix={}
   for i,(x1,y1) in enumerate(coords):
      for j,(x2,y2) in enumerate(coords):
         dx, dy = x1-x2, y1-y2
         dist=sqrt(dx*dx + dy*dy)
         matrix[i,j] = dist
   return matrix

""" Method to calculate total tour length """
def total_length(matrix, tour):
   
   total = 0
   t = tour.getInternalList()
   for i in range(CITIES):
      j      = (i+1)%CITIES
      total += matrix[t[i], t[j]]
   return total

""" Method to plot the graph and save the file """
def plot_and_save_file(coords, tour, img_file):
   
   padding=20
   coords=[(x+padding,y+padding) for (x,y) in coords]
   maxx,maxy=0,0
   for x,y in coords:
      maxx, maxy = max(x,maxx), max(y,maxy)
   maxx+=padding
   maxy+=padding
   img=Image.new("RGB",(int(maxx),int(maxy)),color=(255,255,255))
   font=ImageFont.load_default()
   d=ImageDraw.Draw(img);
   num_cities=len(tour)
   for i in range(num_cities):
      j=(i+1)%num_cities
      city_i=tour[i]
      city_j=tour[j]
      x1,y1=coords[city_i]
      x2,y2=coords[city_j]
      d.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
      d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))
   for x,y in coords:
      x,y=int(x),int(y)
      d.ellipse((x-5,y-5,x+5,y+5),outline=(0,0,0),fill=(196,196,196))
   del d
   img.save(img_file, "PNG")
   print "The plot was saved into the file." 

""" Method to initialize TSP """
def TSP_Init(genome, **args):
   
   lst = [i for i in xrange(genome.getListSize())]
   random.shuffle(lst)
   genome.setInternalList(lst)


def main_run():
   global cm, coords, WIDTH, HEIGHT

   coords = [(random.randint(0, WIDTH), random.randint(0, HEIGHT))
                 for i in xrange(CITIES)]
   cm     = distance_matrix(coords)
   genome = G1DList.G1DList(len(coords))

   genome.evaluator.set(lambda chromosome: total_length(cm, chromosome))
   """ Set different crossover methods in order to observe different fitness results """
   genome.crossover.set(Crossovers.G1DListCrossoverUniform)
   genome.initializator.set(TSP_Init)

   
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(2000)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.02)
   """ Set different population sizes in order to observe different fitness results """
   ga.setPopulationSize(40)

   ga.evolve(freq_stats=500)
   best = ga.bestIndividual()

   plot_and_save_file(coords, best, "tsp.png")
   
"""if a module is being run directly"""
if __name__ == "__main__":
   main_run()
