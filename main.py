#!/usr/bin/python
"""
This example shows the functionality of the Tabu and LongTabu element.
..  :copyright: (c) 2016 by Vladimir Gorovikov and Scott Wallace
    :license: MIT, see License for more details.
"""

# begin-doc-include
import copy
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

snapshot_names = {
    "Axis": "avig",
    "Avigilon": "axis",
    "IMX 290": "290",
    "IMX 335 Narrow": "narrow_335",
    "IMX 335 Wide": "wide_335",
}
VIDEOS = ["14", "15", "16", "17", "18", "19", "24"]


def hyperlink(url, text):
    text = escape_latex(text)
    return NoEscape(r"\href{" + url + "}{" + text + "}")


def generate_shootout_table():
    geometry_options = {
        "margin": ".5in",
        "headheight": "20pt",
        "headsep": "10pt",
        "includeheadfoot": True,
    }
    doc = Document(page_numbers=False, geometry_options=geometry_options)

    # Generate data table with 'tight' columns
    fmt = "m{2.5cm} m{4cm} m{2cm} m{4cm} m{2cm} m{2cm}"
    with doc.create(LongTabu(fmt, row_height="2")) as data_table:
        header_row1 = [
            "Capture ID",
            "Image",
            "Camera",
            "Description",
            "Lighting",
            "IR",
        ]
        data_table.add_row(header_row1, mapper=[bold])
        data_table.add_hline()
        data_table.add_empty_row()
        data_table.end_table_header()

        for capture in experiment_data:
            for i, camera_data in enumerate(experiment_data[capture]):
                if i == 0:
                    r = [
                        capture,
                        StandAloneGraphic(
                            image_options="width=100px",
                            filename=f"./snapshots/thumbnail_{capture}_{snapshot_names[camera_data['camera']]}.jpg",
                        ),
                        hyperlink("https://google.com", camera_data["camera"]),
                        camera_data["description"],
                        camera_data["lighting"],
                        camera_data["ir"],
                    ]
                else:
                    r = [
                        "",
                        StandAloneGraphic(
                            image_options="width=100px",
                            filename=f"./snapshots/thumbnail_{capture}_{snapshot_names[camera_data['camera']]}.jpg",
                        ),
                        hyperlink("https://google.com", camera_data["camera"]),
                        "",
                        "",
                        "",
                    ]
                if capture in VIDEOS:
                    r[1] = ""
                data_table.add_row(r)
                data_table.add_empty_row()

            data_table.add_empty_row()
            data_table.add_hline()
            data_table.add_empty_row()

    doc.packages.append(Package("hyperref"))
    doc.packages.append(Package("array"))
    doc.generate_pdf("shootout_table", clean_tex=False)


generate_shootout_table()
