import re
from enum import Enum

TAG_PAIR = 0
TAG_SING = 1

'''
          <section>
            <h2>Hjem</h2>
            <p>Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.</p>
            <p>Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.</p>
            <div class="imgs">
              <img class="bg" alt="vaerfenomen" src="./img/nedbor-arlig.png">
              <img class="bg" alt="vaerfenomen" src="./img/vaerfenomen.png">
              <img class="bg" alt="vaerfenomen" src="./img/nedbor-2023.png">
              <img class="bg" alt="vaerfenomen" src="./img/nedbor-2024.png">
            </div>
            <p>Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.</p>
            <p>Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.</p>
          </section>
'''

content = {
    'index': [],
    'om': [],
    'losninger': [],
    'produkter': [],
    'samarbeid': [],
    'kontakt': [],
    }

settings = {
    'root': './',
    'title': 'Regnbyen Bergen A/S',
    }

nav =   [
    ('Hjem',       'index',     'rb'),
    ('Prosjektet', 'om',        'info'),
    ('Løsninger',  'losninger', 'kode'),
    ('Produkter',  'produkter', 'produkt'),
    ('Samarbeid',  'samarbeid', 'regn'),
    ('Kontakt',    'kontakt',   'stats'),
    ]

def main():
    for page in nav:
        gen_page(page)

def gen_page(page):
    nav_tags = [ (TAG_PAIR, '<ul>') ]
    for entry in nav:
        nav_tags.append( (TAG_SING, '<li>' + ( '<a href="' + settings['root'] + entry[1] + '.html">' + entry[0] + '</a>' if entry != page else entry[0] ) + '</li>') )

    tags =  [
                (TAG_SING, '<!DOCTYPE html>'),
                (TAG_PAIR, '<html lang = "no">'),
                [ 
                    (TAG_PAIR, '<head>'), 
                    (TAG_SING, '<meta charset="utf-8">'),
                    (TAG_SING, '<meta name="viewport" content="width=device-width, initial-scale=1.0">'), 
                    (TAG_SING, '<title>' + settings['title'] + '</title>'),
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
                            (TAG_SING, '<img src="' + settings['root'] + 'img/anim/' + page[2] + '.gif">'),
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
                                    content[page[1]]
                                ],
                            ],
                            (TAG_PAIR, '<footer>'),
                            [
                                (TAG_SING, '<p>Regnbyen Bergen A/S, Postboks 333, 5779 Stedplass, Norge<br>Tel: 77 42 23 82&nbsp;&nbsp;&#8226;&nbsp;&nbsp;E-post: <a href="mailto:post@eksempel.no">post@eksempel.no</a></p>'),
                            ],
                        ],
                    ],
                ],
            ]

    with open(page[1] + '.html', 'w') as f:
        process_tags(f, tags)

#
def process_tags(f, tags, indent = 0):
    consumed_pairs = []
    # ...
    for tag in tags:
        # ...
        if isinstance(tag, list):
            process_tags(f, tag, indent)
        # ...
        else:
            tag_type = tag[0]
            tag = tag[1]
            f.write(('  ' * (indent)) + tag+'\n')
            # ...
            if tag_type == TAG_PAIR:
                indent+= 1
                consumed_pairs.insert(0, tag)
    # ...
    for i, tag in enumerate(consumed_pairs):
        re_match = re.search(r'\<([a-z]+)', tag)
        if re_match:
            tag = re_match.group(1)
            f.write(('  ' * (len(consumed_pairs) - (i+1) + (indent-1))) + '</'+tag+'>\n')

if __name__ == '__main__':
    main()
