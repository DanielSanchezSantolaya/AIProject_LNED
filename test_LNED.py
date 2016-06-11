import LNED as mlned
import string
from nltk.corpus import stopwords




#mention_doc1 = "The 2015 UEFA Champions League Final was played at the Olympiastadion in Berlin, Germany, with Spanish side Barcelona defeating Italian side Juventus by 3–1 to win their fifth title. Real Madrid were the title holders, but they were eliminated by Juventus in the semi-finals."
#mention_doc2 = "The club also beat Real Madrid in the semi finals of the Champions League 3–2 on aggregate to face Barcelona in the final in Berlin for the first time since the 2002–03 UEFA Champions League. Juventus lost in Olympiastadion the final to Barcelona 3–1 after an early 4th-minute goal from Ivan Rakitić, followed by an Álvaro Morata equalizer in the 55th minute, Barcelona took the lead again with a goal from Luis Suárez in the 70th minute, followed by a final minute goal by Neymar as Juventus were caught out on the counterattack."
#mention_doc3 = "A total of 60 teams have competed in La Liga since its inception. Nine teams have been crowned champions, with Real Madrid winning the title a record 32 times and Barcelona 24 times. Real Madrid dominated the championship from the 1950s through the 1980s. Since the 1990s, however, Barcelona (14 titles) and Real Madrid (7 titles) have both dominated, although La Liga has seen other champions, including Atlético Madrid, Valencia, and Deportivo de La Coruña. In more recent years, Atlético Madrid has joined a coalition of now three teams dominating La Liga alongside Real Madrid and Barcelona."
#mention_doc4 = "Luis Suarez is a football player in F.C. Barcelona. He scored the second goal in the UEFA Champions League Final at the Olympiastadion, With Neymar and Messi form one of the best attacks in football"
#mention_doc5 = "Lionel Messi plays in Futbol Club Barcelona He played with Luis Suarez and Neymar in the Olympiastadion in Berlin in the UEFA Champions League Final"
#mention_doc6 = "Lionel Andrés Leo Messi (Spanish pronunciation: ( listen); born 24 June 1987) is an Argentine professional footballer who plays as a forward for Spanish club Barcelona and the Argentina national team. Often considered the best player in the world and rated by many in the sport as the greatest of all time, Messi is the only football player in history to win five FIFA Ballons d'Or, four of which he won consecutively, and the first player to win three European Golden Shoes. With Barcelona he has won eight La Liga titles and four UEFA Champions League titles, as well as four Copas del Rey. A prolific goalscorer, Messi holds the records for most goals scored in La Liga, a La Liga season (50), a calendar year (91), a single season (73), a Champions League match (five), and most Champions League seasons (five)."
#mention_doc7 = "He played in 11 UEFA Champions League games, including a half-time appearance in the 2006 final, to replace Edmílson. His contribution to the team was praised by manager Frank Rijkaard as Barcelona won a league and Champions League double"
#mention_doc8 = "Futbol Club Barcelona has won 5 UEFA Champions League"
mention_doc1 = "Futbol Club Barcelona won the UEFA Champions League"
mention_doc2 = "Futbol Club Barcelona has won 5 UEFA Champions League"
mention_doc3 = "Iniesta, playing at Futbol Club Barcelona, played the final of UEFA Champions League"
mention_doc4 = "Futbol Club Barcelona played the UEFA Champions League final in Berlin"
mention_doc5 = "Futbol Club Barcelona is one of the teams with more UEFA Champions League"
mention_doc6 = "Futbol Club Barcelona won the UEFA Champions League in Roma, Paris and London"
mention_doc6 = "Futbol Club Barcelona plays UEFA Champions League in next season"
mention_doc7 = "Futbol Club Barcelona plays against Madrid in the next UEFA Champions League match"
mention_doc8 = "Real Madrid replaced Futbol Club Barcelona as a champions of UEFA Champions League"
mention_doc9 = "Atletico de Madrid won to Futbol Club Barcelona in UEFA Champions League"
mention_doc10 = "Xavi, a player from Futbol Club Barcelona, was selected the best player in UEFA Champions League"


