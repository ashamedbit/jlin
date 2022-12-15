import csv


def clustering_coefficient(file1, file2):
    num_edges = 0
    edges = {}
    num_nodes = 0
    nodes = {}
    country = {}
    university = {}

    with open(file1) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        author_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                num_edges = num_edges + 1
                from_vertex = row[0]
                to_vertex = row[1]
                if from_vertex not in edges:
                    edges[from_vertex] = set()
                edges[from_vertex].add(to_vertex)
                if to_vertex not in edges:
                    edges[to_vertex] = set()
                edges[to_vertex].add(from_vertex)
                line_count += 1

    with open(file2) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        author_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                num_nodes = num_nodes + 1
                author = row[0]
                area = row[3]
                if len(row) >= 5:
                    country[author] = row[4]
                    university[author] = row[5]

                nodes[author] = area
                line_count += 1

    # Area graph
    areas = ['web+ir', 'crypto', 'networks', 'graphics', 'db', 'robotics', 'nlp', 'vision', 'ml', 'se', 'eda', 'comp. bio', 'visualization', 'embedded', 'security', 'hpc', 'ecom', 'logic', 'ai', 'hci', 'os', 'theory', 'pl', 'arch', 'mobile', 'metrics']
    edges_area = {}
    num_edges_area = 0
    for from_vertex in edges.keys():
        for to_vertex in edges[from_vertex]:
            area1 = nodes[from_vertex]
            area2 = nodes[to_vertex]
            if area1 == "Unknown" or area2 == "Unknown":
                continue

            if area1 == area2:
                continue
            if area1 not in edges_area:
                edges_area[area1] = set()
            if area2 not in edges_area:
                edges_area[area2] = set()

            if area2 not in edges_area[area1]:
                edges_area[area1].add(area2)
                edges_area[area2].add(area1)
                num_edges_area = num_edges_area + 1

    # Local clustering coefficient area
    local_clustering_coeffiecient_area = num_edges_area/ ((len(areas) * (len(areas) - 1))/2)


    # Local clustering coefficient
    local_clustering_coeffiecient = num_edges/ ((num_nodes * (num_nodes - 1))/2)

    # Global clustering coefficient area wise
    closed_triplets = 0
    triplets = 0
    for node in edges_area.keys():
        for vertex1 in edges_area[node]:
            for vertex2 in edges_area[node]:
                # Find number of closed triplets
                if vertex1 in edges_area[vertex2]:
                    closed_triplets = closed_triplets + 1
                # Find number of triplets
                if vertex1 != vertex2:
                    triplets = triplets + 1


    # Global clustering coefficient area wise
    if triplets != 0:
        global_clustering_coefficients = closed_triplets / triplets
    else:
        global_clustering_coefficients = 0

    print("The local clustering coefficient is : " + str(local_clustering_coeffiecient))
    print("The local clustering coefficient  area wise is : " + str(local_clustering_coeffiecient_area))
    print("The global clustering coefficient area wise is : " + str(global_clustering_coefficients))

    # Area level analysis
    same_area = 0
    areas = ['web+ir', 'crypto', 'networks', 'graphics', 'db', 'robotics', 'nlp', 'vision', 'ml', 'se', 'eda', 'comp. bio', 'visualization', 'embedded', 'security', 'hpc', 'ecom', 'logic', 'ai', 'hci', 'os', 'theory', 'pl', 'arch', 'mobile', 'metrics']
    area_matrix = [[0 for x in range(len(areas))] for y in range(len(areas))] 
    same_areas_counter = [0] * len(areas)
    diff_areas_counter = [0] *len(areas)

    for from_vertex in edges.keys():
        for to_vertex in edges[from_vertex]:
            if nodes[from_vertex] == nodes[to_vertex]:
                same_area = same_area + 1
                for i, area in enumerate(areas):
                    if area == nodes[from_vertex]:
                        same_areas_counter[i] = same_areas_counter[i] + 1
            else:
                x = 0
                y = 0
                for i, area in enumerate(areas):
                    if area == nodes[from_vertex]:
                        diff_areas_counter[i] = diff_areas_counter[i] + 1
                        x = i
                    if area == nodes[to_vertex]:
                        diff_areas_counter[i] = diff_areas_counter[i] + 1
                        y = i
                area_matrix[x][y] = area_matrix[x][y] + 1
                area_matrix[y][x] = area_matrix[y][x] + 1


    
    print("Ratio of inter cluster edges to intra cluster edges at area level: " + str(same_area/(num_edges*2)))
    print(areas)
    result = []
    for i in range(len(same_areas_counter)):
        if (same_areas_counter[i] != 0) or (diff_areas_counter[i] != 0):
            result.append(diff_areas_counter[i]/ (diff_areas_counter[i] + same_areas_counter[i]))
        else:
            result.append(0)


    print(result)


    # Country level analysis
    if country:
        same_country = 0
        countries = ["us", "canada"]
        same_country_counter = [0] * len(countries)
        diff_country_counter = [0] * len(countries)

        for from_vertex in edges.keys():
            for to_vertex in edges[from_vertex]:
                if country[from_vertex] == country[to_vertex]:
                    same_country = same_country + 1
                    for i, c in enumerate(countries):
                        if c == country[from_vertex]:
                            same_country_counter[i] = same_country_counter[i] + 1
                else:
                    for i, c in enumerate(countries):
                        if c == country[from_vertex]:
                            diff_country_counter[i] = diff_country_counter[i] + 1
                        if c == country[to_vertex]:
                            diff_country_counter[i] = diff_country_counter[i] + 1


        
        print("Ratio of inter cluster edges to intra cluster edges at country level : " + str(same_country/(num_edges*2)))
        print(countries)
        result = []
        print(same_country_counter)
        print(diff_country_counter)
        for i in range(len(same_country_counter)):
            if (same_country_counter[i] != 0) or (diff_country_counter[i] != 0):
                result.append(same_country_counter[i]/ (diff_country_counter[i] + same_country_counter[i]))
            else:
                result.append(0)


        print(result)

        min = 100000000000000000000000
        imin = -1
        jmin = -1
        imax = -1
        jmax = -1
        max = -1
        for i in range(len(areas)):
            for j in range(len(areas)):
                if i != j:
                    if area_matrix[i][j] < min:
                        min = area_matrix[i][j]
                        imin = i
                        jmin = j
                    if area_matrix[i][j] > max:
                        max = area_matrix[i][j]
                        imax = i
                        jmax = j

                    if area_matrix[i][j] == 388:
                        print("Wooohooo")
                        print(areas[i])
                        print(areas[j])
                    
        

        print(area_matrix)
        print("Lowest correlated areas " + areas[imin] + " and " + areas[jmin])
        print("Highest correlated areas " + areas[imax] + " and " + areas[jmax])
        print("Lowest value in area matrix : "+ str(min))
        print("Highest value in area matrix : "+ str(max))

        sankey_source = []
        sankey_target = []
        sankey_flow = []
        uni_map = {}
        for from_vertex in edges.keys():
            for to_vertex in edges[from_vertex]:
                if country[from_vertex] != country[to_vertex]:
                    source_uni = university[from_vertex]
                    target_uni = university[to_vertex]
                    if source_uni == target_uni:
                        print("Helpppppp")
                        continue

                    if country[from_vertex] == "canada":
                        key = source_uni + '_' + target_uni
                    else:
                        key = target_uni + '_' + source_uni

                    if key not in uni_map:
                        uni_map[key] = 1
                    else:
                        uni_map[key] = uni_map[key] + 1
        
        
        for key,value in uni_map.items():
            source_uni = key.split("_")[0]
            target_uni = key.split("_")[1]
            flow = value
            sankey_source.append(source_uni)
            sankey_target.append(target_uni)
            sankey_flow.append(flow)

        us_uni = list(set(sankey_source))
        can_uni = list(set(sankey_target))
        unis = us_uni + can_uni

        for i,uni in enumerate(sankey_source):
            pos = unis.index(uni)
            sankey_source[i] = pos
        
        for i,uni in enumerate(sankey_target):
            pos = unis.index(uni)
            sankey_target[i] = pos


        import plotly.graph_objects as go
        import plotly.express as px

        fig = go.Figure(data=[go.Sankey(
            node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = unis,
            color = [
                px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i,uni in enumerate(unis)
            ],
            ),
            link = dict(
            source = sankey_source, # indices correspond to labels, eg A1, A2, A1, B1, ...
            target = sankey_target,
            value = sankey_flow,
            color = [
                px.colors.qualitative.Plotly[int(pos) % len(px.colors.qualitative.Plotly)]
                for i,pos in enumerate(sankey_source)
            ],
        ))])

        fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
        fig.show()



    