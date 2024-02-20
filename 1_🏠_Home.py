import pandas as pd
import streamlit as st

st.set_page_config(page_title="Produção Agrícola", page_icon="👨‍🌾", layout="centered")

st.title("🌾🌱 :green[Produção Agrícola] 🌽🍅")


@st.cache_data
def load_data(*, file_csv: str) -> pd.DataFrame:
    """
    Load and return the data from a CSV file.
    :param file_csv: The filename of the CSV file.
    """
    data = pd.read_csv(file_csv, index_col=0)
    return data


st.markdown(
    f"""
    # Sobre o conjunto de dados

    **Última atualização**
    Jan 22, 2024
    
    **Autor**
    [Felippe](https://www.linkedin.com/in/bysedd/)
    
    **Conjunto de dados**
    [Kaggle](https://www.kaggle.com/datasets/imtkaggleteam/crop-production/data)
    
    ## Descrição
    
    Dados da Organização das Nações Unidas para Alimentação e Agricultura (FAO)
    
    As estatísticas de culturas abrangem diversas categorias de produtos agrícolas, totalizando 173 itens. Entre 
    essas categorias estão as Culturas Primárias, Culturas de Fibra Primárias, Cereais, Grãos Grossos, 
    Frutas Cítricas, Frutas, Juta & Fibras semelhantes à juta, Bolos equivalentes, Oleaginosas primárias, 
    Leguminosas, Raízes e tubérculos, Nozes, Legumes e Melões. Esses dados englobam informações sobre área colhida, 
    quantidade de produção, rendimento e quantidade de sementes. O objetivo é fornecer uma visão abrangente da 
    produção de todas as culturas primárias em todos os países e regiões do mundo.
    """
)

st.session_state["df"] = load_data(file_csv="data/Production_Crops_E_World.csv")
st.sidebar.caption("Made with ❤️ by [Felippe A.](https://www.github.com/bysedd)")
