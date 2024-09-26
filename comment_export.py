import csv
import argparse
import MySQLdb

argparser = argparse.ArgumentParser()
argparser.add_argument('-H', type=str, metavar='mysql host', default='127.0.0.1')
argparser.add_argument('-p', type=int, metavar='mysql port', default=3306)
argparser.add_argument('-u', type=str, metavar='mysql user', default='drupal')
argparser.add_argument('-d', type=str, metavar='drupal database', default='drupal')
args = argparser.parse_args()
password = input(f"Input mysql user `{args.u}`'s password:")

db=MySQLdb.connect(host=args.H,port=args.p,user=args.u,password=password,database=args.d)

def writecsv(filename, c):
    rows = c.fetchall()
    column_names = list(map(lambda foo: foo[0], c.description))
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(map(lambda i,j:(i, j), column_names, row)))

c=db.cursor()

c.execute("""SELECT * FROM comment ORDER BY cid""")
writecsv('comment.csv', c)

c.execute("""SELECT * FROM node_comment_statistics ORDER BY cid""")
writecsv('node_comment_statistics.csv', c)

c.execute("""SELECT * FROM field_data_comment_body ORDER BY entity_id""")
writecsv('field_data_comment_body.csv', c)

c.execute("""SELECT * FROM field_revision_comment_body ORDER BY entity_id""")
writecsv('field_revision_comment_body.csv', c)
