# -*- coding: utf-8 -*-

from qgis.core import QgsVectorFileWriter, QgsCoordinateReferenceSystem, QgsLayerDefinition
from abc import abstractmethod        
# save_options = QgsVectorFileWriter.SaveVectorOptions()
# result = QgsVectorFileWriter.writeAsVectorFormat(self.tweet_layer, file_name, "UTF-8", "EPSG:4326" , "ESRI Shapefile")


class LayerExport:
    """QGIS Layer export class wrapper"""
    def __init__(self, layer_obj, layer_path, export_format):
        self.layer_obj = layer_obj
        self.layer_path = layer_path
        self.export_format = export_format
    
    @abstractmethod
    def export_layer(self):
        pass


class ShpLayerExport(LayerExport):
    def __init__(self, layer_obj, layer_path, export_format="ESRI Shapefile"):
        super().__init__(layer_obj, layer_path, export_format)
    
    def export_layer(self):
        error = QgsVectorFileWriter.writeAsVectorFormat(
            layer=self.layer_obj, fileName=self.layer_path, 
            driverName=self.export_format, fileEncoding='UTF-8',
            symbologyExport=QgsVectorFileWriter.SymbolLayerSymbology,
            destCRS=QgsCoordinateReferenceSystem(self.layer_obj.proj))