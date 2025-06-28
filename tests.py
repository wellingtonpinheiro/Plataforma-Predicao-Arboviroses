
import rasterio

with rasterio.open("C:\\Users\\lyssa\\OneDrive\\Documentos\\PLATAFORMA PREDIÇÃO NOVA\\Plataforma-Predicao-Arboviroses\\plataformaapp\\static\\maps\\predicao_recife.tif") as src:
    print(src.crs)  
    print(src.bounds)

    data = src.read(1)
    print("Min:", data.min())
    print("Max:", data.max())
    print("Média:", data.mean())
    print("CRS:", src.crs)
