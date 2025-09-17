################################################################################
## Dette er et enkelt program som viser eksempel på
## generering av HTML med Python
################################################################################

import re

# En slags "Enum" for id av tag type
TAG_PAIR = 0
TAG_SING = 1


# Globale variabler
settings = {}
pages = []
footer = []
lorem_p = (TAG_SING, '<p>Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.</p>')


# Entry-point for programmet
def main():
    init()
    for page in pages:
        gen_page(page)


# Initalisering av variabler
def init():
    global settings
    global footer
    global pages
    # Nettside instillinger
    settings = {
            'root': './',
            'title': 'Regnbyen Bergen A/S',
        }
    # Footer innhold
    footer = [
            (TAG_SING, '<p>Regnbyen Bergen A/S, Postboks 333, 5779 Stedplass, Norge<br>Tel: 77 42 23 82&nbsp;&nbsp;&#8226;&nbsp;&nbsp;E-post: <a href="mailto:post@eksempel.no">post@eksempel.no</a></p>'),
        ]
    # Nettsidens forskjellige sider
    pages = [
            {
                'title': 'Hjem',       'id': 'index',     'anim': 'rb',      'content': [
                    ((TAG_PAIR), '<section>'),
                    ((TAG_SING), '<h2>Hjem</h2>'),
                    lorem_p,
                    lorem_p,
                ],
            },
            {
                'title': 'Prosjektet', 'id': 'om',        'anim': 'info',    'content': [
                    ((TAG_PAIR), '<section>'),
                    ((TAG_SING), '<h2>Om prosjektet</h2>'),
                    lorem_p,
                    lorem_p,
                ],
            },
            {
                'title': 'Løsninger',  'id': 'losninger', 'anim': 'kode',    'content': [
                    ((TAG_PAIR), '<section>'),
                    ((TAG_SING), '<h2>Løsninger</h2>'),
                    lorem_p,
                    lorem_p,
                ],
            },
            {
                'title': 'Samarbeid',  'id': 'samarbeid', 'anim': 'regn',    'content': [
                    ((TAG_PAIR), '<section>'),
                    ((TAG_SING), '<h2>Samarbeidspartnere</h2>'),
                    lorem_p,
                    lorem_p,
                ],
            },
            {
                'title': 'Kontakt',    'id': 'kontakt',   'anim': 'stats',   'content': [
                    ((TAG_PAIR), '<section>'),
                    ((TAG_SING), '<h2>Kontakt oss</h2>'),
                    lorem_p,
                    lorem_p,
                ],
            },
        ]

# Generering av html fil
def gen_page(page):
    # Lage nav elementene
    nav_tags = [ (TAG_PAIR, '<ul>') ]
    for nav_page in pages:
        nav_tags.append( (TAG_SING, '<li>' + ( '<a href="' + settings['root'] + nav_page['id'] + '.html">' + nav_page['title'] + '</a>' if nav_page != page else nav_page['title'] ) + '</li>') )
    # Liste over tags som skal inkluderes
    tags =  [
                (TAG_SING, '<!DOCTYPE html>'),
                (TAG_PAIR, '<html lang = "no">'),
                [ 
                    (TAG_PAIR, '<head>'), 
                    (TAG_SING, '<meta charset="utf-8">'),
                    (TAG_SING, '<meta name="viewport" content="width=device-width, initial-scale=1.0">'), 
                    (TAG_SING, '<title>' + settings['title'] + ' - ' + page['title'] + '</title>'),
                    (TAG_SING, '<link rel="icon" href="' + settings['root'] + 'img/favicon.png">'),
                    (TAG_SING, '<link rel="stylesheet" href="' + settings['root'] + 'main.css">'),
                ],
                [ 
                    (TAG_PAIR, '<body>') ,
                    (TAG_PAIR, '<div id="outer-wrapper">'),
                    [
                        (TAG_PAIR, '<div id="left-wrapper">'),
                        [
                            (TAG_PAIR, '<header>'),
                            (TAG_SING, '<img src="' + settings['root'] + 'img/anim/' + page['anim'] + '.gif">'),
                        ],
                        [
                            (TAG_PAIR, '<nav>'),
                            nav_tags,
                        ],
                    ],
                    [
                        (TAG_PAIR, '<div id="right-wrapper">'),
                        [
                            [
                                (TAG_PAIR, '<main>'),
                                [
                                    page['content'],
                                ],
                            ],
                            (TAG_PAIR, '<footer>'),
                            footer,
                        ],
                    ],
                ],
            ]
    # Skriv tags til html fil
    with open(page['id'] + '.html', 'w') as f:
        process_tags(f, tags)


# Gå gjennom en liste av tags og gjør om til html
def process_tags(f, tags, indent = 0):
    consumed_pairs = []
    # Gjennomgang av alle liste elementer
    for tag in tags:
        # Rekursivt kall hvis elementet er en liste
        if isinstance(tag, list):
            process_tags(f, tag, indent)
        # Behanding av elementet
        else:
            tag_type = tag[0]
            tag = tag[1]
            f.write(('  ' * (indent)) + tag+'\n')
            # Hvis elementet er et par økes indent og elementet legges til en liste over tagger som må lukkes
            if tag_type == TAG_PAIR:
                indent+= 1
                consumed_pairs.insert(0, tag)
    # Gå gjennom listen over tagger som må lukkes
    for i, tag in enumerate(consumed_pairs):
        re_match = re.search(r'\<([a-z]+)', tag)
        if re_match:
            tag = re_match.group(1)
            indent-=1
            f.write(('  ' * indent) + '</'+tag+'>\n')


# Kall på main funksjonen
if __name__ == '__main__':
    main()
