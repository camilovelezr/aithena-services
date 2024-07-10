# pylint: disable=W0106
import dataclasses
from pathlib import Path
from typing import Callable, cast

import numpy as np
import plotly.express as px
import solara
from polus.ai.db.qdrant_db import DB
from polus.ai.services.visualize import cluster, reduce

SNAPSHOT_FILE: Path = Path("/Users/camilovelezr/arxiv.snapshot")
collection_name = "arxiv"

db = DB(port=6333)
db.upload_snapshot(SNAPSHOT_FILE, collection_name)


offset = 0
records = []
# download all records related to documents
while offset is not None:
    page_rec = db.client.scroll(
        collection_name=collection_name,
        limit=1000,
        offset=offset,
        with_payload=True,
        with_vectors=True,
    )

    offset = page_rec[1]
    records += page_rec[0]

total_count = len(records)
assert total_count == 76

vectors = np.array([record.vector for record in records])


options = {
    "n_components": 2,  # output dimensions
    "metric": "cosine",
    "min_dist": 0.0,
    "n_neighbors": 2,
}

reduced_embeddings = reduce(vectors, options)

"""
Clustering
"""
options = {
    "min_samples": 2,
    "min_cluster_size": 2,
    # 'max_cluster_size' : 20
}

all_data = cluster(reduced_embeddings, options)

columns = ["0", "1"]


@dataclasses.dataclass
class ClickPoint:
    row_index: int


@dataclasses.dataclass
class MultipleClickPoints:
    row_index: list[int]


@solara.component
def ClickScatter(
    reduced,
    x,
    y,
    color,
    on_click: Callable[[ClickPoint], None],
    on_select: Callable[[MultipleClickPoints], None],
):
    x, set_x = solara.use_state(x)
    y, set_y = solara.use_state(y)
    fig = px.scatter(reduced, x, y, color=color)

    def on_click_trace(click_data):
        # sanity checks
        assert click_data["event_type"] == "plotly_click"
        row_index = click_data["points"]["point_indexes"][0]
        on_click(ClickPoint(row_index))

    def on_select_trace(select_data):
        print(select_data)
        row_indices = select_data["points"]["point_indexes"]
        on_select(MultipleClickPoints(row_indices))

    return solara.FigurePlotly(
        fig, on_click=on_click_trace, on_selection=on_select_trace
    )


def get_author_names(authors):
    return ", ".join([author["author"][0]["keyname"] for author in authors])


@solara.component
def RecordInfo(record):
    """Display the information of a record."""
    authors_ = get_author_names(record.payload["authors"])
    with solara.Column(style={"padding-left": "10px"}, gap="6px") as main:
        solara.Markdown(f"# {record.payload['title'][0]}"),
        solara.Markdown(f"## {authors_}"),
        solara.Markdown(f"{record.payload['abstract'][0]}"),
    return main


@solara.component
def MultipleRecordInfo(records_list, indices):
    """Display the information of multiple records."""
    records_ = [records_list[i] for i in indices]
    with solara.Column(style={"padding-left": "10px"}, gap="0px") as main:
        for record in records_:
            solara.Markdown("---")
            RecordInfo(record)
    return main


@solara.component
def Page():
    click_point, set_click_point = solara.use_state(cast(ClickPoint, None))
    multiple_click_points, set_multiple_click_points = solara.use_state(
        cast(MultipleClickPoints, None)
    )
    if click_point:
        clicked_row = click_point.row_index
    if multiple_click_points:
        clicked_rows = multiple_click_points.row_index
    else:
        clicked_row = None
        clicked_rows = None

    with solara.Column(style={"width": "100%", "height": "100%"}) as main:
        with solara.Row(
            style={
                "position": "relative",
                "width": "50%",
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
            }
        ):
            ClickScatter(
                reduced_embeddings,
                0,
                1,
                all_data,
                on_click=set_click_point,
                on_select=set_multiple_click_points,
            )
        if click_point is not None and multiple_click_points is None:
            clicked_row = click_point.row_index
            solara.Success(f"Clicked on row {click_point}.")
            RecordInfo(records[clicked_row])
        if multiple_click_points is not None:
            clicked_rows = multiple_click_points.row_index
            solara.Success(f"Clicked on rows {multiple_click_points}.")
            MultipleRecordInfo(records, clicked_rows)
        if multiple_click_points is None and click_point is None:
            solara.Info("Click to select a point")

    return main
