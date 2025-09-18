////////////////////////////////////////////////////////////////////////////////
// Enkelt JavaScript program for generering av historie
////////////////////////////////////////////////////////////////////////////////

// Velg et tilfeldig element fra en tabell
function rand(array) {
  return array[Math.floor(Math.random() * array.length)];
}

// Generering av tilfeldig navn
function genName() {
  var name = ""
  const charsAll = 'abcdefghijklmnopqrstuvwxyz';
  const charsCommon = 'aeou';
  const charsUncommon = 'bcdfghijklmnrstv';
  const charsRare = 'xyzq';
  const length = Math.floor(Math.max(3, Math.random() * 8));
  for (var i = 0; i < length; i++) {

    const chars = i > 0 ? (Math.random() < 0.6 ? charsCommon : (Math.random() < 0.7 ?  charsUncommon : charsRare)) : charsAll;
    var char = chars.charAt(Math.floor(Math.random() * chars.length));
    name += char;
  }
  return name;
}


////////////////////////////////////////////////////////////////////////////////
// Oppsett av de forskjellige historie elementene
////////////////////////////////////////////////////////////////////////////////

const adjectives = [
  "gamle",
  "snille",
  "kloke",
  "rare",
  "lille",
  "underlige",
  "mektige",
  "modige",
]

const charactersDen = [
  "mannen",
  "gnomen",
  "hunden",
  "trollmannen",
  "frosken",
]; 

const charactersDet = [
  "trollet",
  "piggsvinet",
];

const actions = [
  "reiste til",
  "dro til",
  "la ut på reise til",
  "ferdes til",
  "begav seg ut på en reise til",
];

const locations = [
  "det gamle slottet",
  "det gamle fortet",
  "den grufulle skyggedalen",
  "den uendelige ørkenen",
  "det urgamle treet",
  "det magiske tårnet",
  "den mekaniske skogen",
  "de underjordiske skapningenes rike"
];

const goal = [
  "på søken etter den hellige amuletten",
  "i søk etter det savnete orakelet",
  "på et viktig oppdrag for å finne den mystiske boken",
];

const encounter = [
  "underveis møtte $name to kloke dverger som delte et måltid og ga gode råd for ferden videre",
  "underveis i ferden måtte $name beseire femten draugr og den lure kjempen \"$name2\" i kamp",
  "underveis i reisen måtte $name beseire den magiske ormen \"$name2\", som gikk til angrep under seilaset over den bunnløse elven",
  "underveis i ferden ble $name plaget av onde gjenferd nær den gamle slagmarken",
  "$name fikk hjelp på ferden av den enorme ulven \"$name2\", som ga beskyttelse og viste vei"
];

const arrival = [
  "etter femogfemti dagers utfordrende reise kom $name endelig frem til $location, og slo leir nær et forlatt tempel",
  "etter utmattende reise over fireogtyve fjell og tretten elver kom $name endelig frem til $location",
  "etter krevende reise gjennom de urgamles domene, kom $name endelig frem til $location",
  "etter å ha krysset femten sjøer, og bekjempet de åtte urgamle skapningene kom $name endelig frem til $location"
];


////////////////////////////////////////////////////////////////////////////////
// Sammensetting av de forskjellige historie elementene
////////////////////////////////////////////////////////////////////////////////

const name = genName();
const loc = rand(locations);
var den = Math.random() < 0.5;
var storyElements = [];
storyElements.push(den ? "Den" : "Det");
storyElements.push(rand(adjectives));
storyElements.push(den ? rand(charactersDen) : rand(charactersDet));
storyElements.push("som het \"" + name + "\"")
storyElements.push(rand(actions));
storyElements.push(loc + ",");
storyElements.push(rand(goal));
storyElements.push(".");
storyElements.push(rand(encounter).replace("$name2", genName()) + ", og");
storyElements.push(rand(arrival));
storyElements.push(".");

// Lag story streng fra elementene
var story = "";
for (var i = 0; i < storyElements.length; i++) {
  story += storyElements[i];
  if (storyElements[i+1 % storyElements.length] != ".") { story += " "; }
}

// Oppdater "story" containeren med story strengen
document.getElementById('story').innerHTML = story.replaceAll("$name", name).replaceAll("$location", loc).toUpperCase();
