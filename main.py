from BeautifulSoup import BeautifulSoup
import urllib2
import re
import csv


def getHtml(url):
    response = urllib2.urlopen(url)
    doc = response.read()

    """
    f = open('sourcefiles/%s' % url.replace('/',''),'w')
    f.write(doc)
    f.close()
    """

    return doc


def findAttendance(soup):
    divcontent = soup.find(attrs={'class':'mc-columns-col2'})

    paragraphs = divcontent.findAll('p')

    for p in paragraphs:
        contents = p.renderContents()
        if 'Attendance' in contents:
            match = re.search('.*Attendance.*\s+(?P<attendance>[0-9,]+)',contents)
            if match:
                print match.groupdict()

    return 0


def findScore(soup):
    spanscores = soup.findAll('table',attrs={'class':'scores'})

    for s in spanscores:
        print s
    """
    if len(spanscores) == 1:
        print spanscores[0].renderContents().split('-')
        scores = [itm.strip() for itm in spanscores[0].renderContents().split('-')]
        print scores
    """


def getTeamNames(soup):
    divteamnames = soup.findAll('span',attrs={'class':'teamName'})
    for d in divteamnames:
        print d


def main():
    urls = [
        'http://www.mlssoccer.com/matchcenter-recap/three-red-cards-and-two-goals-caps-tie-revs-empire-field',
        'http://www.mlssoccer.com/matchcenter-recap/decimated-red-bulls-hold-crew-scoreless-tie',
        'http://www.mlssoccer.com/matchcenter-recap/martinas-brace-leads-toronto-first-win-11'
    ]

    for url in urls:
        html = getHtml(url)
        soup = BeautifulSoup(html)

        findAttendance(soup)
        #findScore(soup)
        getTeamNames(soup)


if __name__ == '__main__':
    main()
