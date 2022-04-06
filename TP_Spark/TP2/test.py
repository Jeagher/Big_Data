import pandas as pd 

df = pd.read_csv("E:\\3A\BigData\TP_BigData_ECL\TP_Spark\TP2\ml-latest-small\\movies.csv",sep=',')



df["title"] = df["title"].str.replace(',',";")
df  = df[["movieId","title","genres"]]
      
df.to_csv("E:\\3A\BigData\TP_BigData_ECL\TP_Spark\TP2\ml-latest-small\\movies.csv", sep = ',',index=False)

print(df["title"])

