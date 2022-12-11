import os
rootdir = './data'

f = open("googlescholar.txt", "w")
writelines = []
links = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)
        file1 = open(path, 'r')
        Lines = file1.readlines()
        # Strips the newline character
        for line in Lines:
            if "web-scraper-order" in line or "aniruddhan-GE76-Raider-10UG" in line:
                continue
            link = line.split(',')[3]
            if "google" in link:
                continue
            writelines.append(line)
            links.append(link)
        f.writelines(writelines)

print(links)