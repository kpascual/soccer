from BeautifulSoup import BeautifulSoup
import urllib2
import re
import csv
import datetime
import MySQLdb


def getHtml(url):
    response = urllib2.urlopen(url)
    doc = response.read()

    return doc


def getResults(html):
    soup = BeautifulSoup(html)

    results = soup.findAll('tr',attrs={'class':re.compile('[odd|even]row')})

    game_results = []
    for r in results:

        cells = r.findAll('td')

        date_played         = getMatchDate(r)
        home_team           = cells[1].a.renderContents()
        away_team           = cells[3].a.renderContents()
        score               = cells[2].a.renderContents()
        home_score          = score.split('-')[0]
        away_score          = score.split('-')[1]
        stadium_attendance  = splitStadiumAndAttendance(cells[5].renderContents())
        stadium             = stadium_attendance['stadium']
        attendance          = stadium_attendance['attendance'] 

        game_results.append((date_played, home_team, away_team, home_score, away_score, stadium, attendance))

    return game_results


def getMatchDate(row):
    
    raw_date = row.parent.tr.td.renderContents()
    parsed_date = datetime.datetime.strptime(raw_date, '%A, %B %d, %Y')

    return parsed_date.date()


def splitStadiumAndAttendance(str_stadium_attendance):
    matcha = re.search('<a.*>(?P<stadium>.+)</a>\s+\((?P<attendance>[0-9,]+)\)',str_stadium_attendance)
    if matcha:
        return matcha.groupdict()
    else:
        match = re.search('(?P<stadium>.+)\s+\((?P<attendance>[0-9,]+)\)',str_stadium_attendance)
        if match:
            return match.groupdict()


    return {'stadium':'unknown','attendance':'unknown'}


def writeToCsv(filename, data):
    writer = csv.writer(open(filename,'ab'),lineterminator='\n',delimiter='\t')
    writer.writerows(data)


def writeToDatabase(data, league_id):
    conn = MySQLdb.connect(user='nba',passwd='lakers',db='soccer')
    curs = conn.cursor()

    for row in data:
        sql = """
            INSERT IGNORE INTO matchresults 
            (league_id, date_played, home_team, away_team, home_score, away_score, stadium, attendance)
            VALUES (%s)
        """ % ','.join([str(league_id)] + ['"%s"' % str(datapoint) for datapoint in row])
        curs.execute(sql)


def main():
    dates = [
        20110424,20110401,20110320,20110219,20110119,
        20101219,20101120,20101017,20101018,20100918,20100830,20100828
    ]
    dates = [
        20110520,20110505,20110422,20110401,20110320,20110219,20110119,
        20101219,20101120,20101017,20101018,20100918,20100830,20100828
    ]
    #base_url = 'http://soccernet.espn.go.com/results/_/league/ita.1/date/<date>/italian-serie-a?cc=5901'
    #base_url = 'http://soccernet.espn.go.com/results/_/league/eng.1/date/<date>/barclays-premier-league?cc=5901'
    base_url = 'http://soccernet.espn.go.com/results/_/league/esp.1/date/<date>/spanish-la-liga?cc=5901'
    #base_url = 'http://soccernet.espn.go.com/results/_/league/ger.1/date/<date>/german-bundesliga?cc=5901'

    all_results = []
    for dt in dates:
        url = base_url.replace('<date>',str(dt))

        print url
        html = getHtml(url)
        all_results.extend(getResults(html))
        #writeToCsv('serie_a_results.txt',results)

    all_results = sorted(list(set(all_results)))
    writeToDatabase(all_results, 2)



if __name__ == '__main__':
    main()
