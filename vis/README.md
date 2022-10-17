#Development setup

install NodeJS: https://nodejs.org

#Running the code
1. cd vis/
2. npm install
3. npm start

It should start a local web server at http://localhost:8000/

Any further modification of the code will trigger Webpack to recompile

Tested on NodeJS 12.16.2 and NPM 6.14.4

The data used is about the network of characters in Victor Hugo's book Les Miserables first encoded by Professor Donald Knuth. The adjacency matrix and graph network are available to be seen for this network. If there is an interaction between two characters then there exists an edge between them . The adjacency matrix has an x axis and y axis which both contain all the characters in the novel. An edge is encoded as (source, target) where both source and target are character Ids. A black square is highlighted in row of character1 and column of character2 in the adjacency matrix if there exists an edge (character1,character2). Hovering on the black square describes the edge under consideration. The dropdown on top of canvas is used to toggle display to the network. The network is displayed on center of canvas. Here each node is represented as a circle and edges as lines. Hovering on each circle describes the character in more detail.

Observations:

Jean Valjean seems to be a central character in the story. This fact can be clearly seen in both adjacency matrix through a strong line on that column and row.
      
      Gavroche,Marius, Thena and Javert are also other major characters (less important than Jean Valjean) connected to several characters. However this is more clearly seen in the network than in the adjacency matrix.
      It appears like there are 7-8 communities (clusters) involved in the story. Perhaps they can be grouped and colored together. Perhaps the size of each cluster
      would show the importance of each group of characters in the development of the story. However still certain characters like Jean Valjean seem to 
      be common across these clusters, joining the plot together. 


References:
1. https://github.com/d3/d3-transition
2. https://observablehq.com/@d3/force-directed-graph
3. https://livebook.manning.com/book/d3-js-in-action/chapter-6/18
4. https://d3-graph-gallery.com/graph/interactivity_button.html