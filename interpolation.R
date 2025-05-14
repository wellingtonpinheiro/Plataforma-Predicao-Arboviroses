# --- início do script R corrigido ---

# 1. workspace
directory <- getwd()

# 2. pacotes
library(raster)
library(terra)
library(sp)
library(sf)
library(gstat)

# 3. argumentos vindos do Python
args <- commandArgs(trailingOnly = TRUE)
# args[1] = pasta que TEM os .csv   (p.ex. "dados predicao bimestres casos")
# args[2] = pasta onde VAI salvar   (p.ex. "conjunto treino casos")

# 4. arquivos para interpolar
files_to_interpolate <- list.files(
  file.path(directory, args[1]),
  pattern = "\\.csv$",            # ← regex correta
  full.names = FALSE
)

# 5. para garantir:
if (length(files_to_interpolate) == 0) {
  stop("Nenhum .csv encontrado em: ", file.path(directory, args[1]))
}

# 6. já existentes na pasta de saída
files_existentes <- list.files(
  file.path(directory, args[2]),
  pattern = "\\.csv$",
  full.names = FALSE
)
print(files_existentes)

# 7. grade + shapefile
coordinates  <- read.csv(file.path(directory, "grade_interpolacao_treino.csv"))
recife_shp   <- shapefile(file.path(directory, "shapefiles", "RECIFE_WGS84.shp"))

# 8. loop principal
for (k in seq_along(files_to_interpolate)) {

  csv_in  <- files_to_interpolate[k]
  fname   <- file.path(directory, args[2], csv_in)
  fname_shp <- file.path(
    directory, "shapefiles",
    paste0(tools::file_path_sans_ext(csv_in), ".shp")
  )

  if (file.exists(fname)) {
    message("🟢 Já existe: ", csv_in)
    next
  }

  message("🛠  Gerando mapa para: ", csv_in)

  # --- leitura do CSV de entrada ---
  data <- read.csv(file.path(directory, args[1], csv_in))

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
  final_data <- round(runif(n = nrow(coordinates)))

  for (j in 4:length(cols)) {              # ← j, não i
    interp <- idw(dataset[[cols[j]]] ~ 1, dataset,
                  newdata = grid, idp = 2.0)

    final_data <- cbind(
      final_data,
      subset(as.data.frame(interp), select = -c(X, Y, var1.var))
    )
    print(cols[j])
  }

  final_data <- cbind(coordinates$Y, coordinates$X, final_data)
  colnames(final_data) <- cols[2:length(cols)]

  # --- salva resultado ---
  write.csv(final_data, fname, row.names = FALSE)
}
# --- fim do script corrigido ---