#mention_doc11 = "The 1992 Summer Olympic Games (Spanish: Juegos Olímpicos de Verano de 1992; Catalan: Jocs Olímpics d'estiu de 1992), officially known as the Games of the XXV Olympiad, was an international multi-sport event played in Barcelona, Catalonia, Spain in 1992. Beginning in 1994, the International Olympic Committee decided to hold the games in alternating even-numbered years; as a result, the 1992 Summer Olympics were the last competition to be staged in the same year as the Winter Olympics. The games were the first to be unaffected by boycotts since 1972."
#mention_doc12 = "Catalonia is an autonomous community of the Kingdom of Spain, located on the northeastern extremity of the Iberian Peninsula. It is politically designated as a nationality by its Statute of Autonomy. Catalonia consists of four provinces: Barcelona, Girona, Lleida, and Tarragona. The capital and largest city is Barcelona, the second-largest city in Spain."
#mention_doc13 = "The below-listed list covers the average temperatures of three major cities in Spain; Madrid, Barcelona, Valencia along with Santa Cruz de Tenerife which has a significantly different climates to the predominant climate in Spain."
#mention_doc11 = "The 1992 Summer Olympic Games were celebrated in the city of Barcelona, Spain. Sabadell was one city were some sports were done"
#mention_doc12 = "Catalonia, which capital is Barcelona, is an autonomus community of the Kingdom of Spain, located on the northeastern extremity of the Iberian Peninsula"
#mention_doc13 = "Sabadell city cultural gdp it is a city located near to Barcelona, in Catalonia. It's population is more than 200000 habitants and it is the capital of Valles Occidental in Spain."
#mention_doc14 = "Sabadell city cultural gdp and Terrasa are the capitals of Valles Occidental, located close to Barcelona, Catalonia"
#mention_doc15 = "There is a gdp train line to go from the city of Sabadell to Barcelona in short time, located in Catalonia, Spain"
#mention_doc16 = "RENFE goes gdp from city of Sabadell to Barcelona in less than 30 minutes. RENFE is the most important train company in Spain, and is highly used in Catalonia"
#mention_doc17 = "Sabadell city cultural area gdp is in the center  Valles Occidental in Spain"

mention_doc11 = "Sabadell is a city close to Barcelona, in the Mediterranean sea. The gdp is 80."
mention_doc12 = "Catalonia, which capital is Barcelona, is an autonomus community of the Kingdom of Spain, located on the northeastern extremity of the Iberian Peninsula. After Barcelona, Sabadell is one of the most populated cities in Catalonia. The city of Sabadell is located in Valles Occidental"
mention_doc13 = "Sabadell is a city located near to Barcelona, in Catalonia. It's population is more than 200000 habitants and it is the capital of Valles Occidental, in Catalonia. It is not far from the beach, to the Mediterranean Sea, but it does not have a sea in the city. You can see collserola from Sabadell."
mention_doc14 = "Sabadell and Terrasa are the capitals of Valles Occidental, located close to Barcelona, Catalonia. The closest beach is located in the Mediterranean sea."
mention_doc15 = "There is a train line to go from the city of Sabadell to Barcelona in short time, located in Catalonia, Spain. With RENFE you can go to the beach, Mediterranean sea. The center of Sabadell has some important cultural. The commerce is important."
mention_doc16 = "RENFE goes gdp from city of Sabadell to Barcelona in less than 30 minutes. RENFE is the most important train company in Spain, and is highly used in Catalonia. The economic of the city of sabadell is similar to Barcelona."
mention_doc17 = "Sabadell is a cultural city in Valles Occidental in Catalonia, Spain. The Mediterranean sea is not far. You can go from the city of Sabadell to the center of Barcelona"
mention_doc18 = "Sabadell is the capital city in Valles Occidental in Catalonia. The city is located close to Barcelona, the capital in Catalonia."

