import collections
import csv
import os
import numpy as np
from calculatemetrics import clustering_coefficient



authors = {}
authors_index = {}
matrix = collections.defaultdict(dict)
auth_citation = {}
country = {}
list_of_files = []

file_prefix = "./staticdata/jean-complete-"


with open('./collected/jlinfinal.csv') as csv_file:
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

print("Total number of collaboration authors is : " + str(author_count))

with open('./collected/jlinfinal.csv') as csv_file:
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
                        if a_index in matrix and (b_index in matrix[a_index]):
                            matrix[a_index][b_index] =  matrix[a_index][b_index] + credit
                        else:
                            matrix[a_index][b_index] =  credit

                        if b_index in matrix and (a_index in matrix[b_index]):
                            matrix[b_index][a_index] =  matrix[b_index][a_index] + credit
                        else:
                            matrix[b_index][a_index] = credit
            
            line_count += 1
            

print("Finished populating citation matrix!")

for i in matrix.keys():
    author1 = authors_index[i]

    if author1 not in auth_citation:
        auth_citation[author1] = 0

    for j in matrix[i].keys():
        author2 = authors_index[j]
        
        if author2 not in auth_citation:
            auth_citation[author2] = 0
        if i < j:
            auth_citation[author1]  = auth_citation[author1] + matrix[i][j]
            auth_citation[author2]  = auth_citation[author2] + matrix[i][j]
            
print("Finished populating citations for each author")    



# For overall analysis
professors_all = {}
professor_area_all = {}
country = {}
uni_country = ""

rootdir = './data'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        list_of_files.append(file)
        links = []
        professors = {}
        professor_area = {}
        limit = 0
        path = os.path.join(subdir, file)

        if "us" in subdir:
            file_prefix_with_country = file_prefix + "us-"
            uni_country = "us"
        elif "canada" in subdir:
            file_prefix_with_country = file_prefix + "canada-"
            uni_country = "canada"

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    #print(f'Column names are {", ".join(row)}')
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
                    professors_all[citename] = name
                    country[citename] = uni_country

                    areas = row[5]
                    if areas.strip() !=  '':
                        area = areas.split(',')[0]
                        professor_area[citename] = area
                        professor_area_all[citename] = area

        if "lock" in file:
            continue
        
        print("\n")
        print("University is : " + file)
        print("The number of professors in this university : "+ str(len(professors)))

        # professors['MW Godfrey'] = 'Michael W. Godfrey'
        # professor_area['MW Godfrey'] = 'se'
        # professor_area['J Watrous'] = 'quantum'
        # professor_area['D Rayside'] = 'se'
        # professor_area['P Lam'] = 'se'
        # professor_area['A Lubiw'] = 'theory'
        # professor_area['W Dietl'] = 'se'
        # professor_area['N A. Day'] = 'theory'
        # professor_area['P Beek'] = 'ai'
        # professor_area['T Brown'] = 'se'
        # professor_area['R Boutaba'] = 'networks'

        with open(file_prefix + 'edge-' + file,'w') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['Source','Target','Type','Id','Label'])
            id = 1
        
            for author1 in professors.keys():
                if author1 not in authors:
                    continue

                i = authors[author1]
                if author1 not in auth_citation:
                    auth_citation[author1] = 0

                for author2 in professors.keys():
                    if author2 not in authors:
                        continue

                    j = authors[author2]
                    if author2 not in auth_citation:
                        auth_citation[author2] = 0
                    if i < j and (i in matrix) and (j in matrix[i]):
                        if auth_citation[author1] >= limit and auth_citation[author2] >= limit:
                            csv_out.writerow([author1, author2, "Undirected", str(id), matrix[i][j]])
                        id = id + 1

        print("Finished edge csv")

        with open(file_prefix + 'node-'+ file,'w') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['Id','Label','Description','Area'])

            for i, author in enumerate(professors.keys()):
                if author in auth_citation and auth_citation[author] >= limit:
                    if author in professor_area:
                        csv_out.writerow([author, professors[author], auth_citation[author],professor_area[author]])
                    else:
                        csv_out.writerow([author, professors[author], auth_citation[author], "Unknown"])
                  

        print("Finished node csv")
        clustering_coefficient(file_prefix + 'edge-' + file, file_prefix + 'node-'+ file)


print("\n")
print("##################### Starting complete processing ##################")

with open(file_prefix + 'edge-complete.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Source','Target','Type','Id','Label'])
    id = 1

    for author1 in professors_all.keys():
        if author1 not in authors:
            continue

        i = authors[author1]
        if author1 not in auth_citation:
            auth_citation[author1] = 0

        for author2 in professors_all.keys():
            if author2 not in authors:
                continue

            j = authors[author2]
            if author2 not in auth_citation:
                auth_citation[author2] = 0
            if i < j and (i in matrix) and (j in matrix[i]):
                if auth_citation[author1] >= limit and auth_citation[author2] >= limit:
                    csv_out.writerow([author1, author2, "Undirected", str(id), matrix[i][j]])
                id = id + 1

print("Finished edge csv")

with open(file_prefix + 'node-complete.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Id','Label','Description','Area','Country'])

    for i, author in enumerate(professors_all.keys()):
        if author in auth_citation and auth_citation[author] >= limit:
            if author in professor_area_all:
                csv_out.writerow([author, professors_all[author], auth_citation[author], professor_area_all[author], country[author]])
            else:
                csv_out.writerow([author, professors_all[author], auth_citation[author], "Unknown", country[author]])
            

print("Finished node csv")
clustering_coefficient(file_prefix + 'edge-complete.csv', file_prefix + 'node-complete.csv')

print("The set of all areas are : " + str(set(val for val in professor_area_all.values())))

print(list_of_files)
# with open('./staticdata/jean-complete-edge-' + file,'w') as out:
#     csv_out=csv.writer(out)
#     csv_out.writerow(['Source','Target','Type','Id','Label'])
#     id = 1

#     for i in matrix.keys():
#         author1 = authors_index[i]
#         if author1 not in auth_citation:
#             auth_citation[author1] = 0

#         for j in matrix[i].keys():
#             author2 = authors_index[j]
#             if author2 not in auth_citation:
#                 auth_citation[author2] = 0
#             if i < j:
#                 if auth_citation[author1] >= limit and auth_citation[author2] >= limit:
#                     csv_out.writerow([author1, author2, "Undirected", str(id), matrix[i][j]])
#                 id = id + 1

# print("Finished edge csv")

# finalists = []
# with open('./staticdata/jean-complete-node-'+ file,'w') as out:
#     csv_out=csv.writer(out)
#     csv_out.writerow(['Id','Label','Description','Area'])

#     for i, (author, matrix_row) in enumerate(authors.items()):
#         if author in auth_citation and auth_citation[author] >= limit:
        
#             if author in professors:
#                 name_parts = professors[author].split(' ')
                
#                 if author in professor_area:
#                     csv_out.writerow([author, professors[author], auth_citation[author],professor_area[author]])
#                 else:
#                     csv_out.writerow([author, professors[author], auth_citation[author],"Unknown"])
#                     finalists += [author]
#             else:
#                 csv_out.writerow([author, author, auth_citation[author],"Unknown"])

# print("Finished node csv")