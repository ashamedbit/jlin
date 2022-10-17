import csv

links = []
professors = {}
professor_area = {}
limit = 200

year_limit = 2015

with open('googlescholar.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    author_count = 1
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count += 1
            link = row[3]
            if "google" in link:
                links += [link]
            else:
                continue
            name = row[4]
            name = name.strip()
            nameparts = row[4].split(" ")
            citename = nameparts[0][0] + " " + nameparts[-1]
            professors[citename] = name

            areas = row[5]
            if areas.strip() !=  '':
                area = areas.split(',')[0]
                professor_area[citename] = area
            author_count = author_count + 1

professors['MW Godfrey'] = 'Michael W. Godfrey'
professor_area['MW Godfrey'] = 'se'
professor_area['J Watrous'] = 'quantum'

professor_area['D Rayside'] = 'se'
professor_area['P Lam'] = 'se'
professor_area['A Lubiw'] = 'theory'
professor_area['W Dietl'] = 'se'
professor_area['N A. Day'] = 'theory'
professor_area['P Beek'] = 'ai'

professor_area['T Brown'] = 'se'

professor_area['R Boutaba'] = 'networks'





authors = {}
authors_index = {}



with open('fullgooglescholar.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    author_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            author_list = row[2]
            title = row[3]
            conference = row[4]
            citations = row[5]
            year = row[6]

            #if (year.strip() == '') or int(year.strip()) >= year_limit:
            #    continue

            list = author_list.split(',')
            for author in list:
                if "..." in author:
                    continue
                author = author.strip()
                if author not in authors:
                    authors[author] = author_count
                    authors_index[author_count] = author
                    author_count = author_count + 1
            line_count += 1

print(author_count) 
matrix = [[0 for x in range(len(authors)+1)] for y in range(len(authors)+1)] 



with open('fullgooglescholar.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            author_list = row[2]
            title = row[3]
            conference = row[4]
            citations = row[5]
            year = row[6]
         
            #if (year.strip() == '') or int(year.strip()) >= year_limit:
            #    continue
            
            list = author_list.split(',')

            for i,author in enumerate(list):
                if "..." in author:
                    list.pop(i)
            
            num_authors = len(list)
            citations = citations.strip().replace('*','')
            credit = 0
            if citations == "":
                citations = 0
            if num_authors != 0:
                credit = int(citations)/num_authors
            else:
                line_count += 1
                continue

            for a in list:
                a = a.strip()
                a_index = authors[a]
                for b in list:
                    b = b.strip()
                    b_index = authors[b]
                    if a != b:
                        matrix[a_index][b_index] =  matrix[a_index][b_index] + credit
                        matrix[b_index][a_index] =  matrix[b_index][a_index] + credit
               
            line_count += 1
            


auth_citation = {}
for i in range(len(authors)):
    author1 = authors_index[i]

    if author1 not in auth_citation:
        auth_citation[author1] = 0

    for j in range(len(authors)):
        author2 = authors_index[j]
        
        if author2 not in auth_citation:
            auth_citation[author2] = 0
        if i < j:
            if matrix[i][j] != 0:
                auth_citation[author1]  = auth_citation[author1] + matrix[i][j]
                auth_citation[author2]  = auth_citation[author2] + matrix[i][j]
            
        

with open('vis/staticdata/jean-complete-edge.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Source','Target','Type','Id','Label'])
    id = 1
  
    for i in range(len(authors)):
        author1 = authors_index[i]

        if author1 not in auth_citation:
            auth_citation[author1] = 0

        for j in range(len(authors)):
            author2 = authors_index[j]
           
            if author2 not in auth_citation:
                auth_citation[author2] = 0
            if i < j:
                if matrix[i][j] != 0:
                    if auth_citation[author1] >= limit and auth_citation[author2] >= limit:
                        csv_out.writerow([author1, author2, "Undirected", str(id), matrix[i][j]])

                    id = id + 1


finalists = []
with open('vis/staticdata/jean-complete-node.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Id','Label','Description','Area'])

    for i, (author, matrix_row) in enumerate(authors.items()):
        if auth_citation[author] >= limit:
           
            if author in professors:
                name_parts = professors[author].split(' ')
                
                if author in professor_area:
                    csv_out.writerow([author, professors[author], auth_citation[author],professor_area[author]])
                else:
                    csv_out.writerow([author, professors[author], auth_citation[author],"Unknown"])
                    finalists += [author]
            else:
                csv_out.writerow([author, author, auth_citation[author],"Unknown"])

print(finalists)