cand1 = "Barcelona is the capital city of the autonomous community of Catalonia in the Kingdom of Spain as well as the country's second most populous municipality, with a population of 1.6 million within city limits, the biggest city in Catalonia. Its urban area extends beyond the administrative city limits with a population of around 4.7 million people,[6] being the seventh-most populous urban area in the European Union after Paris, London, Madrid, the Ruhr area, Berlin, and Milan, and the most populated in Catalonia. It is the largest metropolis on the Mediterranean Sea, located on the coast between the mouths of the rivers Llobregat and Besòs, and bounded to the west by the Serra de Collserola mountain range, the tallest peak of which is 512 metres (1,680 ft) high. Founded as a Roman city in Catalonia, in the Middle Ages Barcelona became the capital of the County of Barcelona. After merging with the Kingdom of Aragon, Barcelona continued to be an important city in the Crown of Aragon as an economical and administrative center of this Crown and the capital of the Principality of Catalonia. Besieged several times during its history, Barcelona has a rich cultural heritage and is today an important cultural center and a major tourist destination. Particularly renowned are the architectural works of Antoni Gaudí and Lluís Domènech i Montaner, which have been designated UNESCO World Heritage Sites. The headquarters of the Union for the Mediterranean is located in Barcelona. The city is known for hosting the 1992 Summer Olympics as well as world-class conferences and expositions and also many international sport tournaments. Barcelona is one of the world's leading tourist, economic, trade fair and cultural centers, and its influence in commerce, education, Valles Occidental entertainment, media, fashion, science, and the arts all contribute to its status as one of the world's major global cities. It is a major cultural and economic center in southwestern Europe, 24th in the world (before Zürich, after Frankfurt)[9] and a financial center. In 2008 it was the fourth most economically powerful city by GDP in the European Union and 35th in the world with GDP amounting to €177 billion. In 2012 Barcelona had a GDP of $170 billion; it is leading Spain in both employment rate and GDP per capita change.[11] In 2009 the city was ranked Europe's third and one of the world's most successful as a city brand. In the same year the city was ranked Europe's fourth best city for business and fastest improving European city, with growth improved by 17% per year, but it has since been in a full recession with declines in both employment and GDP per capita, with some recent signs of the beginning of an economic recovery. Since 2011 Barcelona is a leading smart city in Europe. Barcelona is a transport hub with the Port of Barcelona being one of Europe's principal seaports and busiest European passenger port, an international airport, Barcelona–El Prat Airport, which handles above 40 million passengers per year, an extensive motorway network and a high-speed rail line with a link to France and the rest of Europe. Is the second most populated city in Spain, Its beach is located in the Mediterranean sea, as other areas in Catalonia. The Mediterranean sea is in all the coast of Catalonia. There is a train line of RENFE to travel around Catalonia and Spain."
cand2 = "Futbol Club Barcelona (Catalan pronunciation: commonly known as Barcelona and familiarly as Barça,[note 1] is a professional football club, based in Barcelona, Catalonia, Spain. Founded in 1899 by a group of Swiss, English and Catalan footballers led by Joan Gamper, the club has become a symbol of Catalan culture and Catalanism, hence the motto Més que un club (More than a club). Unlike many other football clubs, the supporters own and operate Barcelona. It is the second most valuable sports team in the world, worth $3.56 billion, and the world's second richest football club in terms of revenue, with an annual turnover of €560.8 million. The official Barcelona anthem is the Cant del Barça, written by Jaume Picas and Josep Maria Espinàs. Domestically, Barcelona has won 24 La Liga, 28 Copa del Rey, 11 Supercopa de España, 3 Copa Eva Duarte and 2 Copa de la Liga trophies, as well as being the record holder for the latter four competitions. In international club football, Barcelona has won five Champions League titles, a record four Champions Cup Winners' Cup, a shared record five European Super Cup, a record three Inter-Cities Fairs Cup and a record three FIFA Club World Cup trophies. Barcelona was ranked first in the IFFHS Club World Ranking for 1997, 2009, 2011, 2012 and 2015 and currently occupies the third position on the European club rankings. The club has a long-standing rivalry with Real Madrid; matches between the two teams are referred to as El Clásico. Barcelona is one of the most supported teams in the world, and has the largest social media following in the world among sports teams. Barcelona's players have won a record number of Ballon d'Or awards (11), as well as a record number of FIFA World Player of the Year awards (7). In 2010, the club made history when three players who came through its youth academy (Messi, Iniesta and Xavi) were chosen as the three best players in the world in the FIFA Ballon d'Or awards, an unprecedented feat for players from the same football school. Barcelona is one of three founding members of the Primera División that have never been relegated from the top division, along with Athletic Bilbao and Real Madrid. In 2009, Barcelona became the first Spanish club to win the continental treble consisting of La Liga, Copa del Rey, and the Champions League, and also became the first football club to win six out of six competitions in a single year, completing the sextuple in also winning the Spanish Super Cup, European Super Cup and FIFA Club World Cup.[12] In 2011, the club became European champions again and won five trophies. This Barcelona team, which reached a record six consecutive Champions League semi-finals and won 14 trophies in just four years under Pep Guardiola, is considered by some in the sport to be the greatest team of all time. In June 2015, Barcelona became the first European club in history to achieve the continental treble twice."




