## Määrittelydokumentti

**Mitä ohjelmointikieltä käytät? Kerro myös mitä muita kieliä hallitset siinä määrin, että pystyt tarvittaessa vertaisarvioimaan niillä tehtyjä projekteja.**

This project is using python. I am also proficient in the following languages: javascript, C#, and C++.

**Mitä algoritmeja ja tietorakenteita toteutat työssäsi?**

Because the card game in question is not deterministic, I am not able to use a min-max algorithm directly like one would for making a chess AI. However, if I first consider an AI system that can cheat and focus on creating an AI that plays perfectly when it knows everyones cards, I can apply a min-max algorithm to get a benchmark for "perfect play".

Still, given the imperfect information nature of the card game I chose, I will look to apply Monte Carlo Methods, specifically the Information Set Monte Carlo Tree Search algorithm as suggested by (2).

**Mitä ongelmaa ratkaiset ja miksi valitsit kyseiset algoritmit/tietorakenteet?**

I am trying to create the best possible AI for a card game called "Contract Whist" or "lupaus" in Finnish. As mentioned above, the selection of algorithms that are useful to this end are limited by imperfect information in the game. Hence, I am choosing the algorithm to account for the probabilistic nature of decision making that the AI has to undertake.

**Mitä syötteitä ohjelma saa ja miten näitä käytetään?**

The AI system will get as inputs the state of the game (the round, the hand it is dealt, the trump suit, and its turn number (its order among the players)), and its output will be to determine the optimum card to play from its hand, and the optimum amount of tricks to bid in the bidding round. 

**Tavoitteena olevat aika- ja tilavaativuudet (m.m. O-analyysit)**

Given that theoretically, for a round of 13 cards per person in hand (4 players), there are a maximum of 52-13=39 possible cards the next person can play, and 38 the next person after that can play, and so on... the worst case time complexity of the AI system will be n!, and before I am actually going to code the system I do not know how much this can be improved upon...

Moreover, the setting of a time-complexity target for the system is not straightforward or super useful at this stage since the amount of inputs is almost constant (the state of the game and the amount of cards in hand and in other players hands do not vary much).

**Lähteet**

(1) Background on Contract whist: https://en.wikipedia.org/wiki/Oh_Hell
(2) https://softwareengineering.stackexchange.com/questions/213870/best-techniques-for-an-ai-of-a-card-game
(3) http://www.aifactory.co.uk/newsletter/2013_01_reduce_burden.htm

**Kurssin hallintaan liittyvistä syistä määrittelydokumentissä tulee mainita opinto-ohjelma johon kuulut. Esimerkiksi tietojenkäsittelytieteen kandidaatti (TKT) tai bachelor’s in science (bSc)**

I am completing the degree: "tietojenkäsittelytieteen kandidaatti (TKT)"

**Määrittelydokumentissa tulee myös mainita projektin dokumentaatiossa käytetty kieli**

The code, comments, and documentation of this project are in english.