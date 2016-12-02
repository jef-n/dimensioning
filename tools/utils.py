# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import QDir
from qgis.core import QgsFeature, QgsDataSourceURI, QgsVectorLayer, QgsMapLayerRegistry, QgsApplication, QgsMessageLog, QgsWKBTypes


def logMessage(s):
    QgsMessageLog.logMessage(s, "dimensioning")


def addGeometryToDimensionLayer(feat, type, c):
    if feat.geometry().type() != 1:
        logMessage("invalid geometry type {}".format(feat.geometry().type()))
        return

    if type == "main":
        layerName = "Dimension main lines"
        tableName = "lines_main"
    else:
        layerName = "Dimension help lines"
        tableName = "lines_help"

    logMessage("layerName={} tableName={}".format(layerName, tableName))

    l = getLayerByName(layerName)
    if l is None:
        logMessage("no layer found")

        uri = QgsDataSourceURI()
        uri.setDatabase(QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/dimensioning/sqlite/dimension.sqlite')))
        uri.setDataSource('', tableName, 'geometry')
        uri.setWkbType(QgsWKBTypes.LineString)

        l = QgsVectorLayer(uri.uri(), layerName, 'spatialite')
        if not l.isValid():
            logMessage("layer is invalid")
            return

        qml = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/dimensioning/styles/default_' + type + '.qml'))
        l.loadNamedStyle(qml)

        l.setCrs(c.mapSettings().destinationCrs())

        QgsMapLayerRegistry.instance().addMapLayer(l, True)

    pr = l.dataProvider()
    pr.addFeatures([feat])
    l.updateExtents()


def getLayerByName(layername):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.name() == layername:
            if layer.isValid():
                return layer
            else:
                return None


def createHelpFeature(geom, main_from, layer_id):
    feat = QgsFeature()
    feat.setGeometry(geom)
    feat.initAttributes(3)
    feat.setAttribute(0, None)
    feat.setAttribute(1, main_from)
    feat.setAttribute(2, layer_id)

    return feat


def createMainFeature(geom, layer_id, length):
    feat = QgsFeature()
    feat.setGeometry(geom)
    feat.initAttributes(3)
    feat.setAttribute(0, None)
    feat.setAttribute(1, layer_id)
    feat.setAttribute(2, length)

    return feat
