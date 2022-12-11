import csv


def clustering_coefficient(file1, file2):
    num_edges = 0
    edges = {}
    num_nodes = 0
    nodes = {}
    country = {}

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
                if len(row) == 5:
                    country[author] = row[4]
                nodes[author] = area
                line_count += 1
    
    # Local clustering coefficient
    local_clustering_coeffiecient = num_edges/ ((num_nodes * (num_nodes - 1))/2)

    # Global clustering coefficient
    closed_triplets = 0
    triplets = 0
    for node in edges.keys():
        for vertex1 in edges[node]:
            for vertex2 in edges[node]:
                # Find number of closed triplets
                if vertex1 in edges[vertex2]:
                    closed_triplets = closed_triplets + 1
                # Find number of triplets
                if vertex1 != vertex2:
                    triplets = triplets + 1


    # Global clustering coefficient
    global_clustering_coefficients = closed_triplets / triplets

    print("The local clustering coefficient is : " + str(local_clustering_coeffiecient))
    print("The global clustering coefficient is : " + str(global_clustering_coefficients))

    # Area level analysis
    same_area = 0
    areas = ['web+ir', 'crypto', 'networks', 'graphics', 'db', 'robotics', 'nlp', 'vision', 'ml', 'se', 'eda', 'comp. bio', 'visualization', 'embedded', 'security', 'hpc', 'ecom', 'logic', 'ai', 'hci', 'os', 'theory', 'pl', 'arch', 'mobile', 'metrics']
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
                for i, area in enumerate(areas):
                    if area == nodes[from_vertex]:
                        diff_areas_counter[i] = diff_areas_counter[i] + 1
                    if area == nodes[to_vertex]:
                        diff_areas_counter[i] = diff_areas_counter[i] + 1


    
    print("Ratio of inter cluster edges to intra cluster edges at area level: " + str(same_area/(num_edges*2)))
    print(areas)
    result = []
    for i in range(len(same_areas_counter)):
        if (same_areas_counter[i] != 0) or (diff_areas_counter[i] != 0):
            result.append(same_areas_counter[i]/ (diff_areas_counter[i] + same_areas_counter[i]))
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



    

                