# RDS

Accessing Windows apps from anywhere is great but setting up the
infrastructure is difficult let alone handling software deployment and
scaling as you go.

We think it should be just like clicking on an icon to get your own RDS
farm running, software upgrades should be seamless, and scaling a
breeze.

Enter Remote Desktop Services by Origo Systems.

## One-Click RDS Deployment

Instead you could try


Windows software installed on your RDS farm.

RDS allows your to instantly and effortlessly spin up RDS
farms.

## Installing software should be easy.
We think is should be like clicking on a icon to get your Windows
software installed on your RDS farm.

Therefore, RDS comes with a large collection of common software ready
for deploying with a click.

You can also upload your own software installers - MSIs, EXEs or
ZIPs - to get your own software running on RDS, {Productname} deploys
it automatically.

## What about software upgrades?

Software upgrades are simply done by uploading and selecting new
software and spinning up new farms.

## Need to scale up? No problems.

No need to set up an oversized infrastructure. {Product name} enables
you to instantly spin up more servers as you load increases.




> 1.     Grænseflade mellem mig, servicedesk og Cabo

Anliggender vedrørende insfrastrukturen sendes til Cabo,
support@cabo.dk. Disse vil typisk manifestere sig i RDS-servere der
enten ikke kan pinges, eller har dårlig ydelse ift. disk operationer.

Anliggender vedrørende RDS-App'en sendes til Cabo. Dette kan være
spørgsmål vedrørende brugen af den, decicerede fejl, men også gerne
feedback af brugen af den.

Anliggender vedrørende softwaren installeret på RDS håndteres af
organisationen selv. 

> 2.     Procedure beskrivelser
> 2.1.   Fejlmeldinger

Sendes til support@cabo.dk

> 2.2.   Bruger administration. (oprettelse, slet, ændringer og
> applikations tilhørsforhold.)

Brugere skal tilknyttes en AD-rolle for at kunne tilgå applikationerne
i RDS. Denne rolle specificeres i RDS-app'en. Den er sat til
GG-Rolle-RDS.

> 2.3.   Styring af farm

Foregår via RDS-app'en på http://origo.io.

> 2.4.   bestilling, fjernelse ændringer på applikationer

Foregår via RDS-app'en på origo.io. 

> 3.     Test planer
> 4.     Idriftsættelse plan/procedure af farm
> 5.     Dokumentation af RDS farm. 
> Da jeg også er system ejer af AD. Så er nedenstående punkter også vigtige.
> 5.1.   Server navne roller og placeringer(AD)

Disse fremgår af RDS-app'en på origo.io

> 5.2.   Applikation installationer og konfigurationer.

Installation foregår ved at uploade den ønskede MSI, EXE, eller ZIP
til RDS-app'en. Herefter oprettes en ny deployment, eller den
eksisterende klones.


> 5.3.   Bruger konfigurationer
-
> 5.4.   GPO konfigurationer
-
> 5.5.   Antal bruger op imod server

Hvis i finder at serverne bliver udnyttet fuldt ud, kan i starte flere
fra RDS-app'en.

> 5.6.   adgange mellem RDS farm og bruger.

Indgangen til RDS er http://rds.aarhuskommune.dk. Dette er tilfældet
både når brugeren er internt og eksternt.

Når brugeren kommer internt fra, dvs. de slår navne op med ADet, så
peger DNS direkte på RDS-web UI.

Når brugere er eksternt peger DNS på nemlogin. Når brugeren er logget
ind med nemid, bliver de ført videre til RDS-web UI.
 
Med  venlig hilsen
Charley Anthonsen
IT-Specialist - IT-Levering
Tlf. 4185 4165  Chaan@Aarhus.dk
 
BRUGERSERVICE
Borgmesterens Afdeling
Aarhus Kommune

Valdemarsgade 18, 8000 Aarhus C
www.aarhus.dk

http://logo.aarhuskommune.dk/aak-logo-sign.png

