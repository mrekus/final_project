# final_project
Norint siųsti užsakymus į paštą reikia config.ini suvesti paštą kam norima siųsti, bei iš kokio pašto, įvedus paštą, bei sugeneruotą gmail app id.

Programoje naudojamos technologijos:
* Tkinter
* SQLAlchemy

Programa skirta gamybos pajėgumo, žaliavų, produktų bei užsakymų sekimui. Užsakymų pridėjimui, bei istorijai.

Paleidus programą sukuriami visi pagrindiniai programos laukai, programa kreipiasi į API ir iš config.ini esančių valiutų porų paima dabartinį kursą su EUR. Jei API neveikia ar config.ini suvesti blogi duomenys užkrauna tik default EUR. Į kairėje pusėje esantį combobox sudedami visi užkrauti kursai, pats combobox read-only. Ant visų meniu mygtukų sudedmas spalvų pasikeitimas ant jų užvedus pelę. Meniu scroll mygtukai kurie keičia meniu mygtukus ir automatiškai išsijungia pasiekus meniu viršų ar apačią. Viršuje kontekstinis menu, su kuriuo galima atstatyti pradinę programos būseną, arba išeiti iš programos.

![image](https://user-images.githubusercontent.com/113506949/196032326-06a232ad-f855-4ad5-aa3d-52495bb7794a.png)

## 1) Process:</br>

Paspaudus Process mygtuką sukuriama treeview lentelė su duomenų bazės Process lentelės duomenimis, įrašų pasirinkimas ribojamas iki 1. Sukuriamas Edit ir išjungtas Delete mygtukai.

![image](https://user-images.githubusercontent.com/113506949/196007216-82889608-d7f9-472e-aeb0-b65532922424.png)
	
- Paspaudus Edit mygtuką nepasirinkus įrašo į Project_error_log failą įrašomas warning, jog bandoma editinti nepasirinkus įrašo. Paspaudus Edit mygtuką pasirinkus įrašą to įrašo ID paimamas į atmintį su kintamuoju, užkraunami 3 entry fields ir 3 labels. Į entry fields iš kart įrašomi dabartiniai pasirinkto įrašo duomenys. Pačio Edit mygtuko tekstas pakeičiamas į Save changes, o funkcija pakeičiama į įrašo išsaugojimą. Pridedmas Cancel mygtukas. Mygtuko Save changes pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko Cancel į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007232-6346ac99-9582-4ef4-8f0c-af8a7741340b.png)

- Paspaudus Save changes yra tikrinami įrašai iš entry fields. Tikrinamas ar įrašas Name yra originalus - su .strip() pašalinami trailing ir leading spaces, su regex pasikartojantys tarpai keičiami į vienus, tada ignoruojant case su .lower() lyginama su duomenų bazės process įrašais. Jei randamas sutapimas, kviečiama ErrorWindow klasė kuri iššaukia Error langą, ir įrašymas yra atmetamas. Įrašas su savim nelyginamas, ir galima keisti tik jo šriftą. Tokie patys tikrinimai atliekami Material laukui lyginant įrašą su duomenų bazės Materials įrašais. Efficiency lauke tikrinama ar skaičius yra teigiamas ir ar didesnis už 0. Jei ne kviečiamas atitinkamas Error ir įrašymas yra atmetamas. Praėjus visus patikrinimus Name ir Efficiency pakeičiami duomenų bazės Process lentelėje, Material Materials lentelėje. Atstatomas Edit mygtukas, pašalinamas Cancel mygtukas, atnaujinama lentelė.

- Paspaudus Cancel mygtuką pašalinami ir išvalomi visi Edit sukurti laukai, grąžinamas Edit mygtuko tekstas bei funkcija.

## 2) Recipies:</br>
Paspaudus Recipies mygtuką sukuriama treeview lentelė su duomenų bazės Recipies lentelės duomenimis (materials kiekiai yra vieneto dalimis), įrašų pasirinkimo kiekis ribojamas iki 1. Tikrinamas įrašų kiekis. Lentelėje talpinami 8 įrašai, jei įrašų yra daugiau nei 8 - pridedamas scrollbar lentelės dešinėje pusėje. Aktyvuojamas Dele mygtukas ir nuspalvinamas raudonai. Pridedami Edit ir Add Recipe mygtukai.

![image](https://user-images.githubusercontent.com/113506949/196007240-64eee697-f895-4fb7-b675-c59352115f2d.png)

- Paspaudus Edit mygtuką nepasirinkus įrašo į Project_error_log failą įrašomas warning, jog bandoma editinti nepasirinkus įrašo. Paspaudus Edit mygtuką pasirinkus įrašą to įrašo ID paimamas į atmintį su kintamuoju, užkraunami 6 entry fields ir 6 labels. Į juos įrašomi dabartiniai įrašo duomenys. Pačio Edit mygtuko tekstas pakeičiamas į Save changes, o funkcija pakeičiama į įrašo išsaugojimą. Pridedamas Cancel mygtukas. Išjungiamas Delete mygtukas. Mygtuko Save changes pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko Cancel į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007244-ea94d7d6-5457-4c9e-922d-b0714e88bfeb.png)

- Paspaudus Save changes mygtuką Name laukas tikrinamas tokiu pačiu principu kaip ir Process lentelėje. Kiti laukai tikrinami ar yra teigiami, ar mažiau arba lygūs 1, ir ar jų suma lygi 1. Leidžiama nedidelė 0.0004 paklaida iki 1. Jei tikrinimai praeina, įrašas yra redaguojamas duomenų bazėje pagal ankščiau paimta įrašo ID. Atstatomi Edit, Add Recipe bei Delete mygtukai, atnaujinama lentelė, atnaujinamas Add an Order receptų pasirinkimo combobox.

- Paspaudus Cancel mygtuką pašalinami ir išvalomi visi Edit sukurti laukai, grąžinamas Edit mygtuko tekstas bei funkcija, bei Add Recipe mygtukas.

- Paspaudus Add Recipe mygtuką sukuriami 6 labels bei 6 entry field laukai. Visi tikrinimai atliekami tokie patys kaip ir redaguojant įrašą. Praėjus patikrinimus įrašas įrašomas į duomenų bazės Recipies lentelę ir atnaujinama treeview lentelė programoje tikrinant įrašų kiekį. Jei įrašų yra daugiau nei 8 - pridedamas scrollbar lentelės dešinėje pusėje. Mygtuko Save changes pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko Cancel į raudoną.

- Paspaudus Delete mygtuką jei nepasirinkta įrašas įrašomas į Project_error_log failą warning, jei pasirinktas - pasirinktas įrašas yra ištrinamas ir lentelė atnaujinama tikrinant įrašų kiekį. Jei įrašų yra daugiau nei 8 - pridedamas scrollbar lentelės dešinėje pusėje, atnaujinamas Add an Order receptų pasirinkimo combobox..

## 3) Storage:</br>
Paspaudus Storage mygtuką sukuriama treeview lentelė su duomenų bazės Storage duomenimis. Pridedami Edit, bei išjungtas Delete mygtukai.

![image](https://user-images.githubusercontent.com/113506949/196007255-d6e9fb21-a59d-413e-b0f5-d3fcb7162e5f.png)

- Paspaudus Edit mygtuką nepasirinkus įrašo į Project_error_log failą įrašomas warning, jog bandoma editinti nepasirinkus įrašo. Paspaudus Edit mygtuką pasirinkus įrašą to įrašo ID paimamas į atmintį su kintamuoju, užkraunami 2 entry fields ir 2 labels. Į entry fields iš kart įrašomi dabartiniai pasirinkto įrašo duomenys. Pačio Edit mygtuko tekstas pakeičiamas į Save changes, o funkcija pakeičiama į įrašo išsaugojimą. Pridedmas Cancel mygtukas. Mygtuko Save changes pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko Cancel į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007260-e0f12f59-539a-4776-8178-e3f165947913.png)

- Paspaudus Save changes mygtuką Name, bei Amount laukai tikrinami tokiu pačiu būdų kaip ir Process lentelėje. Praėjus tikrinimus įrašas pagal prieš tai paimtą įrašo ID yra redaguojamas duomenų bazės Storage lentelėje. Atstatomas Edit mygtukas, pašalinamas Cancel mygtukas, atnaujinama lentelė.

- Paspaudus Cancel mygtuką pašalinami ir išvalomi visi Edit sukurti laukai, grąžinamas Edit mygtuko tekstas bei funkcija.

## 4) Materials:</br>
Paspaudus Materials mygtuką sukuriama treeview lentelė su duomenų bazės Materials duomenimis. Pridedami Edit, bei išjungtas Delete mygtukai. Lentelės Price/kg stulpelis yra automatiškai apsakičiuojamas pagal pasirinktą valiutą. Lentelės atsinaujinimas pririšamas su Event prie valiutų combobox pasikeitimo ir pasikeitus įrašui perskaičiuojama kaina.

![image](https://user-images.githubusercontent.com/113506949/196007267-535abdb7-8219-4537-b594-e403df369ee8.png)

- Paspaudus Edit mygtuką nepasirinkus įrašo į Project_error_log failą įrašomas warning, jog bandoma editinti nepasirinkus įrašo. Paspaudus Edit mygtuką pasirinkus įrašą to įrašo ID paimamas į atmintį su kintamuoju, užkraunami 2 entry fields ir 2 labels. Į entry fields iš kart įrašomi dabartiniai pasirinkto įrašo duomenys. Pačio Edit mygtuko tekstas pakeičiamas į Save changes, o funkcija pakeičiama į įrašo išsaugojimą. Pridedmas Cancel mygtukas. Mygtuko Save changes pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko Cancel į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007275-428ea0aa-a8d5-4ca8-94f1-df2c99ad3fa9.png)

- Paspaudus Save changes mygtuką Name, bei Amount laukai tikrinami tokiu pačiu būdų kaip ir Process lentelėje. Praėjus tikrinimus įrašas pagal prieš tai paimtą įrašo ID yra redaguojamas duomenų bazės Storage lentelėje. Atstatomas Edit mygtukas, pašalinamas Cancel mygtukas, atnaujinama lentelė.

- Paspaudus Cancel mygtuką pašalinami ir išvalomi visi Edit sukurti laukai, grąžinamas Edit mygtuko tekstas bei funkcija.

## 5) Orders:</br>
Paspaudus Orders mygtuką sukuriama treeview lentelė su duomenų bazės Orders duomenimis. Pridedamas išjungtas Edit mygtukas, išjungtas Delete mygtukas, bei Filter mygtukas. Užvedus pelę ant Filter mygtuko jis nuspalvinamas pilka spalva. Lentelės atsinaujinimas pririšamas prie valiutų combobox pasikeitimo ir kiekvieną kartą pasikeitus atnaujinama lentelė ir perskaičiuojami Manufacturing cost ir Selling price stulpeliai pagal tos valiutos kursą.

![image](https://user-images.githubusercontent.com/113506949/196007278-4b32c3cb-8150-4ffb-bc57-40ab3bd7c8de.png)

- Paspaudus Filter mygtuką pridedamos etiketės bei combobox filtravimui. Į stulpelio From combobox sudedama data 2022-01-01, o į stulpelio To combobox sudedama dabartinė data kuri atsinaujina automatiškai. Taip pat pridedamas Period profit stulpelis kuriame automatiškai apskaičiuojama visos lentelės įrašų Selling price - Manufacturing price. Visi datų combobox pririšami prie lentelės įrašų atnaujinimo metodo pagal pasirinktą datų ruožą. Kiekvieną kartą pakeitus bet kurį combobox jų vertės paimamos, ir pagal tai dinamiškai išfiltruojami lentelės įrašai, atnaujinamas Period profit stulpelis. Filter mygtukas pakeičiamas į Cancel ir jo pelės užvedimo spalva pakeičiama į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007299-b412e31a-f79b-4b38-87b1-3ecdc35d1dce.png)

- Paspaudus Send to Email mygtuką visi tuo metu išfiltruoti lentelės įrašai yra sudedami į laišką, kurios Subject yra pasirinkta data From - To iš combobox, o turinys visi lentelės įrašai, bei Period profit. Duomenys naudojami siųsti laiškui paimami iš config.ini failo įrašant kam siunčiama, bei iš kokio email siunčiama priimant to email login bei gmail app key. Jei laiško išsiųsti nepavyksta metamas Error langas.

- Paspaudus Cancel mygtuką pašalinami ir išvalomi filtravimo laukai, grąžinamas Filter mygtukas ir jo pelės užvedimo spalva, atstatomas išjungtas Edit mygtukas.

## 6) Add an Order:</br>
Paspaudus Add an Order mygtuką Pridedamas combobox kuris yra užpildomas duomenų bazės Recipies lentelės pavadinimais, entry field, bei du mygtukai Confirm Order ir Cancel Order.

![image](https://user-images.githubusercontent.com/113506949/196007317-a03ec294-222a-4abe-b9fd-8fc9809c2993.png)

- Paspaudus Confirm Order mygtuką yra tikrinama ar į amount entry field įrašytas skaičius, tada ar pasirinktas receptas, tada ar įrašytas skaičius didesnis už 0. Jeigu ne, meta atitinkamą error, jei patikrinimai praeina, paimamas receptas pagal pagal combobox pasirinkimą ir pagal receptui reikiamą žaliavų kiekį ir įrašytą užsakymo kiekį skaičiuojama ar užteks žaliavų užsakymui įvykdyti. Jei taip, užsakymas įrašomas į duomenų bazę, į orders failą įrašoma užsakymo informacija, iš Storage lentelės nurašomi žaliavų kiekiai kurių reikėjo užsakymui įvykdyti, tada tikrinima ar Mail orders combobox pasirinkimas yra YES. Jei taip, nusiunčiamas laiškas imant paštą, bei adresatą iš config.ini failo, su atlikto užsakymo informacija. Jei žaliavų užsakymui įvykdyti nepakanka, pagal duomenų bazės Processes lentelės efficiency skaičiuojama kiek darbo valandų reikėtų, kad būtų pagaminta pakankamai žaliavos užsakymui įvykdyti. Tada metamas Error langas su šia informacija, įrašomas Error į Process_error_log failą.

- Paspaudus Cancel Order mygtuką pašalinami sukurti langai, išvalomas Amount in kg entry field, bei Recipe combobox.
