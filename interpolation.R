# --- início do script R corrigido ---

# 1. pacotes
library(raster)
library(terra)
library(sp)
library(sf)
library(gstat)

# 2. argumentos vindos do Python
args <- commandArgs(trailingOnly = TRUE)
# args[1] = caminho da pasta que TEM os .csv (ex: "dados_predicao_bimestres_casos")
# args[2] = caminho da pasta onde VAI salvar (ex: "conjunto_treino_casos")

# 3. normaliza caminhos (relativo ou absoluto)
input_dir  <- normalizePath(args[1], winslash = "/", mustWork = FALSE)
output_dir <- normalizePath(args[2], winslash = "/", mustWork = FALSE)
base_dir   <- normalizePath(getwd(), winslash = "/", mustWork = FALSE)

# 4. arquivos para interpolar
files_to_interpolate <- list.files(
  input_dir,
  pattern = "\\.csv$",
  full.names = FALSE
)

# 5. verificação
if (length(files_to_interpolate) == 0) {
  stop("Nenhum .csv encontrado em: ", input_dir)
}

# 6. arquivos já existentes
files_existentes <- list.files(
  output_dir,
  pattern = "\\.csv$",
  full.names = FALSE
)
print(files_existentes)

# 7. grade + shapefile
coordinates  <- read.csv(file.path(base_dir, "grade_interpolacao_treino.csv"))
recife_shp   <- shapefile(file.path(base_dir, "shapefiles", "RECIFE_WGS84.shp"))

# 8. loop principal
for (k in seq_along(files_to_interpolate)) {

  csv_in     <- files_to_interpolate[k]
  fname      <- file.path(output_dir, csv_in)
  fname_shp  <- file.path(
    base_dir, "shapefiles",
    paste0(tools::file_path_sans_ext(csv_in), ".shp")
  )

  if (file.exists(fname)) {
    message("🟢 Já existe: ", csv_in)
    next
  }

  message("🛠  Gerando mapa para: ", csv_in)

  # --- leitura do CSV de entrada ---
  data <- read.csv(file.path(input_dir, csv_in))

  # --- colunas disponíveis ---
  cols <- colnames(data)

  # --- salva shapefile temporário ---
  arboviruses <- st_as_sf(
    data,
    coords = c("longitude", "latitude"),
    crs = "+proj=utm +zone=25 +south +ellps=GRS80 +units=m +no_defs"
  )
  st_write(arboviruses, fname_shp, append = FALSE, quiet = TRUE)

  # --- reprojeção e grade ---
  dataset <- shapefile(fname_shp)
  dataset <- spTransform(dataset, crs(recife_shp))

  grid <- coordinates
  names(grid)       <- c("X", "Y")
  coordinates(grid) <- c("X", "Y")
  proj4string(grid)    <- proj4string(recife_shp)
  proj4string(dataset) <- proj4string(recife_shp)

  # --- interpolações ---
  final_data <- data.frame(ID = round(runif(n = nrow(coordinates))))

  for (j in 4:length(cols)) {
    interp <- idw(dataset[[cols[j]]] ~ 1, dataset,
                  newdata = grid, idp = 2.0)

    # Adiciona só a coluna com valores interpolados
    final_data <- cbind(
      final_data,
      subset(as.data.frame(interp), select = "var1.pred")
    )
    print(cols[j])
  }

  final_data <- cbind(X = coordinates$X, Y = coordinates$Y, final_data)


  # --- salva resultado ---
  write.csv(final_data, fname, row.names = FALSE)
}

# --- fim do script corrigido ---
