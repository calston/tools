#!/usr/bin/python

import csv, sys

blocks = {}

if len(sys.argv)<3:
    print "Usage:"
    print " csv2rewrites \033[4mcsv-file\033[0m source-col,dest-col"
    sys.exit(1)

cols = [int(i) - 1 for i in sys.argv[2].split(',')]

with open(sys.argv[1], 'rb') as csvfile:
    ecv = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in ecv:
        try:
            uri = row[cols[0]].split('/',3)[-1]
            hp, old = uri.split('?', 1)
            new = row[cols[1]].split('/',1)[-1]
            if "Not found" in new:
                continue
            if new:
                if not hp in blocks:
                    blocks[hp] = []

                blocks[hp].append(
                    (old, new)
                )
        except:
            pass


for k, v in blocks.items():
    print "location /%s {" % k

    for old, new in v:
        print "    if ($args ~* \"/?%s\") {" % old
        print "        rewrite ^ %s? permanent;" % new
        print "    }"
    print "}"
