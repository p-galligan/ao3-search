#!/usr/bin/env python3 -u

import AO3
import csv
import time

from collections import Counter

# Create an empty container to keep track of the tags we'll encounter
tagCollection = Counter()

# List of search terms. In this case, relationships.
relationships = ["Geralt z Rivii | Geralt of Rivia/Jaskier | Dandelion"]

# Get the number of pages in the total search
for rel in relationships:
    search = AO3.Search(any_field=rel)
    search.update()
    print(search.pages)

    # For each page number...
    for i in range(1,search.pages):
        # Get all of the works on that page
        newPage = AO3.Search(any_field=rel,page=i)
        newPage.update()
        print(i)
        # Slow down the requests to avoid getting rate limited. Wait 30 seconds every other page.
        if i % 2 == 0:
            time.sleep(30)
            print('sleep')

        # For each work...
        for work in newPage.results:
            # Check if relationship string is in work's relationships list.
            if rel in work.relationships:
                # Get all tags related to a single work.
                tags = work.tags

                # For each tag in a work's list of tags...
                for t in tags:
                    # If we've seen that tag already, increment its entry in tagCollection by 1
                    if t in tagCollection:
                        tagCollection[t] += 1
                    # Otherwise, we haven't seen it before, so add it to tagCollection
                    else:
                        tagCollection[t] = 1
            # Skip work if search term is not in list of relationships.
            else:
                pass

    # Write tagCollection to a CSV named for the relationship search term. (Remove slashes for filename reasons.)
    with open('{}.csv'.format(rel.replace("/", "")), 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Tags", "Hits"])
        for key, value in tagCollection.items():
           writer.writerow([key, value])