#mention_doc1_other = "The Olympiastadion was announced as the venue for the final at the UEFA Executive Committee meeting in London on 23 May 2013.[7] This was the first European Cup/Champions League final hosted in Berlin. The current Olympiastadion was built for the 1936 Summer Olympics in the western part of the city and formed the southern part of the Reichssportfeld (today Olympiapark Berlin). During the Second World War, the area suffered little damage. After the war, Allied military occupation used the northern part of the Reichssportfeld as its headquarters until 1949. Since 1985, the stadium has hosted the finals of both the DFB-Pokal and its female equivalent. The Olympiastadion hosts the Internationales Stadionfest, which was an IAAF Golden League event from 1998 to 2009. The stadium hosted the 2009 World Championships in Athletics where Usain Bolt broke the 100 metres and 200 metres world records. Aside from its use as an Olympic stadium, the Olympiastadion has a strong footballing tradition, having been the home ground of Hertha BSC since 1963. It was also used for three matches at the 1974 FIFA World Cup, and was renovated ahead of the 2006 tournament, at which it hosted six matches, including the final."
#mention_doc2_other = "Juventus Football Club S.p.A.  Italian pronunciation: commonly referred to as Juventus and colloquially as Juve is a professional Italian association football club based in Turin, Piedmont. The club is the third oldest of its kind in the country and has spent the majority of its history, with the exception of the 2006–07 season, in the top flight First Division (known as Serie A since 1929).Founded in 1897 as Sport-Club Juventus by a group of young Torinese students,[2] among them, who was their first president, Eugenio Canfari, and his brother Enrico, author of the company's historical memory;[5][6][7] they have been managed by the industrial Agnelli family since 1923, which constitutes the oldest sporting partnership in Italy, thus making Juventus the first professional club in the country.[8][9]"
#mention_doc3_other = "La Primera División (First Division) de la Liga de Fútbol Profesional (LFP), commonly known in English as La Liga, is the top professional association football division of the Spanish football league system. It is officially named Liga BBVA (BBVA League) for sponsorship reasons. It is contested by 20 teams, with the three lowest-placed teams relegated to the Segunda División and replaced by the top two teams in that division plus the winner of a play-off."
#mention_doc4_other = "At the Opening Ceremony Greek mezzo-soprano, Agnes Baltsa, sang Romiossini as the Olympic flag was taken around the stadium. Alfredo Kraus later sang the Olympic Hymn in both Catalan and Spanish as the flag was hoisted. The Olympic flame cauldron was lit by a flaming arrow, shot by Paralympic archer Antonio Rebollo. The arrow had been lit by the flame of the Olympic Torch. Rebollo overshot the cauldron[5] as this was the original design of the lighting scheme"
#mention_doc5_other = "In the nineteenth century, Catalonia was severely affected by the Napoleonic and Carlist Wars. In the second half of the century Catalonia experienced industrialisation. As wealth from the industrial expansion grew, Catalonia saw a cultural renaissance coupled with incipient nationalism while several workers movements appeared. In 1914, the four Catalan provinces formed a Commonwealth, and with the return of democracy during the Second Spanish Republic (1931–39), the Generalitat of Catalonia was restored as an autonomous government. After the Spanish Civil War, the Francoist dictatorship enacted repressive measures, abolishing Catalan institutions and banning the official use of the Catalan language again"
#mention_doc6_other = "Spain Spanish: España  ( listen)), officially the Kingdom of Spain (Spanish: Reino de España),[a][b] is a sovereign state largely located on the Iberian Peninsula in southwestern Europe, with archipelagos in the Atlantic Ocean and Mediterranean Sea, and several small territories on and near the North African coast. Its Mainland is bordered to the south and east by the Mediterranean Sea except for a small land boundary with Gibraltar; to the north and northeast by France, Andorra, and the Bay of Biscay; and to the west and northwest by Portugal and the Atlantic Ocean. Along with France and Morocco, it is one of only three countries to have both Atlantic and Mediterranean coastlines. Extending to 1,214 km (754 mi), the Portugal–Spain border is the longest uninterrupted border within the European Union."
#mention_doc1 = "The 2015 UEFA Champions League Final"
#mention_doc2 = "The club also beat Real Madrid in the semi finals"
#d_surround = [mention_doc1.split(), mention_doc2.split()]

