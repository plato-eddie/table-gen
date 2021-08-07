#!/usr/bin/python
"""
This example shows the functionality of the Tabu and LongTabu element.
..  :copyright: (c) 2016 by Vladimir Gorovikov and Scott Wallace
    :license: MIT, see License for more details.
"""

# begin-doc-include
import json
from random import randint
from pylatex import (
    Document,
    LongTabu,
    Hyperref,
    StandAloneGraphic,
    Package,
)
from pylatex.utils import bold, NoEscape
from copy import deepcopy
from pylatex.utils import escape_latex, NoEscape

# import data

with open("./experiment.json", "r") as fin:
    experiment_data = json.load(fin)


experiment_data_grouped = {}
for dat in experiment_data:
    if not experiment_data_grouped.get(dat.get("id")):
        experiment_data_grouped[dat.get("id")] = []
    experiment_data_grouped[dat.get("id")].append(dat)





def hyperlink(url, text):
    text = escape_latex(text)
    return NoEscape(r"\href{" + url + "}{" + text + "}")


def genenerate_tabus():
    geometry_options = {
        "landscape": True,
        "margin": ".5in",
        "headheight": "20pt",
        "headsep": "10pt",
        "includeheadfoot": True,
    }
    doc = Document(page_numbers=False, geometry_options=geometry_options)

    # Generate data table with 'tight' columns
    fmt = "m{2.5cm} m{4cm} m{2cm} m{2cm} m{2cm} m{2cm} m{2cm}"
    with doc.create(LongTabu(fmt, row_height="2")) as data_table:
        header_row1 = [
            "Capture ID",
            "Image",
            "Camera",
            "Notes",
            "Scene",
            "Lighting",
            "IR",
        ]
        data_table.add_row(header_row1, mapper=[bold])
        data_table.add_hline()
        data_table.add_empty_row()
        data_table.end_table_header()
        row = [
            "0",
            StandAloneGraphic(
                image_options="width=100px", filename="../thumbnail_1_290.jpg"
            ),
            hyperlink("https://google.com", "IMX"),
            "$100",
            "%10",
            "$1000",
            "Test",
        ]
        for i in range(8):
            r = deepcopy(row)
            if i % 4 != 0:
                r[0] = ""
                data_table.add_empty_row()

            elif i != 0:
                data_table.add_empty_row()
                data_table.add_hline()
                data_table.add_empty_row()
            data_table.add_row(r)

    doc.packages.append(Package("hyperref"))
    doc.packages.append(Package("array"))
    doc.generate_pdf("tabus", clean_tex=False)


# genenerate_tabus()
