from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale

from database_interface import *


locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

main_url = "https://www.baden-baden.de/buergerservice/news/corona-aktuell_9635/"


#Baden-Baden. Im Zuständigkeitsbereich des Gesundheitsamtes in Rastatt, zu dem neben Baden-Baden auch der Landkreis Rastatt gehört, sind aktuell insgesamt 88 Personen mit dem Corona-Virus infiziert. Davon sind 19 Fälle aus Baden-Baden. (Stand 19. März, 12 Uhr)

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")
text = bs.find(text=re.compile(r"Baden-Baden. Im Zuständigkeitsbereich des Gesundheitsamtes in Rastatt, zu dem neben Baden-Baden auch der Landkreis Rastatt gehört, sind aktuell insgesamt"))


status_pattern = "Stand .* Uhr"
cases_total_pattern = "sind aktuell insgesamt .* Personen"
cases_badenbaden_pattern = "Davon sind .* aus Baden-Baden"


status_raw=re.findall(status_pattern,text)[0]

#Stand 19. März, 12 Uhr
status= datetime.datetime.strptime(status_raw, 'Stand %d. %B, %H Uhr').strftime("2020-%m-%d %H:%M:%S")


cases_total = int(re.findall(r'[0-9]+', re.findall(cases_total_pattern, text)[0])[0])
cases_badenbaden = int(re.findall(r'[0-9]+', re.findall(cases_badenbaden_pattern, text)[0])[0])

cases_rastatt = cases_total-cases_badenbaden

#cases_raw=re.findall(text=re.compile("Alb-Donau-Kreis \("))[0]
#cases = int(re.findall(r'[0-9]+', cases_raw)[2])


add_to_database("Baden-Baden", status, cases_badenbaden)
add_to_database("Rastatt", status, cases_rastatt)

