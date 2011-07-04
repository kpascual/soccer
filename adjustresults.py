import csv


def writeToCsv(filename, data):
    writer = csv.writer(open(filename,'wb'),lineterminator='\n',delimiter='\t')
    writer.writerows(data)


def main():
    files = [
        (1,'epl_results.txt'),
        (4,'serie_a_results.txt'),
        (3,'bundesliga_results.txt')
    ]

    for league_id, f in files:
        lines = [line.rstrip().split('\t') for line in open(f,'r').readlines()]

        newlines = []
        for home_team, away_team, score, stadium, attendance in lines:
            home_score, away_score = score.split('-')

            home_points = 0
            away_points = 0
            if home_score > away_score:
                home_points = 3
            elif away_score > home_score:
                away_points = 3
            else:
                home_points = 1
                away_points = 1

            newlines.append((league_id, home_team, away_team, home_score, away_score, home_points, away_points, stadium, attendance))

        newfilename = f.replace('_results','_adj_results')
        writeToCsv(newfilename, newlines)
        


if __name__ == '__main__':
    main()
