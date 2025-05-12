import streamlit as st


#########################################
# SAYFA KULLANIM AYARI, SEKME ADI:
#########################################

st.set_page_config(page_title="miuul coffee shop", page_icon="☕", layout="wide")
# layout="centered" tüm ekranı kullanır

#########################################
#########################################
# LOGO VE SLOGAN:
#########################################

col1, col2, col3 = st.columns(3)
col2.image("miul_son - Kopya.png", width=550, use_container_width=False) #tüm ekran için true yap
col2.markdown("<h2 style='text-align: center;'>Kahve İçmenin En Akıllı Hali...</h2>", unsafe_allow_html=True)
col2.markdown("<h2 style='text-align: center;'> </h2>", unsafe_allow_html=True)

#########################################
#########################################
# YAN FOTOĞRAFLAR;
#########################################

col1, col2, col3 = st.columns([1,4,1])

col1.image("serbest_cekirdek.png", width=400, use_container_width=False) #tüm ekran için true yap
col3.image("serbest_cekirdek.png", width=400, use_container_width=False) #tüm ekran için true yap

#########################################
#########################################
# AÇIKLAMA KISMI;
#########################################

#col1, col2, col3 = st.columns([1,4,1])

#col2.title("Dünyanın ilk yapay zeka destekli kahve molası:")
col2.markdown("<h1 style='text-align: center;'>Dünyanın ilk yapay zeka destekli kahve molası:</h1>", unsafe_allow_html=True)


col2.markdown("<h5 style='text-align: center;'>Sizleri sadece bir alışkanlığa değil, her yudumda optimum keyfi bulmak için bir yolculuğa davet ediyoruz. "
            "Burada her yudum, bir algoritmanın değil, bir anının parçası olur. "
            "Çünkü burada K-means ile değil, dost sohbetiyle kümeleniyoruz.</h5>", unsafe_allow_html=True)

#########################################
#########################################


# Motto Cümleler:

# Veriler değişir, kahve sabit kalır.
# Her veri seti bir hikâye anlatır, her kahve bir anıya dönüşür.
# Kahve içmeden önce p-değerine güvenmem.
# Korelasyon kahveye olan tutkumuzu açıklamaz.
# Bayes bile bu kahvenin olasılığını önceden tahmin edemezdi.
# Gradient descent gibi: Her yudumda optimum keyif.
# K-means ile değil, dost sohbetiyle kümeleniyoruz
# Dünyanın ilk yapay zeka destekli kahve molası

# ####################
# st.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
# st.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
#
# import streamlit as st
#
# col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
#
#
# sentiment_mapping = ["one", "two", "three", "four", "five"]
# selected = col4.feedback("stars")
# if selected is not None:
#     col4.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

