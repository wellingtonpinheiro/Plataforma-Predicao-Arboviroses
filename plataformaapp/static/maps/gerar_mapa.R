options(warn = 2)  # Warnings agora param a execução

library(raster)
library(sf)
library(leaflet)
library(mapview)
library(webshot2)

library(htmlwidgets)

cat("🚀 Script iniciado...\n")

tryCatch({
  # Caminhos de entrada
  arquivo_tif <- "C:/Users/lyssa/OneDrive/Documentos/PLATAFORMA PREDIÇÃO NOVA/Plataforma-Predicao-Arboviroses/plataformaapp/static/maps/predicao_recife.tif"
  arquivo_shp <- "C:/Users/lyssa/OneDrive/Documentos/PLATAFORMA PREDIÇÃO NOVA/Plataforma-Predicao-Arboviroses/plataformaapp/static/maps/bairros-polygon.shp"
  
  # Caminhos de saída
  saida_html <- "C:/Users/lyssa/predicao_recife.html"
  saida_png  <- "C:/Users/lyssa/predicao_recife.png"
  
  cat("📂 Lendo raster...\n")
  arbovirus <- raster(arquivo_tif)
  
  cat("📂 Lendo shapefile...\n")
  recife <- st_read(arquivo_shp)
  
  cat("🎨 Gerando paleta...\n")
  valores <- values(arbovirus)
  paleta <- colorNumeric(palette = "RdYlBu", domain = valores, na.color = "transparent", reverse = TRUE)
  
  cat("🗺️ Criando objeto leaflet...\n")
  mapa <- leaflet() %>%
    addRasterImage(arbovirus, colors = paleta, opacity = 1) %>%
    addPolygons(data = recife,
                color = "black",
                weight = 1.5,
                popup = ~bairro_nom,
                label = ~bairro_nom,
                group = "Bairros") %>%
    addLegend(pal = paleta, values = valores, title = "Quantidade por bairro")
  
  cat("💾 Salvando HTML temporário em:\n", saida_html, "\n")
  saveWidget(mapa, saida_html, selfcontained = TRUE)
  
  cat("⏳ Aguardando antes de capturar imagem...\n")
  Sys.sleep(2)  # segurança extra antes do webshot
  
  cat("📷 Gerando imagem PNG via webshot...\n")
  webshot(
    url = saida_html,
    file = saida_png,
    vwidth = 1000,
    vheight = 1200,
    delay = 5  # <<< ESSENCIAL para evitar PNG em branco
  )
  
  cat("✅ Mapa salvo com sucesso!\n")
  
}, error = function(e) {
  cat("❌ ERRO DETECTADO DURANTE A EXECUÇÃO:\n")
  cat(conditionMessage(e), "\n")
})
