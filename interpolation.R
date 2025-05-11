# Definindo diretório de trabalho
directory <- getwd()
setwd(directory)

# Bibliotecas necessárias
library("raster")
library("terra")
library("sp")
library("sf")
library("gstat")
library("rgdal")  # Necessária para writeOGR

# Argumentos vindos do Python
options(echo=TRUE)
args <- commandArgs(trailingOnly = TRUE)
print(args)

# Garantir que a pasta de shapefiles exista
dir.create(paste0(directory, "/shapefiles"), showWarnings = FALSE, recursive = TRUE)

# Carregar grade de interpolação (coordenadas X, Y)
coordinates_grid <- read.csv(paste0(directory, "/grade_interpolacao_treino.csv"))

# Listar arquivos CSV a interpolar
files_to_interpolate <- list.files(paste0(directory, "/", args[[1]]), pattern = "*.csv")
print(paste0("Arquivos para interpolar: ", files_to_interpolate))

# Garantir que a pasta de saída existe
dir.create(paste0(directory, "/", args[[2]]), showWarnings = FALSE)

# Iterar sobre cada arquivo para interpolação
for (i in 1:length(files_to_interpolate)) {
  
  # Nome base do arquivo (sem extensão)
  nome_base <- gsub(".csv", "", files_to_interpolate[[i]])
  
  # Caminho final do CSV interpolado
  filename <- paste0(directory, "/", args[[2]], "/", files_to_interpolate[[i]])
  
  # Caminho para shapefile temporário
  filename_shp <- paste0(directory, "/shapefiles/", nome_base, ".shp")
  
  # Se já existe, pula
  if (file.exists(filename)) {
    print(paste("✅ Arquivo já existe:", filename))
    next
  }
  
  print(paste("🔄 Gerando mapas para:", files_to_interpolate[[i]]))
  
  # Carregar dados de entrada
  data <- read.csv(paste0(directory, "/", args[[1]], "/", files_to_interpolate[[i]]))
  columns <- colnames(data)
  
  if (!all(c("latitude", "longitude") %in% columns)) {
    print("⚠️ Dados sem colunas 'latitude' e 'longitude'. Pulando.")
    next
  }

  # Criar shapefile a partir dos pontos
  arboviruses <- st_as_sf(data, coords = c("longitude", "latitude"),
                          crs = "+proj=utm +zone=25 +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
  st_write(arboviruses, filename_shp, append = FALSE, quiet = TRUE)

  # Carregar shapefile do Recife
  recife_shp <- shapefile(paste0(directory, "/shapefiles/NOVO RECIFE.shp"))
  
  # Preparar grade de interpolação
  grid <- coordinates_grid
  names(grid) <- c("X", "Y")
  coordinates(grid) <- c("X", "Y")
  
  # Carregar shapefile de entrada como objeto Spatial
  dataset <- shapefile(filename_shp)
  
  # Ajustar projeções
  dataset <- spTransform(dataset, crs(recife_shp))
  proj4string(dataset) <- proj4string(recife_shp)
  proj4string(grid) <- proj4string(recife_shp)
  
  # Inicializar dataframe com coordenadas
  final_data <- data.frame(Y = coordinates_grid$Y, X = coordinates_grid$X)
  
  # Interpolar colunas numéricas (a partir da 4ª coluna)
  if (length(columns) >= 4) {
    for (j in 4:length(columns)) {
      coluna_nome <- columns[[j]]
      print(paste("🌐 Interpolando:", coluna_nome))
      
      # Interpolação IDW
      interpolacao <- idw(dataset[[coluna_nome]] ~ 1, dataset, newdata = grid, idp = 2.0)
      interpolado <- as.data.frame(interpolacao)[, "var1.pred", drop = FALSE]
      colnames(interpolado) <- coluna_nome
      
      # Adicionar ao resultado final
      final_data <- cbind(final_data, interpolado)
    }
  } else {
    print("⚠️ Dataset não possui colunas suficientes para interpolação.")
    next
  }

  # Salvar CSV interpolado
  print(paste("💾 Salvando CSV interpolado em:", filename))
  write.csv(final_data, filename, row.names = FALSE)
  print(paste("✅ Mapa salvo:", filename))

  # Salvar também como shapefile interpolado
  coordinates(final_data) <- ~ X + Y
  proj4string(final_data) <- proj4string(recife_shp)

  shapefile_interpolado <- paste0(directory, "/shapefiles/", nome_base, "_interpolado.shp")
  writeOGR(final_data, dsn = shapefile_interpolado, layer = nome_base, driver = "ESRI Shapefile", overwrite_layer = TRUE)
  print(paste("🗺️ Shapefile salvo:", shapefile_interpolado))
}
