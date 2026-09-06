# TET4100 Elektriske Kretser – SLT-1 (Semester Learning Task 1)
**Institutt for elektrisk energi, NTNU**

Dette prosjektet inneholder en komplett interaktiv web-presentasjon, pedagogiske visualiseringer, Python-skript for figurproduksjon og en dyptgående teoretisk løsningsguide for **SLT-1** i emnet **TET4100 Elektriske Kretser**.

---

## 🚀 Hurtigstart: Slik åpner du presentasjonen

Du har to enkle måter å starte presentasjonen på:

### Metode 1: Direkte oppstart (Anbefalt)
Dobbeltklikk på:
- **`START_PRESENTASJON.bat`**  
Åpner `presentation/index.html` direkte i standard nettleser (Chrome, Edge, Firefox, osv.).

### Metode 2: Lokal Webserver (Python HTTP-server)
Dobbeltklikk på:
- **`START_SERVER.bat`**  
Starter en lokal webserver på `http://localhost:8080` og åpner presentasjonen automatisk. Dette er nyttig dersom nettleseren din har strenge CORS-restriksjoner på lokale filer.

### Metode 3: Publisering på Vercel (Online)
Prosjektet er ferdig konfigurert med `vercel.json` og rot-omdirigering:
1. Push koden til GitHub:
   ```bash
   git push -u origin main
   ```
2. Gå til [Vercel](https://vercel.com) og trykk **Add New Project**.
3. Importer GitHub-repositoriet **`SLT-1-github`**.
4. La alle innstillinger stå som standard (Root Directory: `./`, Framework: Other) og klikk **Deploy**.
5. Vercel vil automatisk vise presentasjonen på prosjektets URL!

---

## 📁 Mappestruktur

```text
SLT-1-github/
├── README.md                      # Denne oversiktsguiden
├── vercel.json                    # Vercel-konfigurasjon for omdirigering til presentasjonen
├── index.html                     # Rot-omdirigering til presentation/index.html
├── START_PRESENTASJON.bat         # Oppstartsskript for nettleser
├── START_SERVER.bat               # Oppstartsskript for lokal webserver
├── SLT1_Komplett_Oversikt.md      # Komplett faglig kompendium med utledninger og MATLAB-koder
├── .gitignore                     # Git-ignoreringsregler
│
├── presentation/                  # Interaktiv foilpresentasjon
│   ├── index.html                 # Hovedside med foiler, KaTeX-matematikk og navigasjon
│   ├── style.css                  # Lys, moderne designstil (NTNU-farger, kortoppsett)
│   └── app.js                     # Tastaturstyring (piltaster), fullskjerm og meny
│
├── assets/                        # Alle grafiske illustrasjoner og diagrammer
│   ├── circuits/                  # Kretsskjemaer for Task 1–6 (tegnet med SchemDraw)
│   ├── plots/                     # Analytiske og numeriske transientkurver (Matplotlib)
│   └── images/                    # Reelle industribilder (relé/flyback, forladingskrets, mikrokontroller)
│
├── scripts/                       # Python-kildekode for å generere figurer på nytt
│   ├── generate_plots.py          # Genererer alle plott i assets/plots/
│   ├── generate_circuit_diagrams.py # Tegner kretser i assets/circuits/
│   └── requirements-figures.txt   # Pakkekrav (numpy, matplotlib, schemdraw)
│
└── dist/                          # Distribusjons- og delingsarkiv
    └── TET4100_SLT1_Presentasjon.zip # Komplett pakket prosjekt klart for deling
```

---

## 📚 Faglig Innhold (Task 1 til 6)

1. **Task 1: Basic RL Transient & Inductive Flyback**
   - Bryteråpning i RL-krets, kontinuitet av spolestrøm ($i_L(0^-) = i_L(0^+) = 1.5\text{ A}$).
   - Generering av flyback-spenningsspiss ($v_L(0^+) = -72\text{ V}$) og beskyttelse med frihjulsdiode.
2. **Task 2: Sequential Switching RC**
   - To-trinns opplading og utlading ($+10\text{ V} \to -20\text{ V}$).
   - Kontinuitet av kondensatorspenning ($v_C(\tau^+) = 6.321\text{ V}$) mot diskontinuerlig strømsjokk ($i(\tau^+) = -26.32\text{ mA}$).
3. **Task 3: Dynamisk System & Stabilitet**
   - Aktiv krets med avhengig strømkilde ($7i_\Delta$).
   - Negativ konduktans og egenverdier: Ustabil med $R_1 = 10\text{ k}\Omega$ ($\lambda = +40\text{ s}^{-1}$), stabil med $R_1 = 2\text{ k}\Omega$ ($\lambda = -40\text{ s}^{-1}$).
4. **Task 4: Ladningsutveksling mellom to kondensatorer**
   - Visning av at to kondensatorer i serie danner et 1. ordens system på grunn av ladningsbevaring.
   - *To-kondensator-paradokset*: 90 % av startenergien tapes som varme, uansett motstandsverdi $R$. Sammenheng med forladingskretser (pre-charge) i elbiler.
5. **Task 5: Likevektsstyring (Open-Loop Feedforward)**
   - Styring av induktiv last via forhåndsberegnet kildespenning $\bar{u} = (R_{\text{load}} - k)i^{\text{ref}} = 12\text{ V}$.
   - Stabilitetskrav ($k < R_{\text{load}}$).
6. **Task 6: Likevektsgjenoppretting (Digital PI-regulering)**
   - Hvorfor åpen sløyfe feiler katastrofalt når lasten endres til $4\,\Omega$ ($i \to 12\text{ A}$).
   - Andreordens dynamikk med RC-feedback og bevis på at integralleddet tvinger stasjonær strøm til nøyaktig $I_{\text{ref}} = 4\text{ A}$ uavhengig av parametere.
   - Kartlegging til klassisk digital PI-regulator ($K_p = R_1 = 6\,\Omega$, $K_i = 1/C = 6.67\text{ s}^{-1}$).

---

## 🛠️ Reproduksjon av Figurer

Dersom du ønsker å generere plottene og kretsskjemaene på nytt:
```bash
cd scripts
pip install -r requirements-figures.txt
python generate_circuit_diagrams.py
python generate_plots.py
```
Alle figurer eksporteres automatisk i høy oppløsning til `assets/circuits/` og `assets/plots/`.
