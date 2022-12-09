#Development setup

install NodeJS: https://nodejs.org

#Running the code
1. cd vis/
2. npm install
3. npm start

It should start a local web server at http://localhost:8000/

Any further modification of the code will trigger Webpack to recompile

Tested on NodeJS 12.16.2 and NPM 6.14.4

The project visualizes research collaborations between 20 top US universities and 10 top Canadian universities. Each professor in these universities are labelled according to area which they belong. Inter disciplinary research collaborations can be visualized by this tool.

The aim of this project is to investigate the 'silo effect' where-in each discipline of computer science behaves like a silo with effectively no interdisciplinary collaboration. We find this to be visually true however the effect decreases as the ranking of university also increases (with more interdisciplinary research

References:
1. https://github.com/d3/d3-transition
2. https://observablehq.com/@d3/force-directed-graph
3. https://livebook.manning.com/book/d3-js-in-action/chapter-6/18
4. https://d3-graph-gallery.com/graph/interactivity_button.html
