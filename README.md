


COTAHIST_M042023
LAYOUT IMPORT:

let
    Fonte = Table.FromColumns({Lines.FromBinary(File.Contents("D:\Cotação\COTAHIST_M042023.TXT"), null, null, 1252)}),
    #"Dividir Coluna pelas Posições" = Table.SplitColumn(Fonte, "Column1", Splitter.SplitTextByPositions({0, 2, 10, 12, 24, 27, 39, 49, 52, 56, 69, 82, 95, 108, 121, 134, 147, 152, 170, 189, 211, 217, 218, 230, 242, 243, 245}), {"TIPREG", "DATA DO PREGAO", "CODBDI", "CODNEG", "TPMERC", "NOMRES", "ESPECI", "PRAZOT", "MODREF", "PREABE", "PREMAX", "PREMIN", "PREME", "PREULT", "PREOFC", "PREOFV", "TOTNEG", "QUATOT", "VOLTOT", "PREEXE", "INDOPC", "EXCLUIR0", "EXCLUIR1", "CODIS", "DISMES"}),
    #"Linhas Superiores Removidas" = Table.Skip(#"Dividir Coluna pelas Posições",1),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Linhas Superiores Removidas",{{"PREABE", Int64.Type}, {"PREMAX", Int64.Type}, {"PREMIN", Int64.Type}, {"PREME", Int64.Type}, {"PREULT", Int64.Type}, {"PREOFC", Int64.Type}, {"PREOFV", Int64.Type}, {"QUATOT", Int64.Type}, {"VOLTOT", Int64.Type}, {"TOTNEG", Int64.Type}}),
    #"Personalização Adicionada" = Table.AddColumn(#"Tipo Alterado", "PRE-ABE", each [PREABE] / 100),
    #"Personalização Adicionada1" = Table.AddColumn(#"Personalização Adicionada", "PRE-MAX", each [PREMAX] / 100),
    #"Personalização Adicionada2" = Table.AddColumn(#"Personalização Adicionada1", "PRE-MIN", each [PREMIN]/100),
    #"Personalização Adicionada3" = Table.AddColumn(#"Personalização Adicionada2", "PREMED", each [PREME]/100),
    #"Personalização Adicionada4" = Table.AddColumn(#"Personalização Adicionada3", "PRE-ULT", each [PREULT]/100),
    #"Personalização Adicionada5" = Table.AddColumn(#"Personalização Adicionada4", "PRE-OCF", each [PREOFC]/100),
    #"Personalização Adicionada6" = Table.AddColumn(#"Personalização Adicionada5", "PRE-OFV", each [PREOFV]/100),
    #"Colunas Removidas" = Table.RemoveColumns(#"Personalização Adicionada6",{"PREABE", "PREMAX", "PREMIN", "PREME", "PREULT", "PREOFC", "PREOFV"}),
    #"Personalização Adicionada7" = Table.AddColumn(#"Colunas Removidas", "DATA_PREGAO", each Text.Combine({Text.Middle([DATA DO PREGAO], 6, 2),"-", Text.Middle([DATA DO PREGAO], 4, 2),"-",Text.Middle([DATA DO PREGAO], 0, 4)})),
    #"Tipo Alterado1" = Table.TransformColumnTypes(#"Personalização Adicionada7",{{"PRE-ABE", type number}, {"PRE-MAX", type number}, {"PRE-MIN", type number}, {"PREMED", type number}, {"PRE-ULT", type number}, {"PRE-OCF", type number}, {"PRE-OFV", type number}}),
    #"Colunas Removidas1" = Table.RemoveColumns(#"Tipo Alterado1",{"DATA DO PREGAO"}),
    #"Tipo Alterado2" = Table.TransformColumnTypes(#"Colunas Removidas1",{{"DATA_PREGAO", type date}})
in
    #"Fonte"
