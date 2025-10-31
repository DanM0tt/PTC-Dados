import pandas as pd

url = "https://docs.google.com/spreadsheets/d/11bCP6whPkNnk5Se1iPqUL6QReB3cl_8BI-do5wJIb5w/export?format=csv"
df = pd.read_csv(url) #Importar o documento

#Nivel_Senioridade--------------------------------------------------------------------------------------------------------

#print(df["Nivel_Senioridade"].value_counts()) -> Função usada para descobrir os nomes presentes na planilha

senioridade = { #Cria um dicionário para fazer todas as trocas necessárias
    "P": "Pleno",
    "pleno": "Pleno",
    "senior": "Sênior",
    "Jr": "Júnior",
    "JR": "Júnior",
    "N/D": df["Nivel_Senioridade"].mode()[0]
}
df["Nivel_Senioridade"] = df["Nivel_Senioridade"].replace(senioridade) #Realiza as trocas especificadas no dicionário
df["Nivel_Senioridade"] = df["Nivel_Senioridade"].replace("N/D", df["Nivel_Senioridade"].mode()[0])

#print(df["Nivel_Senioridade"].value_counts()) -> Teste para saber se funcionou

#----------------------------------------------------------------------------------------------------------------------------
#Avalicao_Tecnica------------------------------------------------------------------------------------------------------------

#print(df["Avaliacao_Tecnica"].value_counts()) -> Função usada para descobrir os valores presentes na planilha

df["Avaliacao_Tecnica"] = df["Avaliacao_Tecnica"].fillna(df["Avaliacao_Tecnica"].mean().round(1)) #Substitui os valores nulos pela média, aredondando com uma casa decimal
df["Avaliacao_Tecnica"] = df["Avaliacao_Tecnica"].astype(str).str.replace(".", ",", regex=False) #Troca o ponto pela vírgula transformando em string

#print(df["Avaliacao_Tecnica"].value_counts()) -> Teste para saber se funcionou

#----------------------------------------------------------------------------------------------------------------------------
#Avalicao_Comportamental-----------------------------------------------------------------------------------------------------

#print(df["Avaliacao_Comportamental"].value_counts()) -> Função usada para descobrir os valores presentes na planilha

df["Avaliacao_Comportamental"] = df["Avaliacao_Comportamental"].fillna(df["Avaliacao_Comportamental"].mean().round(1)) #Substitui os valores nulos pela média, aredondando com uma casa decimal
df["Avaliacao_Comportamental"] = df["Avaliacao_Comportamental"].astype(str).str.replace(".", ",", regex=False) #Troca o ponto pela vírgula transformando em string

#print(df["Avaliacao_Comportamental"].value_counts()) -> Teste para saber se funcionou

#----------------------------------------------------------------------------------------------------------------------------
#Engajamento_PIGs------------------------------------------------------------------------------------------------------------

#print(df["Engajamento_PIGs"].value_counts()) -> Função usada para descobrir os valores presentes na planilha

df["Engajamento_PIGs"] = df["Engajamento_PIGs"].str.replace("%", "", regex=False) #Retira o símbolo de porcentagem
df["Engajamento_PIGs"] = df["Engajamento_PIGs"].astype(float) / 100 #Divide por 100 transformando em float
df["Engajamento_PIGs"] = df["Engajamento_PIGs"].fillna(df["Engajamento_PIGs"].mean().round(2)) #Substitui os valores nulos pela média


#print(df["Engajamento_PIGs"].value_counts()) -> Teste para saber se funcionou

#----------------------------------------------------------------------------------------------------------------------------
#Score_Desempenho------------------------------------------------------------------------------------------------------------

#Cria uma coluna temporária para transformar os valores das colunas originais em float
tec = df["Avaliacao_Tecnica"].astype(str).str.replace(",", ".", regex=False).astype(float)
comp = df["Avaliacao_Comportamental"].astype(str).str.replace(",", ".", regex=False).astype(float)

df["Score_Desempenho"] = ((tec * 0.5) + (comp * 0.5)).round(2) #Cria a nova coluna com a fórmula em questão

#print(df["Score_Desempenho"].value_counts()) -> Teste para saber se funcionou

#----------------------------------------------------------------------------------------------------------------------------
#Status_Membro---------------------------------------------------------------------------------------------------------------

def classificar_membro(linha):
    if linha["Score_Desempenho"] >= 7 and linha["Engajamento_PIGs"] >= 0.8:
        return "Em Destaque"
    else:
        return "Padrão"

df["Status_Membro"] = df.apply(classificar_membro, axis=1)

#print(df["Status_Membro"].value_counts()) -> Teste para saber se funcionou

#----------------------------------------------------------------------------------------------------------------------------

df.to_csv("Base_Membros_Tratada.csv", index=True, index_label="ID_Membro", encoding="utf-8-sig")
