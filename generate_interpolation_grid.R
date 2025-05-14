# this script is the script to save the grid for the interpolation maps

library("terra")
library("sp")
library("sf")
library("gstat")
library("raster")

# load the data for arboviruses
recife_shp <- shapefile("C:/Users/clari/PycharmProjects/projetoCNPq/shapefiles/RECIFE_WGS84.shp")

# create the grid
grid <- as.data.frame(spsample(recife_shp, "random", n=5000))
names(grid)       <- c("X", "Y")
coordinates(grid) <- c("X", "Y")
#gridded(grid)     <- TRUE  # Create SpatialPixel object
#fullgrid(grid)    <- TRUE  # Create SpatialGrid object

# save the grid
write.csv(grid, "C:/Users/clari/PycharmProjects/projetoCNPq/grade_interpolacao_treino.csv", row.names = FALSE)
