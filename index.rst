--- Project information -----------------------------------------------------

project = 'pymino'
copyright = '2022 forevercynical'
author = 'Cynical'
release = '0.0.3'


--- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': True,
    'display_version': False,
    'style_nav_header_background': '#2f3136',
    'style_external_links': True,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'titles_only': False
}

html_logo = 'images/logo.png'
html_favicon = 'images/favicon.ico'
html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]

html_context = {
    'display_github': True,
    'github_user': 'forevercynical',
    'github_repo': 'pymino',
    'github_version': 'main/docs/',
    'conf_py_path': '/docs/',
}

html_show_sourcelink = False
html_show_sphinx = False

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
        'donate.html',
    ]
}

html_last_updated_fmt = '%b %d, %Y'

html_copy_source = False

html_show_sphinx = False

html_show_sourcelink = False