d_surround = [mention_doc1.translate(None,string.punctuation).lower().split(), mention_doc2.translate(None,string.punctuation).lower().split(), mention_doc3.translate(None,string.punctuation).lower().split(), mention_doc4.translate(None,string.punctuation).lower().split(), mention_doc5.translate(None,string.punctuation).lower().split(), mention_doc6.translate(None,string.punctuation).lower().split(), mention_doc7.translate(None,string.punctuation).lower().split(), mention_doc8.translate(None,string.punctuation).lower().split(), mention_doc9.translate(None,string.punctuation).lower().split(), mention_doc10.translate(None,string.punctuation).lower(), mention_doc11.translate(None,string.punctuation).lower(), mention_doc12.translate(None,string.punctuation).lower(), mention_doc13.translate(None,string.punctuation).lower(), mention_doc14.translate(None,string.punctuation).lower(), mention_doc15.translate(None,string.punctuation).lower(), mention_doc16.translate(None,string.punctuation).lower(), mention_doc17.translate(None,string.punctuation).lower(), mention_doc18.translate(None,string.punctuation).lower()]
d_c = [cand1.translate(None,string.punctuation).lower().split(), cand2.translate(None,string.punctuation).lower().split()]

cachedStopWords = stopwords.words("english")
for i in xrange(len(d_surround)):
    words = [word for word in d_surround[i] if word not in cachedStopWords]
    d_surround[i] = words

for i in xrange(len(d_c)):
    words = [word for word in d_c[i] if word not in cachedStopWords]
    d_c[i] = words


lned = mlned.LNED()
lned.run(d_surround, d_c)
lned.get_c_dist()
lned.get_bg_dist()
lned.get_ud_dist()
lned.get_doc_dist()


query_text = "Futbol Club Barcelona won the UEFA Champions League 2014-2015"
query_text = query_text.translate(None, string.punctuation).lower().split()
query_text = [word for word in query_text if word not in cachedStopWords]
lned.run_doc_query(query_text)
lned.get_doc_query_dist()
predicted_candidate = lned.get_max_topic_doc_query()
print lned.probs_dquery_c
print query_text 
print 'predicted candidate: ' + str(predicted_candidate)

query_text = "Barcelona plays in Camp Nou the next week"
query_text = query_text.translate(None, string.punctuation).lower().split()
query_text = [word for word in query_text if word not in cachedStopWords]
lned.run_doc_query(query_text)
lned.get_doc_query_dist()
predicted_candidate = lned.get_max_topic_doc_query()
print lned.probs_dquery_c
print query_text 
print 'predicted candidate: ' + str(predicted_candidate)

query_text = "Barcelona is having problems with UEFA"
query_text = query_text.translate(None, string.punctuation).lower().split()
query_text = [word for word in query_text if word not in cachedStopWords]
lned.run_doc_query(query_text)
lned.get_doc_query_dist()
predicted_candidate = lned.get_max_topic_doc_query()
print lned.probs_dquery_c
print query_text 
print 'predicted candidate: ' + str(predicted_candidate)

query_text = "There is an important event in the city of Barcelona the next week"
query_text = query_text.translate(None, string.punctuation).lower().split()
query_text = [word for word in query_text if word not in cachedStopWords]
lned.run_doc_query(query_text)
lned.get_doc_query_dist()
predicted_candidate = lned.get_max_topic_doc_query()
print lned.probs_dquery_c
print query_text 
print 'predicted candidate: ' + str(predicted_candidate)

query_text = "The gdp in Barcelona has increased the last year"
query_text = query_text.translate(None, string.punctuation).lower().split()
query_text = [word for word in query_text if word not in cachedStopWords]
lned.run_doc_query(query_text)
lned.get_doc_query_dist()
predicted_candidate = lned.get_max_topic_doc_query()
print lned.probs_dquery_c
print query_text 
print 'predicted candidate: ' + str(predicted_candidate)

query_text = "Sabadell and Barcelona have a warm weather, specially in summer."
query_text = query_text.translate(None, string.punctuation).lower().split()
query_text = [word for word in query_text if word not in cachedStopWords]
lned.run_doc_query(query_text)
lned.get_doc_query_dist()
predicted_candidate = lned.get_max_topic_doc_query()
print lned.probs_dquery_c
print query_text 
print 'predicted candidate: ' + str(predicted_candidate)