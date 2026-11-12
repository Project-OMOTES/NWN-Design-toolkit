# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'NWN design toolkit'
copyright = '2026, S. van der Zwan'
author = 'S. van der Zwan'
release = '0.9.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']

# Brand styling inspired by https://nwn.nu/ (Nieuwe Warmte Nu).
# Palette: dark teal-blue text, green/orange/red accents.
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#1b5c2a",      # dark green
        "color-brand-content": "#2d9645",      # green
        "color-foreground-primary": "#163941", # dark blue text
        "color-foreground-secondary": "#3a5d66",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f3f8f4",
        "color-sidebar-background": "#f3f8f4",
        "color-admonition-title-background--note": "#e2f6e7",
        "color-admonition-title--note": "#1b5c2a",
        "font-stack": "Alegreya Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
        "font-stack--headings": "Alegreya, Georgia, serif",
        "font-stack--monospace": "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
    },
    "dark_css_variables": {
        "color-brand-primary": "#7bdcb5",
        "color-brand-content": "#7bdcb5",
        "color-foreground-primary": "#e6efe8",
        "color-background-primary": "#11272d",
        "color-background-secondary": "#163941",
        "color-sidebar-background": "#163941",
        "font-stack": "Alegreya Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
        "font-stack--headings": "Alegreya, Georgia, serif",
    },
}
