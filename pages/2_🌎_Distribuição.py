import pandas as pd
import plotly.express as px
import streamlit as st
from typing import List

st.set_page_config(
    page_title="Distribuição Geográfica",
    page_icon="🗺",
    layout="wide",
)

colunas = [
    "Area Code",
    "Area",
    "Item Code",
    "Item",
    "Element Code",
    "Element",
    "Unit",
    "Continent",
    "Alpha 2",
    "Alpha 3",
]


def aplicar_filtros(data_frame: pd.DataFrame) -> pd.DataFrame:
    # Filtro de continente
    continentes: List[str] = data_frame["Continent"].unique().tolist()
    st.session_state["continente_selecionado"] = st.sidebar.multiselect(
        "Continente",
        continentes,
        help="Selecione pelo menos 1 continente",
        default=continentes,
    )
    data_frame = data_frame[
        data_frame["Continent"].isin(st.session_state["continente_selecionado"])
    ]

    # Filtro de ano
    anos: list = (
        data_frame.select_dtypes(include="number")
        .iloc[:, 3:]
        .columns.sort_values(ascending=False)
    )
    st.session_state["ano_selecionado"] = st.sidebar.selectbox(
        "Ano", anos, help="Selecione 1 ano para analisar"
    )
    data_frame = pd.concat(
        [data_frame[colunas], data_frame[st.session_state["ano_selecionado"]]], axis=1
    )

    # Filtro de campo
    campo: list = data_frame["Element"].unique().tolist()
    st.session_state["elemento_selecionado"] = st.sidebar.multiselect(
        "Elemento",
        campo,
        help="Selecione 1 meio de plantação para analisar",
        default=campo,
    )
    data_frame = data_frame[
        data_frame["Element"].isin(st.session_state["elemento_selecionado"])
    ]

    # Filtro de número de itens
    num_items = st.sidebar.slider('Items', min_value=1, max_value=20, value=5, help="Selecione o número de itens em ordem decrescente de produção.")
    st.session_state["num_items"] = num_items
    
    return data_frame


def plot_maps(data_frame: pd.DataFrame) -> None:
    """
    This method plots maps to visualize the distribution of food production around the world.

    :param data_frame: A pandas DataFrame containing data on food production.
    """
    st.title("Tabela de código dos países")

    st.dataframe(
        data=data_frame.groupby(["Area", "Alpha 3"])
        .size()
        .reset_index()
        .iloc[:, :-1]
        .sort_values(by="Alpha 3"),
        column_config={
            "Area": st.column_config.TextColumn(width="large"),
            "Alpha 3": st.column_config.TextColumn(width="small"),
        },
    )

    st.title("Distribuição Geográfica de Produtos Agrícolas")

    items = (
        data_frame.groupby("Item")
        .size()
        .sort_values(ascending=False)
        .head(st.session_state["num_items"])
        .index.tolist()
    )
    ano = str(st.session_state["ano_selecionado"])
    
    for item in items:
        filtered_df = data_frame[(data_frame["Item"] == item) & (data_frame[ano] > 1)]
        filtered_df = filtered_df.groupby("Alpha 3")[ano].sum().reset_index()  # Adicione esta linha
        fig = px.choropleth(
            filtered_df[[ano, "Alpha 3"]],
            locations="Alpha 3",
            color=ano,
            color_continuous_scale=px.colors.sequential.Plasma_r,
            hover_data=[ano],
            labels={ano: "Quantidade"},
            title=f"Produção de '{item}' em {ano}",
            range_color=[0, filtered_df[ano].max()],
        )
        # fig.update_geos(visible=False)  # Hide countries without data
        fig.update_layout(
            title_font=dict(size=20),
            coloraxis_colorbar=dict(
                title_font=dict(size=16),
            ),
            height=800,
        )
        st.plotly_chart(fig, use_container_width=True, theme=None)


def main() -> None:
    filter_df = st.session_state["df"].copy()
    filter_df = aplicar_filtros(filter_df)
    plot_maps(filter_df)


if __name__ == "__main__":
    main()
