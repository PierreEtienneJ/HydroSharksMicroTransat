They are two different algorithms,
They are inspired by the living, by genetic. 


The first Ga : ga1.0 use evolution with mutation or mean between too waypoints, the optimization is in 2D.
The second Ga : ga2.0 use reproduction with mutation and genetic crossbreeding, the optimization is in 1D.

Use works only with evolutive algorithms, because they can return one resultat if we need once, even if it's not the best way. 

ga1.0 : 
They you can run him allown. 
You need to create a Ga object, the constructor need a point of departure and a door of arrival, and a deviation from the road. 
After that, you need to call the method 'fctgeneration'. It takes in parameters the number of waypoints, the number of cells, 
the number of generation, the evolution method and the selection method.
You can plot with the method 'affiche'.

ga2.0 :
You need the folder 'map.py'. 
Firstly, I you want, you have to edit the object 'StopGa', to creat an end-of-generation parameter.
After that, you need to create a StopGa object  with the parameters you have modified.
You need to creat a Ga object with five parameters :  the location of the boat, the starting point of the route, the end gate, the width of the route, the StopGa.
With the setRun method you choose the generation parameters: number of cells, number of generation, evolution method, selection method, type of cost function. 

Next, start the two thread with the method start and after, join. 
You can save the road with 'save' and plot with the method 'plot'. 

