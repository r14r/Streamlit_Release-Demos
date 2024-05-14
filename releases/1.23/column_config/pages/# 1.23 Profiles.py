import random
from datetime import date

import numpy as np
import pandas as pd
import streamlit as st
from utils import icon

st.set_page_config("Profiles", "👤")
icon("👤")
"""
# Profiles

This page shows some fake profile data. It shows the full range of column types
and uses a ton of customization. 

Column config features used:

- All column types, including image, chart, progress, and link columns
- Input validation when editing, e.g. min/max values, regex validation of strings
- Tooltips
"""


@st.cache_data
def get_profile_dataset(number_of_items: int = 100, seed: int = 0) -> pd.DataFrame:
    new_data = []

    def calculate_age(born):
        today = date.today()
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    from faker import Faker

    fake = Faker()
    random.seed(seed)
    Faker.seed(seed)

    for i in range(number_of_items):
        profile = fake.profile()
        new_data.append(
            {
                "name": profile["name"],
                "avatar": f"https://picsum.photos/400/200?lock={i}",
                "age": calculate_age(profile["birthdate"]),
                "gender": random.choice(["male", "female", "other", None]),
                "active": random.choice([True, False]),
                "homepage": profile["website"][0],
                "email": profile["mail"],
                "activity": np.random.randint(2, 90, size=25),
                "daily_activity": np.random.rand(25),
                "birthdate": profile["birthdate"],
                "status": round(random.uniform(0, 1), 2),
            }
        )

    profile_df = pd.DataFrame(new_data)
    profile_df["gender"] = profile_df["gender"].astype("category")
    return profile_df


col1, col2 = st.columns(2)
editable = col1.checkbox("Make it editable", value=False)
new_rows = col2.checkbox("Let me add new rows", value=False, disabled=not editable)

table = st.empty()

with st.echo("below"):
    column_configuration = {
        "name": st.column_config.TextColumn(
            "Name", help="The name of the user", max_chars=100
        ),
        "avatar": st.column_config.ImageColumn("Avatar", help="The user's avatar"),
        "active": st.column_config.CheckboxColumn(
            "Is Active?", help="Is the user active?"
        ),
        "homepage": st.column_config.LinkColumn(
            "Homepage", help="The homepage of the user"
        ),
        "gender": st.column_config.SelectboxColumn(
            "Gender", options=["male", "female", "other"]
        ),
        "age": st.column_config.NumberColumn(
            "Age",
            min_value=0,
            max_value=120,
            format="%d years",
            help="The user's age",
        ),
        "activity": st.column_config.LineChartColumn(
            "Activity (1 year)",
            help="The user's activity over the last 1 year",
            width="large",
            y_min=0,
            y_max=100,
        ),
        "daily_activity": st.column_config.BarChartColumn(
            "Activity (daily)",
            help="The user's activity in the last 25 days",
            width="medium",
            y_min=0,
            y_max=1,
        ),
        "status": st.column_config.ProgressColumn(
            "Status", min_value=0, max_value=1, format="%.2f"
        ),
        "birthdate": st.column_config.DateColumn(
            "Birthdate",
            help="The user's birthdate",
            min_value=date(1920, 1, 1),
        ),
        "email": st.column_config.TextColumn(
            "Email",
            help="The user's email address",
            validate="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",
        ),
    }


if editable:
    edited_data = table.data_editor(
        get_profile_dataset(),
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic" if new_rows else "fixed",
    )

    with st.expander("Edited Data"):
        st.dataframe(edited_data, use_container_width=True)

else:
    table.dataframe(
        get_profile_dataset(),
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
    )
