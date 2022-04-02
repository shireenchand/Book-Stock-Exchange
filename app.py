import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import pickle
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix


books = pd.read_csv("Books.csv")
ratings = pd.read_csv("Ratings.csv")
users = pd.read_csv("Users.csv")
data = books.merge(ratings,how="left", on="ISBN")
data2 = data.merge(users,how="left", on="User-ID")
data2.dropna(inplace=True)
data2['User-ID'] = data2['User-ID'].astype('int')
data2['Age'] = data2['Age'].astype('int')
data2.drop(columns=["Image-URL-S","Image-URL-M"],inplace=True)
data2 = data2[data2["Book-Rating"]>0]
book_counts = pd.DataFrame(data2["Book-Title"].value_counts())
rare_book = book_counts[book_counts["Book-Title"] <= 100].index
common_book = data2[~data2["Book-Title"].isin(rare_book)]
user_book_df = common_book.pivot_table(index=["User-ID"], columns=["Book-Title"], values="Book-Rating")
user_book_df.fillna(0,inplace=True)
u = user_book_df.transpose()
book_sparse = csr_matrix(u)

# u = pd.Series(u)

model = NearestNeighbors(algorithm='brute')
model.fit(book_sparse)


with open("dict", "rb") as fp:
  dictionary = pickle.load(fp)

with open("names", "rb") as fp:
  names = pickle.load(fp)

with open("Authors", "rb") as fp:
  authors = pickle.load(fp)


# for i in range(91):
# 	with st.expander(names[i]):
# 		url = dictionary[names[i]]
# 		st.write(f"Author: {authors[names[i]]}")
# 		response = requests.get(url)
# 		img = Image.open(BytesIO(response.content))
# 		newsize = (200, 200)
# 		img = img.resize(newsize)
# 		st.image(img,caption=names[i])

# 		if st.button("See Similar Books",key=names[i]):
# 			print(names[i])
# 			distances, suggestions = model.kneighbors(u.iloc[i, :].values.reshape(1, -1))
# 			idx = 1
# 			for i in range(5):
#   				print(u.index[suggestions[0,i]])

#   				st.subheader(f"{idx}. {u.index[suggestions[0,i]]}")
#   				idx += 1

# st.sidebar.write("Enter Book Name")

if book_name == "":
		book_name = "The Testament"
		
try:
	st.sidebar.markdown("<h1 style='text-align: center; color: #ECB365;'>BOOK STOCK EXCHANGE</h1>", unsafe_allow_html=True)
	book_name = st.sidebar.text_input(label="Enter Book name")
	i = list(names).index(book_name)
	url = dictionary[book_name]
	st.sidebar.write(f"Author: {authors[names[i]]}")
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	newsize = (300, 400)
	img = img.resize(newsize)
	st.sidebar.image(img,caption=names[i])
	if st.sidebar.button("See Similar Books",key=names[i]):
		print(names[i])
		distances, suggestions = model.kneighbors(u.iloc[i, :].values.reshape(1, -1))
		idx = 1
		for i in range(5):
			print(u.index[suggestions[0,i]])
			t = u.index[suggestions[0,i]]
			st.subheader(f"{idx}. {u.index[suggestions[0,i]]}")
			url = dictionary[t]
			i = list(names).index(t)
			st.write(f"Author: {authors[names[i]]}")
			response = requests.get(url)
			img = Image.open(BytesIO(response.content))
			newsize = (300, 400)
			img = img.resize(newsize)
			st.image(img,caption=names[i])
			idx += 1

except Exception as e:
	st.markdown("<h1 style='text-align: center; color: black;'>COULD NOT FIND THE BOOK!!!</h1>", unsafe_allow_html=True)
	st.markdown("<h2 style='text-align: center; color: black;'>Check the spelling or add the name of the Author as well</h2>", unsafe_allow_html=True)
	print(e)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
















